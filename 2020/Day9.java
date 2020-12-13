import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class Day9 {
    public static int getAnswerA(String filepath, int preambleSize) throws IOException {
        return getFirstInvalidNumber(filepath, preambleSize);
    }

    public static int getFirstInvalidNumber(String filepath, int preambleSize) throws IOException {
        try(BufferedReader reader = new BufferedReader(new FileReader(filepath))) {
            String line = reader.readLine();
            // preamble is a circular buffer
            int[] preamble = new int[preambleSize];
            int lineIndex = 0;
            while(line != null) {
                int number = Integer.valueOf(line);
                if(lineIndex >= preambleSize && 
                    ! numberIsValid(preamble, number)) {
                    return number;
                }

                // add to the preamble as a circular buffer
                preamble[lineIndex % preambleSize] = number;
                lineIndex ++;

                line = reader.readLine();
            }
        }
        return -1;
    }

    public static boolean numberIsValid(int[] preamble, int number) {
        // we must find two numbers in the preamble which add
        // up to this
        for(int i=0; i<preamble.length; i++) {
            int searchFor = number - preamble[i];
            for(int j=i+1; j<preamble.length; j++) {
                if(preamble[j] == searchFor) return true;
            }
        }
        return false;

    }

    public static long getAnswerB(String filepath, int preambleSize) throws IOException {

        // load all the numbers
        List<Long> numbers = new ArrayList<>();
        try(BufferedReader reader = new BufferedReader(new FileReader(filepath))) {
            String line = reader.readLine();
            
            while(line != null) {
                numbers.add(Long.valueOf(line));
                line = reader.readLine();
            }
        }

        // now find a sliding window
        int incorrectNumber = getFirstInvalidNumber(filepath, preambleSize);
        int sum = 0;
        int left = 0, right = 0;
        for(int i=0; i<numbers.size(); i++) {
            long num = numbers.get(i);
            sum += num;
            right = i;
            System.out.println(String.format("left=%d right=%d i=%d sum=%d", left, right, num, sum));
            if(num == incorrectNumber) continue;
            if(sum == incorrectNumber) break;
            while(sum > incorrectNumber && left < numbers.size()) {
                // we need to remove the first number
                sum -= numbers.get(left);                
                left ++;
                if(sum == incorrectNumber) break;
            }
            if(sum == incorrectNumber) break;
        }

        
        System.out.println(String.format("left=%d right=%d", left, right));

        if(left >= right) return -1;
        
        // now find the smallest and larget in this range
        long min = Long.MAX_VALUE, max = Long.MIN_VALUE;
        for(int i=left; i<=right; i++) {
            min = Math.min(min, numbers.get(i));
            max = Math.max(max, numbers.get(i));
        }
        System.out.println(String.format("min=%d max=%d", min, max));
        return min + max;
    }

    public static void main(String[] args) throws IOException {
        int preambleSize = 25;
        if(args.length > 1) {
            preambleSize = Integer.valueOf(args[1]);
        }

        System.out.println("using preamble size " + preambleSize);

        System.out.println(String.format(
            "A. The first number that does not have this property is %d",
            getAnswerA(args[0], preambleSize)
        ));
        System.out.println(String.format(
            "A. the encryption weakness in my XMAS-encrypted list of numbers is %d",
            getAnswerB(args[0], preambleSize)
        ));
    }
    
}
