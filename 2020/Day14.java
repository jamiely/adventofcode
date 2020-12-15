import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Day14 {
    public static class Prog {
        protected String currentMask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
        public Map<Long, Long> memory = new HashMap<>();
        protected long oneMask = 1;
        protected long zeroMask = 0;

        public void setMask(String mask) {
            currentMask = mask;

            // now create separate masks
            String oneMaskStr = mask.replace('X', '0'); // will use | to combine
            oneMask = Long.parseLong(oneMaskStr, 2);
            String zeroMaskStr = mask.replace('X', '1'); // will use & to comebine
            zeroMask = Long.parseLong(zeroMaskStr, 2);
        }

        public void assign(long address, long value) {
            long maskAppliedValue = (value | oneMask) & zeroMask;
            memory.put(address, maskAppliedValue);
        }
    }
    public static long getAnswerA(String filepath) throws IOException {
        Prog prog = new Prog();
        try(BufferedReader reader = new BufferedReader(new FileReader(filepath))) {
            String line = reader.readLine();
            while(line != null) {
                if(line.startsWith("mask")) {
                    processLineMask(prog, line);
                }
                else if(line.startsWith("mem")) {
                    processLineMem(prog, line);
                }
                else {
                    System.out.println("Unrecognized line");
                }
                line = reader.readLine();
            }
        }

        long sum = 0;
        for(Map.Entry<Long, Long> entry: prog.memory.entrySet()) {
            sum += entry.getValue();
        }
        return sum;
    }

    static Pattern patMask = Pattern.compile("^mask = (?<mask>[01X]+)$");
    public static void processLineMask(Prog prog, String line) {
        Matcher m = patMask.matcher(line);
        if(! m.matches()) {
            System.out.println("There was a problem matching line " + line);
            return;
        }
        String mask = m.group("mask");
        prog.setMask(mask);
    }
    static Pattern patAssignment = Pattern.compile("^mem\\[(?<address>\\d+)\\] = (?<value>\\d+)$");
    public static void processLineMem(Prog prog, String line) {
        Matcher m = patAssignment.matcher(line);
        if(! m.matches()) {
            System.out.println("There was a problem matching line " + line);
            return;
        }

        long address = Long.valueOf(m.group("address"));
        long value = Long.valueOf(m.group("value"));
        prog.assign(address, value);
    }
    public static void main(String[] args) throws IOException {
        System.out.println(String.format(
            "A. the sum of all values left in memory after it completes is %d",
            getAnswerA(args[0])));
    }
}
