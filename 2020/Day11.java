import java.io.*;
import java.nio.file.*;
import java.util.List;

public class Day11 {
    public static class SeatResolver {
        public int maxSeatsOccupiedBeforeLeaving = 4;

        public char resolveIndex(char[][] layout, int r, int c) {
            char entry = layout[r][c];
            if(entry == 'L') {
                if(countOccupiedSeatsAdjacent(layout, r, c) == 0) return '#';
            }
            else if(entry == '#') {
                if(countOccupiedSeatsAdjacent(layout, r, c) >= maxSeatsOccupiedBeforeLeaving) {
                    // System.out.println("more than 4");
                    return 'L';
                }
            }

            return entry;
        }

        public int countOccupiedSeatsAdjacent(char[][] layout, int r, int c) {
            int seatCount = 0;
            for(int i=-1; i<=1; i++) {
                for(int j=-1; j<=1; j++) {
                    if(i==0 && j==0) continue;

                    if(i + r < 0) continue;
                    if(i + r >= layout.length) continue;
                    if(j + c < 0) continue;
                    if(j + c >= layout[0].length) continue;

                    if(layout[i + r][j + c] == '#') seatCount++;
                }
            }
            return seatCount;
        }

    }

    public static class SeatResolverB extends SeatResolver {
        static int[][] directions = new int[][] {
            new int[] { -1, -1 },
            new int[] { -1, 0 },
            new int[] { -1, 1 },
            new int[] { 0, -1 },
            new int[] { 0, 1 },
            new int[] { 1, -1 },
            new int[] { 1, 0 },
            new int[] { 1, 1 }
        };

        public int countOccupiedSeatsAdjacent(char[][] layout, int r, int c) {
            int seatCount = 0;
            for(int[] direction: directions) {
                int di = direction[0], dj = direction[1];
                int i=di, j=dj;
                while(true) {
                    if(i + r < 0) break;
                    if(i + r >= layout.length) break;
                    if(j + c < 0) break;
                    if(j + c >= layout[0].length) break;
                    if(layout[i + r][j + c] == 'L') break;
                    if(layout[i + r][j + c] == '#') {
                        seatCount++;
                        break;
                    }

                    i+=di;
                    j+=dj;
                }
            }
            return seatCount;
        }
    }

    public static char[][] copyArray(char[][] layout) {
        char [][] copy = new char[layout.length][layout[0].length];

        for(int i=0; i<layout.length; i++)
            for(int j=0; j<layout[0].length; j++)
                copy[i][j] = layout[i][j];

        return copy;
    }

    public static void printBoard(char[][] layout) {
        StringBuffer sb = new StringBuffer();
        for(char[] row: layout) {
            sb.append(String.valueOf(row));
            sb.append("\n");
        }
        System.out.println(sb);
    }
    public static int getAnswerA(char[][] layout) {
        char[][] last = copyArray(layout), current = copyArray(layout);
        // System.out.println("Initial board");
        // printBoard(current);
        int changes = 1;
        int rounds = 0;
        SeatResolver resolver = new SeatResolver();
        while(changes > 0) {
            changes = resolveRules(last, current, resolver);

            // System.out.println("Current board");
            // printBoard(current);
            // System.out.println("Continue?");
            // System.console().readLine();

            // swap the arrays now. this allows us to avoid using extra memory
            char[][] tmp = current;
            current = last;
            last = tmp;

            rounds ++;            
        }

        System.out.println("Completed in " + rounds + " rounds.");

        return countSeats(current, '#');
    }

    public static int getAnswerB(char[][] layout) {
        char[][] last = copyArray(layout), current = copyArray(layout);
        // System.out.println("Initial board");
        // printBoard(current);
        int changes = 1;
        int rounds = 0;
        SeatResolver resolver = new SeatResolverB();
        resolver.maxSeatsOccupiedBeforeLeaving = 5;
        while(changes > 0) {
            changes = resolveRules(last, current, resolver);

            // System.out.println("Current board");
            // printBoard(current);
            // System.out.println("Continue?");
            // System.console().readLine();

            // swap the arrays now. this allows us to avoid using extra memory
            char[][] tmp = current;
            current = last;
            last = tmp;

            rounds ++;            
        }

        System.out.println("Completed in " + rounds + " rounds.");

        return countSeats(current, '#');
    }

    public static int countSeats(char[][] layout, char c) {
        int sum = 0;
        for(char[] row: layout)
            for(char seat: row)
                if(c == seat) sum++;
        return sum;
    }

    public static int resolveRules(char[][] last, char[][] current, SeatResolver resolver) {
        int changes = 0;
        for(int i=0; i<last.length; i++) {
            for(int j=0; j<last[0].length; j++) {
                char newEntry = resolver.resolveIndex(last, i, j);
                current[i][j] = newEntry;

                if(newEntry == last[i][j]) continue;
                // System.out.println(String.format("%d,%d changed from %c to %c",
                //     i, j, last[i][j], newEntry));
                changes++;
            }
        }
        return changes;
    }

    public static void main(String[] args) throws IOException {
        char[][] seatLayout = getInput(args[0]);
        System.out.println(String.format(
            "A. when no seats change, %d seats end up occupied.",
            getAnswerA(seatLayout)
        ));
        System.out.println(String.format(
            "B. when no seats change, and we change the rules for occupied seats, %d seats end up occupied.",
            getAnswerB(seatLayout)
        ));
    }
    public static char[][] getInput(String filepath) throws IOException {
        List<String> lines = Files.readAllLines(Paths.get(filepath));
        return lines.stream().map(String::toCharArray).toArray(char[][]::new);
    }   
}
