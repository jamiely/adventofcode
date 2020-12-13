import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.stream.Collectors;

public class Day10 {
    public static int getAnswerA(List<Integer> nums) {
        // your device's built-in joltage adapter
        nums.add(nums.get(nums.size() - 1) + 3);

        int lastNumber = 0;
        int[] diffCount = new int[4];
        Arrays.fill(diffCount, 0);
        for(int i=0; i<nums.size(); i++) {
            int diff = nums.get(i) - lastNumber;
            diffCount[diff] ++;

            lastNumber = nums.get(i);
        }   

        return diffCount[1] * diffCount[3];
    }
    public static long getAnswerB(List<Integer> originalNums) {
        /**
         * Number of ways to arrange 1 adapter is 2 (if z is 3 or less from start) (1 unique)
         * a -> b -> z
         * a -> z
         * 
         * Number of ways to arrange 2 adapters is 4 (2 unique)
         * a -> b -> c -> z
         * a -> c -> z
         * a -> b -> z # this one is repeated above
         * a -> z # this one is repeated above
         * 
         * Number of ways to arrange 3 adapters is 8 (4 unique)
         * a -> b -> c -> d -> z
         * a -> b -> d -> z
         * a -> c -> d -> z
         * a -> d -> z
         * a -> b -> c -> z # repeated in previous section
         * a -> c -> z # repeated in previous section
         * a -> b -> z # repeated in first section
         * a -> z # this one is repeated above
         * 
         * Sliding window. How many combinations end with that number. (not
         * including endings)
         * 
         *      1    2
         * a -> b -> c -> d -> e -> f -> g -> h -> i -> j -> k ->z
         */
        List<Integer> nums = new ArrayList<>();
        nums.add(0);
        nums.addAll(originalNums);
        nums.add(nums.get(nums.size() - 1) + 3);

        // we will keep the count of each adapter ending at that point
        long[] counts = new long[nums.size()];
        // this is the number of adapters that can be reached from the
        // adapter i.
        long innerCount = 1;

        for(int i = 1; i < nums.size(); i++) {
            counts[i - 1] = innerCount;
            innerCount = 0;

            int num = nums.get(i);

            
            // we always assume that the configuration of adapters that
            // includes the previous number will work. 
            innerCount += counts[i - 1];

            if(i < 2) continue;
            int beforePreviousNumber = nums.get(i - 2);
            if(num - beforePreviousNumber <= 3) {
                // then we can remove the previous number
                // and add all combinations of the previous number
                // (because we will just append the current adapter)
                innerCount += counts[i - 2];
            }

            if(i < 3) continue;
            int twoBeforeNumber = nums.get(i - 3);
            if(num - twoBeforeNumber <= 3) {
                // then we can remove both previous numbers
                innerCount += counts[i - 3];
            }
        }
        counts[counts.length - 1] = innerCount;

        // StringBuffer sb = new StringBuffer();
        // for(int n: nums) {
        //     sb.append(n);
        //     sb.append(" -> ");
        // }
        // sb.append("\n");
        // for(int c: counts) {
        //     sb.append(c);
        //     sb.append(" -> ");
        // }
        // System.out.println(sb);

        return counts[counts.length - 1];
    }

    public static void main(String[] args) throws IOException {
        List<Integer> nums = Files.readAllLines(Paths.get(args[0])).stream()
            .map(Integer::valueOf)
            .collect(Collectors.toList());

        nums.sort(Integer::compare);

        

        System.out.println(String.format(
            "A. the number of 1-jolt differences multiplied by the number of 3-jolt differences is %d",
            getAnswerA(nums)
        ));

        System.out.println(String.format(
            "B. the total number of distinct ways you can arrange the adapters to connect the charging outlet to my device is %d", 
            getAnswerB(nums)));
        
    }
    
}

// 1, 2, 3, 4, 6, 7, 8, 9, 10, 13

// 1, 2, 3, 4, 6, 8, 9, 10, 13
// 1, 2, 3, 4, 6, 7, 9, 10, 13

// 1, 2, 3, 6, 7, 8, 9, 10, 13
// 1, 2, 4, 6, 7, 8, 9, 10, 13

// 1, 3, 6, 7, 8, 9, 10, 13