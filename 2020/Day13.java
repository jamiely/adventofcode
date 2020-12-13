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

    public static void main(String[] args) throws IOException {
        List<String> lines = Files.readAllLines(Paths.get(args[0]));
        long timestamp = Integer.valueOf(lines.get(0));
        List<Integer> buses = Arrays.asList(lines.get(1).split(","))
            .stream()
            .filter(x -> ! x.equals("x"))
            .map(Integer::valueOf)
            .collect(Collectors.toList());
        System.out.println(String.format(
            "A. the ID of the earliest bus I can take to the airport multiplied \n" + 
            "by the number of minutes you'll need to wait for that bus is %d",
            getAnswerA(timestamp, buses)
        ));
    }
    
}
