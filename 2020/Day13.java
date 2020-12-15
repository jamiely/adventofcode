import java.io.IOException;
import java.nio.file.*;
import java.util.stream.Collectors;
import java.util.*;

public class Day13 {
    public static long getAnswerA(long timestamp, List<Integer> buses) {
        int earliestBus = -1;
        long minWait = Long.MAX_VALUE;
        for(int bus: buses) {
            long multiplier = (long) Math.floor((double) timestamp / bus) + 1;
            long nextTimestamp = bus * multiplier;
            long wait = nextTimestamp - timestamp;
            if(wait >= minWait) continue;

            earliestBus = bus;
            minWait = wait;
        }

        if(earliestBus == -1) {
            System.out.println("There was a problem!");
            return -1;
        }

        return earliestBus * minWait;
    }

    // references for chinese remainder theorem:
    // https://brilliant.org/wiki/chinese-remainder-theorem/
    // https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
    // https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
    // https://www.geeksforgeeks.org/chinese-remainder-theorem-set-2-implementation/
    // https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#See_also
    // https://en.wikipedia.org/wiki/Chinese_remainder_theorem
    public static long getAnswerB(List<Integer> constraints) {
        // // 7,13,x,x,59,x,31,19

        // // timestamp % 7  == 0 => timestamp === 0 (mod 7)
        // // (timestamp + 1) % 13 == 0 or timestamp % 13 == (13 - 1) => timestamp === 12 (mod 13)
        // // (timestamp + 4) % 59 == 0 or timestamp % 59 == (59 - 4) => timestamp === 55 (mod 59)
        // // (timestamp + 6) % 31 == 0 or timestamp % 31 == (31 - 6) => timestamp === 25 (mod 31)
        // // (timestamp + 7) % 19 == 0 or timestamp % 19 == (19 - 7) => timestamp === 12 (mod 19)
        // // N = 7 * 13 * 59 * 31 * 19 = 3162341

        // long upperBound = 1;

        // // y1 = N/7, y2=N/13
        // // gcd(7, 13) = 1
        // // 7x + 13b = 1
        // // 7x === 1 (mod 13)
        // // (7x - 1) % 13 == 0
        long N = 1;

        List<int[]> shortContraints = new ArrayList<>();
        for(int i=0; i<constraints.size(); i++) {
            int bus = constraints.get(i);
            if(bus == -1) continue;

            N *= bus;

            shortContraints.add(new int[]{i, bus});
        }
        System.out.println("N=" + N);
        int[] a = new int[shortContraints.size()];
        long[] y = new long[shortContraints.size()];
        long[] z = new long[shortContraints.size()];
        long sum = 0;
        for(int i=0; i<y.length; i++) {
            int index = shortContraints.get(i)[0];
            int bus = shortContraints.get(i)[1];
            a[i] = bus - index;

            y[i] = N / bus;
            GCD.Result result = GCD.extendedGCD(y[i], bus);
            z[i] = result.getInverse();

            long thisSum = a[i] * y[i] * z[i];
            System.out.println(String.format(
                "%d (bus=%d): %d*%d*%d=%d",
                index, bus, a[i], y[i], z[i], thisSum
            ));
            sum += thisSum;
        }

        return sum % N;
    }

    public static void main(String[] args) throws IOException {
        List<String> lines = Files.readAllLines(Paths.get(args[0]));
        long timestamp = Integer.valueOf(lines.get(0));
        List<Integer> buses = Arrays.asList(lines.get(1).split(","))
            .stream()
            .map(s -> s.equals("x") ? -1 : Integer.valueOf(s))
            .collect(Collectors.toList());

        List<Integer> busesWithoutX = buses
            .stream()
            .filter(x -> x != -1)
            .collect(Collectors.toList());

        System.out.println(String.format(
            "A. the ID of the earliest bus I can take to the airport multiplied \n" + 
            "   by the number of minutes you'll need to wait for that bus is %d",
            getAnswerA(timestamp, busesWithoutX)
        ));
        System.out.println(String.format(
            "B. the earliest timestamp such that all of the listed bus IDs depart \n" + 
            "   at offsets matching their positions in the list is %d",
            getAnswerB(buses)
        ));
    }
    
}
