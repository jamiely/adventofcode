import java.util.*;
import java.util.stream.Collectors;

public class Day15 {
    public static int getNthNumber(List<Integer> startingNumbers, int n) {
        Map<Integer, Integer> memLastTurn = new HashMap<>();
        Map<Integer, Integer> memLastTurn2 = new HashMap<>();

        int turn = 1;
        int last = -1;
        for(int i=0; i<startingNumbers.size(); i++, turn++) {
            int num = startingNumbers.get(i);
            if(memLastTurn.containsKey(num)) {
                memLastTurn2.put(num, memLastTurn.get(num));
            }
            memLastTurn.put(num, turn);
            last = num;
        }

        for(; turn<=n; turn++) {
            if(memLastTurn2.containsKey(last)) {
                int lastTurn = memLastTurn2.get(last);
                int diff = turn - lastTurn - 1;
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
        }
        return last;
    }

    protected static List<Integer> parseStartingNumbers(String list) {
        return Arrays.asList(list.split(","))
            .stream()
            .map(Integer::valueOf)
            .collect(Collectors.toList());
    }

    public static int getAnswerA(List<Integer> startingNumbers) {
        return getNthNumber(startingNumbers, 2020);
    }
    public static void main(String[] args) {
        System.out.println(String.format(
            "A. the 2020th number spoken will be %d",
            getAnswerA(parseStartingNumbers(args[0]))));
    }
    
}
