import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class Day16 {
    public static class Field {
        public String name;
        public List<int[]> constraints = new ArrayList<>();

        public boolean valueWithinConstraints(int v) {
            for(int[] constraint: constraints) {
                if(v < constraint[0]) continue;
                if(v > constraint[1]) continue;
                return true;
            }
            return false;
        }
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
            sum += getTicketErrorRate(input, ticket);
        }        
        
        return sum;
    }

    protected static int getTicketErrorRate(Input input, int[] ticket) {
        int sum = 0;

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

        return sum;
    }

    public static List<String> getFieldOrdering(Input input) {
        // assumes all tickets have equal number of fields
        int fieldCount = input.fields.size();
        List<Set<String>> sets = new ArrayList<>();
        List<int[]> validTickets = input.nearbyTickets
            .stream()
            .filter(t -> getTicketErrorRate(input, t) == 0)
            .collect(Collectors.toList());
        for(int i=0; i<fieldCount; i++) {            
            sets.add(new HashSet<>());
            for(int t=0; t<validTickets.size(); t++) {
                int[] ticket = validTickets.get(t);
                int value = ticket[i];
                Set<String> possibilities = new HashSet<>();

                for(Field field: input.fields) {
                    if(! field.valueWithinConstraints(value)) continue;

                    possibilities.add(field.name);
                }

                // System.out.println("i=" + i + " t=" + t + " ps=" + possibilities);

                if(t == 0) {
                    sets.get(i).addAll(possibilities);
                    // System.out.println("field index " + i + " has possiblities " + possibilities);
                    continue;
                }

                Set<String> s = sets.get(i);
                if(s.isEmpty()) continue;
                s.retainAll(possibilities);
                // if(s.isEmpty()) {
                //     System.out.println("At fieldIndex=" + i + " ticket=" + t + " set is empty! Possibilities were: " + possibilities);
                // }
            }
            // System.out.println(String.format("Field %d could be %s", i, sets.get(i)));            
        }

        List<Set<String>> toSimplify = new ArrayList<>(sets);
        while(! toSimplify.isEmpty()) {
            int examining = -1;
            // get a set with only one element
            for(int i=0; i<toSimplify.size(); i++) {
                if(toSimplify.get(i).size() == 1) {
                    examining = i;
                    break;
                }
            }
            if(examining == -1) {
                System.out.println("Big problem!");
                break;
            }

            String strToRemove = null;
            for(String s: toSimplify.get(examining)) {
                strToRemove = s;
                break;
            }

            // this must be the right field so remove it from all others
            toSimplify.remove(examining);
            for(Set<String> s: toSimplify) {
                s.remove(strToRemove);
            }
        }

        // System.out.println("Final answers");
        // for(Set<String> s: sets) {
        //     System.out.println(s);
        // }


        return IntStream.range(0, sets.size())
            .boxed()
            .map(i -> {
                for(String str: sets.get(i)) {
                    return str;
                }
                return "BAD" + i;
            })
            .collect(Collectors.toList());
    }

    public static long getAnswerB(Input input) {
        List<String> fields = getFieldOrdering(input);

        Map<String, Integer> myTicketValues = new HashMap<>();
        for(int i=0; i<fields.size(); i++) {
            myTicketValues.put(fields.get(i), input.myTicket[i]);
        }

        System.out.println("My ticket values are " + myTicketValues);

        long product = 1;
        for(Map.Entry<String, Integer> entry: myTicketValues.entrySet()) {
            if(! entry.getKey().startsWith("departure")) continue;

            product *= entry.getValue();
        }

        return product;
    }

    public static void main(String[] args) throws IOException {
        Input input = parseInput(args[0]);
        System.out.println(String.format(
            "Parsed input with %d criteria, my ticket with %d fields, and %d other nearby tickets.",
            input.fields.size(),
            input.myTicket.length,
            input.nearbyTickets.size()));
        System.out.println("A. My ticket scanning error rate is " + getAnswerA(input));
        System.out.println("B. If I multiply the values of the departure fields together I get " + getAnswerB(input));
    }
}
