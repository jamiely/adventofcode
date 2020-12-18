import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.stream.Collectors;

public class Day17b {
    public static class Change {
        public int x;
        public int y;
        public int z;
        public int w;
        public boolean isActive;

        public Change(int x, int y, int z, int w, boolean isActive) {
            this.x = x; this.y = y; this.z = z; this.w = w;
            this.isActive = isActive;
        }
    }

    public static class PocketDimension {
        private Map<String, Character> data = new HashMap<>();
        public int minX = 0, maxX = 0, 
            minY = 0, maxY = 0, 
            minZ = 0, maxZ = 0,
            minW = 0, maxW = 0;


        public void set(int x, int y, int z, int w, boolean isActive) {
            String key = getCoordKey(x, y, z, w);
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
            minW = Math.min(minW, w);
            maxW = Math.max(maxW, w);

            data.put(key, '#');
        }

        public boolean isActive(int x, int y, int z, int w) {
            String key = getCoordKey(x, y, z, w);
            return data.getOrDefault(key, '.') == '#';
        }

        private String getCoordKey(int x, int y, int z, int w) {
            return String.format("(%d, %d, %d, %d)", x, y, z, w);
        }

        public int countActiveNeighbors(int x, int y, int z, int w) {
            int[] delta = new int[] { -1, 0, 1};
            int count = 0;
            for(int i: delta) {
                for(int j: delta) {
                    for(int k: delta) {
                        for(int l: delta) {
                            // skip this b/c it is the point itself
                            if(i == 0 && j == 0 && k == 0 && l == 0) continue;
                            if(isActive(x + i, y + j, z + k, w + l)) count ++;
                        }
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
            StringBuffer sbExt = new StringBuffer();
            for(int w=minW; w<=maxW; w++) {
                for(int z=minZ; z<=maxZ; z++) {
                    StringBuffer sb = new StringBuffer();
                    boolean hadOneActive = false;
                    sb.append("z=");
                    sb.append(z);
                    sb.append(", w=");
                    sb.append(w);
                    sb.append("\n");
                    for(int y=maxY; y>=minY; y--) {
                        StringBuffer sbRow = new StringBuffer();
                        boolean hadOneActiveInRow = false;
                        for(int x=minX; x<=maxX; x++) {
                            boolean active = isActive(x, y, z, w);
                            hadOneActive = hadOneActive || active;
                            hadOneActiveInRow = hadOneActiveInRow || active;
                            sbRow.append(active ? '#' : '.');
                        }
                        if(hadOneActiveInRow) {
                            sb.append(sbRow);
                            sb.append("\n");
                        }
                    }
                    sb.append("\n");
                    if(hadOneActive) {
                        sbExt.append(sb);
                    }
                }
            }
            return sbExt.toString();
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
                dimension.set(j, rowCount - i, 0, 0,
                    strs.get(i).charAt(j) == '#');
            }
        }
        return dimension;
    }
    public static int getAnswerB(PocketDimension dimension, int n) {
        System.out.println("Before any cycles:\n" + dimension);

        for(int i=1; i<=n; i++) {
            step(dimension);

            if(i <= 2) {
                System.out.println("After " + i + " cycles:\n" + dimension);
            }
            else {
                System.out.println("Cycle " + i);
            }
        }
        return dimension.countActive();
    }
    public static void step(PocketDimension dimension) {
        List<Change> changes = new ArrayList<>();

        for(int x=dimension.minX - 1; x<=dimension.maxX + 1; x++) {
            for(int y=dimension.minY - 1; y<=dimension.maxY + 1; y++) {
                for(int z=dimension.minZ - 1; z <= dimension.maxZ + 1; z++) {
                    for(int w=dimension.minW - 1; w <= dimension.maxW + 1; w++) {
                        int activeNeighborCount = dimension.countActiveNeighbors(x, y, z, w);
                        if(dimension.isActive(x, y, z, w)) {
                            if(activeNeighborCount == 2) continue;
                            if(activeNeighborCount == 3) continue;

                            changes.add(new Change(x, y, z, w, false));
                        }
                        else { // inactive
                            if(activeNeighborCount != 3) continue;

                            changes.add(new Change(x, y, z, w, true));
                        }
                    }
                }
            }
        }

        // now apply changes
        for(Change c: changes) {
            dimension.set(c.x, c.y, c.z, c.w, c.isActive);
        }
    }

    public static void main(String[] args) throws IOException {
        List<String> gridStrs = parseGrid(args[0]);
        PocketDimension dimension = getDimension(gridStrs);
        System.out.println("B. After the sixth cycle, " 
           + getAnswerB(dimension, 6) + " cubes are left in the active state.");
    }
    
}
