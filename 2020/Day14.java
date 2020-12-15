import java.io.*;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class Day14 {
    public static interface Prog {
        public void setMask(String mask);
        public void assign(long address, long value);
        public Map<Long, Long> getMemory();
    }

    public static class ProgA implements Prog {
        protected String currentMask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
        public Map<Long, Long> memory = new HashMap<>();
        protected long oneMask = 1;
        protected long zeroMask = 0;
        public Map<Long, Long> getMemory() { return memory; }

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

    public static class ProgB implements Prog {
        protected String currentMask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
        public Map<Long, Long> memory = new HashMap<>();
        protected long oneMask = 0;
        // protected List<Long> allMasks = new ArrayList<>();
        public Map<Long, Long> getMemory() { return memory; }

        public void setMask(String mask) {
            currentMask = mask;
            
            // List<String> maskStrs = getAllMasks(mask);
            // System.out.println("Possibilites for " + mask);
            // for(String s: maskStrs) {
            //     System.out.println(s);
            // }

            // allMasks = maskStrs.stream()
            //     .map(s -> Long.valueOf(s, 2))
            //     .collect(Collectors.toList());

            // for(Long maskL: allMasks) {
            //     System.out.println(maskL);
            // }
        }

        public String maskFromAddress(long address) {
            String addressBinary = String.format("%36s", Long.toBinaryString(address)).replace(' ', '0');
            
            char[] copy = currentMask.toCharArray();
            for(int i=0; i<addressBinary.length(); i++) {
                // Xs take precedence
                if(copy[i] == 'X') continue;
                if(addressBinary.charAt(i) == '0') continue;

                // should write a 1
                copy[i] = addressBinary.charAt(i);
            }
            return String.valueOf(copy);
        }

        public void assign(long address, long value) {
            String adjustedMask = maskFromAddress(address);
            // System.out.println("address = " + address + " = " +
            //     Long.toBinaryString(address) + " mask=" + currentMask +
            //     " adjustedMask=" + adjustedMask);
            for(String maskStr: getAllMasks(adjustedMask)) {
                long adjustedAddress = Long.valueOf(maskStr, 2);
                // System.out.println("mask=" + maskStr + " adjustedAddress=" + adjustedAddress);
                memory.put(adjustedAddress, value);
            }

            // // every one in the mask should become a one.
            // System.out.println("Original address: " + address + " = " + Long.toBinaryString(address));
            // for(long mask: allMasks) {
            //     long adjustedAddress = address | mask;
            //     System.out.println("with mask (" + Long.toBinaryString(mask) + ") writing to " + adjustedAddress + " = " + Long.toBinaryString(adjustedAddress));
            //     memory.put(adjustedAddress, value);
            // }
        }

        public List<String> getAllMasks(String mask) {
            // get the first X
            int index = mask.indexOf('X');
            if(index == -1) {
                return Arrays.asList(mask);
            }

            ArrayList<String> all = new ArrayList<>();
            char[] cs = mask.toCharArray();
            cs[index] = '0';
            List<String> zeroStr = getAllMasks(String.valueOf(cs));
            cs[index] = '1';
            List<String> oneStr = getAllMasks(String.valueOf(cs));
            all.addAll(zeroStr);
            all.addAll(oneStr);
            return all;
        }
    }
    public static long getAnswerA(String filepath, Prog prog) throws IOException {
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
        for(Map.Entry<Long, Long> entry: prog.getMemory().entrySet()) {
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
            getAnswerA(args[0], new ProgA())));
        System.out.println(String.format(
            "A. the sum of all values left in memory after it completes is %d",
            getAnswerA(args[0], new ProgB())));
    }
}
