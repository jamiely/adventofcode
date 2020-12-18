import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.stream.Collectors;

public class Day17 {
    public static class Change {
        public int x;
        public int y;
        public int z;
        public boolean isActive;

        public Change(int x, int y, int z, boolean isActive) {
            this.x = x; this.y = y; this.z = z; this.isActive = isActive;
        }
    }

    public static class PocketDimension {
        private Map<String, Character> data = new HashMap<>();
        public int minX = 0, maxX = 0, minY = 0, maxY = 0, minZ = 0, maxZ = 0;


        public void set(int x, int y, int z, boolean isActive) {
            String key = getCoordKey(x, y, z);
            if(! isActive) {
                data.remove(key);
                return;
            }

            minX = Math.min(minX, x);
            maxX = Math.max(maxX, x);
            minY = Math.min(minY, y);
            maxY = Math.max(maxY, y);
            minZ = Math.min(minZ, z);
            maxZ = Math.max(maxZ, z);

            data.put(key, '#');
        }

        public boolean isActive(int x, int y, int z) {
            String key = getCoordKey(x, y, z);
            return data.getOrDefault(key, '.') == '#';
        }

        private String getCoordKey(int x, int y, int z) {
            return String.format("(%d, %d, %d)", x, y, z);
        }

        public int countActiveNeighbors(int x, int y, int z) {
            int[] delta = new int[] { -1, 0, 1};
            int count = 0;
            for(int i: delta) {
                for(int j: delta) {
                    for(int k: delta) {
                        if(i == 0 && j == 0 && k == 0) continue;
                        if(isActive(x + i, y + j, z + k)) count ++;
                    }
                }
            }
            return count;
        }

        public int countActive() {
            int count = 0;
            for(Character c: data.values()) {
                if(c == '#') count++;
            }
            return count;
        }

        public String toString() {
            StringBuffer sb = new StringBuffer();
            for(int z=minZ; z<=maxZ; z++) {
                sb.append("z=");
                sb.append(z);
                sb.append("\n");
                for(int y=maxY; y>=minY; y--) {
                    for(int x=minX; x<=maxX; x++) {
                        sb.append(isActive(x, y, z) ? '#' : '.');
                    }
                    sb.append("\n");
                }
                sb.append("\n");
            }
            return sb.toString();
        }
    }
    public static List<String> parseGrid(String filepath) throws IOException {
        return Files.readAllLines(Paths.get(filepath))
            .stream()
            .filter(s -> ! s.isEmpty())
            .collect(Collectors.toList());
    }

    public static PocketDimension getDimension(List<String> strs) {
        PocketDimension dimension = new PocketDimension();
        int rowCount = strs.size();
        for(int i=0; i<rowCount; i++) {
            for(int j=0; j<strs.get(0).length(); j++) {
                dimension.set(j, rowCount - i, 0, strs.get(i).charAt(j) == '#');
            }
        }
        return dimension;
    }
    public static int getAnswerA(PocketDimension dimension, int n) {
        System.out.println("Before any cycles:\n" + dimension);

        for(int i=0; i<n; i++) {
            step(dimension);

            if(i <= 3) {
                System.out.println("After " + (i + 1) + " cycles:\n" + dimension);
            }
        }
        return dimension.countActive();
    }
    public static void step(PocketDimension dimension) {
        List<Change> changes = new ArrayList<>();

        for(int x=dimension.minX - 1; x<=dimension.maxX + 1; x++) {
            for(int y=dimension.minY - 1; y<=dimension.maxY + 1; y++) {
                for(int z=dimension.minZ - 1; z <= dimension.maxZ + 1; z++) {
                    int activeNeighborCount = dimension.countActiveNeighbors(x, y, z);
                    if(dimension.isActive(x, y, z)) {
                        if(activeNeighborCount == 2) continue;
                        if(activeNeighborCount == 3) continue;

                        changes.add(new Change(x, y, z, false));
                    }
                    else { // inactive
                        if(activeNeighborCount != 3) continue;

                        changes.add(new Change(x, y, z, true));
                    }
                }
            }
        }

        // now apply changes
        for(Change c: changes) {
            dimension.set(c.x, c.y, c.z, c.isActive);
        }
    }

    public static void main(String[] args) throws IOException {
        List<String> gridStrs = parseGrid(args[0]);
        PocketDimension dimension = getDimension(gridStrs);
        System.out.println("A. After the sixth cycle, " 
           + getAnswerA(dimension, 6) + " cubes are left in the active state.");
    }
    
}
