import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;
import java.util.stream.Collectors;

public class Day16 {
    public static class Field {
        public String name;
        public List<int[]> constraints = new ArrayList<>();
    }

    public static class Input {
        public List<Field> fields = new ArrayList<>();
        public int[] myTicket = new int[0];
        public List<int[]> nearbyTickets = new ArrayList<>();
    }

    public static Field parseField(String line) {
        return null;
    }

    public static Input parseInput(String filepath) throws IOException {
        Input input = new Input();
        final int MODE_PARSINGFIELDS = 0, MODE_PARSINGMYTICKET = 1,
            MODE_PARSINGOTHERTICKETS = 2;
        int mode = MODE_PARSINGFIELDS;
        
        for(String line: Files.readAllLines(Paths.get(filepath))) {
            if(mode == MODE_PARSINGFIELDS) {
                if(parseInputFields(input, line)) continue;
                mode = MODE_PARSINGMYTICKET;
            }
            else if(mode == MODE_PARSINGMYTICKET) {
                if(parseMyTicket(input, line)) continue;
                mode = MODE_PARSINGOTHERTICKETS;
            }
            else if(mode == MODE_PARSINGOTHERTICKETS) {
                if(parseOtherTickets(input, line)) continue;

                break;
            }
        }

        return input;
    }

    static Pattern patField = Pattern.compile("(?<name>[\\w ]+): (?<aMin>\\d+)-(?<aMax>\\d+) or (?<bMin>\\d+)-(?<bMax>\\d+)");
    public static boolean parseInputFields(Input input, String line) {
        if(line.isEmpty()) return false;

        Matcher matcher = patField.matcher(line);
        if(! matcher.find()) return false;

        Field field = new Field();
        field.name = matcher.group("name");
        List<Integer> items = Arrays.asList(
                matcher.group("aMin"),
                matcher.group("aMax"),
                matcher.group("bMin"),
                matcher.group("bMax")
            )
            .stream()
            .map(s -> Integer.valueOf(s))
            .collect(Collectors.toList());

        field.constraints.add(new int[]{items.get(0), items.get(1)});
        field.constraints.add(new int[]{items.get(2), items.get(3)});

        input.fields.add(field);

        return true;
    }

    public static int[] parseTicket(String line) {
        return Arrays.asList(line.split(","))
            .stream()
            .map(Integer::valueOf)
            .mapToInt(Integer::intValue)
            .toArray();
    }

    public static boolean parseMyTicket(Input input, String line) {
        if(line.equals("your ticket:")) return true;
        if(line.isEmpty()) return false;

        input.myTicket = parseTicket(line);
        return true;
    }

    public static boolean parseOtherTickets(Input input, String line) {
        if(line.equals("nearby tickets:")) return true;
        if(line.isEmpty()) return false;

        input.nearbyTickets.add(parseTicket(line));
        return true;
    }

    protected static int getAnswerA(Input input) {
        int sum = 0;
        
        for(int[] ticket: input.nearbyTickets) {
            for(int value: ticket) {
                boolean valueIsValid = false;
                for(Field field: input.fields) {
                    for(int[] constraint: field.constraints) {
                        if(constraint[0] <= value && value <= constraint[1]) {
                            valueIsValid = true;
                            break;
                        }
                    }
                    if(valueIsValid) break;
                }
                if(! valueIsValid) sum+= value;
            }
        }        
        
        return sum;
    }

    public static void main(String[] args) throws IOException {
        Input input = parseInput(args[0]);
        System.out.println(String.format(
            "Parsed input with %d criteria, my ticket with %d fields, and %d other nearby tickets.",
            input.fields.size(),
            input.myTicket.length,
            input.nearbyTickets.size()));
        System.out.println("My ticket scanning error rate is " + getAnswerA(input));
    }
}
