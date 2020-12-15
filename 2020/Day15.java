import java.util.*;
import java.util.stream.Collectors;

public class Day15 {
    public static long getNthNumber(List<Integer> startingNumbers, long n) {
        Map<Long, Long> memLastTurn = new HashMap<>();
        Map<Long, Long> memLastTurn2 = new HashMap<>();

        long turn = 1;
        long last = -1;
        for(int i=0; i<startingNumbers.size(); i++, turn++) {
            long num = startingNumbers.get(i);
            if(memLastTurn.containsKey(num)) {
                memLastTurn2.put(num, memLastTurn.get(num));
            }
            memLastTurn.put(num, turn);
            last = num;
        }

        for(; turn<=n; turn++) {
            if(memLastTurn2.containsKey(last)) {
                long lastTurn = memLastTurn2.get(last);
                long diff = turn - lastTurn - 1;
                if(turn < 11) System.out.println(turn + ": " + last + " was last spoken at " + lastTurn + " so we will say " + diff);
                last = diff;

            } else {
                if(turn < 11) System.out.println(turn + ": " + last + " was first spoken the previous round.");
                last = 0;
            }
            
            if(memLastTurn.containsKey(last)) {
                memLastTurn2.put(last, memLastTurn.get(last));
            }
            memLastTurn.put(last, turn);

            if(turn % 1000000 == 0) {
                System.out.println("On turn "+ turn);
            }
        }
        return last;
    }

    protected static List<Integer> parseStartingNumbers(String list) {
        return Arrays.asList(list.split(","))
            .stream()
            .map(Integer::valueOf)
            .collect(Collectors.toList());
    }

    public static long getAnswerA(List<Integer> startingNumbers) {
        return getNthNumber(startingNumbers, 2020);
    }
    public static long getAnswerB(List<Integer> startingNumbers) {
        // 30,000,000
        return getNthNumber(startingNumbers, 30000000);
    }
    public static void main(String[] args) {
        System.out.println(String.format(
            "A. the 2020th number spoken will be %d",
            getAnswerA(parseStartingNumbers(args[0]))));
        System.out.println(String.format(
            "A. the 30000000th number spoken will be %d",
            getAnswerB(parseStartingNumbers(args[0]))));
    }
    
}
