import java.io.*;

public class Day3 {
    public static int getNumberOfTreesHit(String filename, int right, int down) throws Exception {
        BufferedReader reader = new BufferedReader(new FileReader(filename));
        String line = reader.readLine();
        int treeCount = 0;
        int currentXPosition = 0;
        while(line != null) {
            currentXPosition = (currentXPosition + right) % line.length();
            
            for(int i=0; i<down; i++) {
                line = reader.readLine();
                if(line == null) break;
            }

            if(line == null) break;
            if(line.charAt(currentXPosition) != '#') continue;

            treeCount++;
        }
        reader.close();
        return treeCount;
    }

    public static long getAnswerB(String filepath) throws Exception {
        int[][] slopes = new int[][] {
            new int[] {1,1},
            new int[] {3,1},
            new int[] {5,1},
            new int[] {7,1},
            new int[] {1,2}
        };
        long product = 1;
        for(int[] slope: slopes) {
            int trees = getNumberOfTreesHit(filepath, slope[0], slope[1]);
            System.out.println(String.format("right=%d down=%d tree count %d", slope[0], slope[1], trees));
            product *= trees;
        }
        return product;
    }

    public static void main(String[] args) throws Exception {
        int treeCount = getNumberOfTreesHit(args[0], 3, 1);
        System.out.println(String.format("a. We'd hit %d trees.", treeCount));
        System.out.println(String.format("b. The product of all the trees we'd hit is %d.", getAnswerB(args[0])));
    }    
}
