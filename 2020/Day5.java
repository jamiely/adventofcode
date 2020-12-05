import java.io.*;
import java.util.*;

public class Day5 {
    public static int getBSPValue(String entries, int min, int max) {
        for(char c: entries.toCharArray()) {
            int midpoint = (max + min) / 2;
            if(c == 'F' || c == 'L') {
                max = midpoint;
            }
            else if(c == 'B' || c == 'R') {
                min = midpoint + 1;
            }
            else {
                return -1;
            }
            // System.out.println(String.format("step min=%d max=%d", min, max));
            if(min == max) return min;
        }
        System.out.println(String.format("Did not find single value min=%d max=%d", min, max));
        return -1;
    }

    public static int getSeatId(int row, int col) {
        return row * 8 + col;
    }

    public static int[] getSeatRowAndCol(String bp) {
        int row = getBSPValue(bp.substring(0, 7), 0, 127);
        int col = getBSPValue(bp.substring(7, 10), 0, 7);

        return new int[]{row, col};
    }

    public static int getSeatId(String bp) {
        int[] rowAndCol = getSeatRowAndCol(bp);
        int row = rowAndCol[0];
        int col = rowAndCol[1];
        return getSeatId(row, col);
    }

    public static void outputExamplesA() {
        Map<String, Integer> examples = new HashMap<>();
        examples.put("FBFBBFFRLR", 357);
        examples.put("BFFFBBFRRR", 567);
        examples.put("FFFBBBFRRR", 119);
        examples.put("BBFFBBFRLL", 820);

        for(Map.Entry<String, Integer> entry: examples.entrySet()) {
            int seat = getSeatId(entry.getKey());
            boolean matches = seat == entry.getValue();

            System.out.println(String.format(
                "Boarding pass %s should have seat id %d. Actual is %d. %s",
                entry.getKey(), entry.getValue(), seat,
                matches ? "PASS": "FAIL"));
        }
    }

    public static int getAnswerA(String filepath) throws IOException {
        int max = -1;
        try(BufferedReader reader = new BufferedReader(new FileReader(filepath))) {
            String line = reader.readLine();
            while(line != null) {
                max = Math.max(getSeatId(line), max);
                line = reader.readLine();
            }
        }
        
        return max;
    }

    public static int getAnswerB(String filepath) throws IOException {
        int[][] seats = new int[128][8];

        for(int r=0; r<=127; r++) {
            Arrays.fill(seats[r], 0);
        }

        try(BufferedReader reader = new BufferedReader(new FileReader(filepath))) {
            String line = reader.readLine();
            while(line != null) {
                int[] rAndC = getSeatRowAndCol(line);
                int r = rAndC[0], c = rAndC[1];
                seats[r][c] = 1; // taken
                line = reader.readLine();
            }
        }

        // now build a lookup table of seat ids
        List<Integer> missingSeatIds = new ArrayList<>();
        Map<Integer, int[]> seatIdToIndex = new HashMap<>();
        for(int r=0; r<=127; r++) {
            for(int c =0; c<=7; c++) {
                if(seats[r][c] != 0) continue;

                int seatId = getSeatId(r, c);
                missingSeatIds.add(seatId);
                seatIdToIndex.put(seatId, new int[]{r, c});
            }
        }

        Collections.sort(missingSeatIds);
        int last = -1;
        int last2 = -1;
        int found = -1;
        for(int seat: missingSeatIds) {
            if(last != last2 + 1 && last != seat - 1) {
                found = last;
            }
            last2 = last;
            last = seat;
        }

        return found;
    }

    public static String formatIndex(int[] rc) {
        return String.format("(r=%d, c=%d)", rc[0], rc[1]);
    }

    public static void main(String[] args) throws IOException {
        outputExamplesA();
        System.out.println("A. The highest seat ID is " + getAnswerA(args[0]));
        System.out.println("B. Our seat ID is " + getAnswerB(args[0]));
    }
    
}
