import java.io.*;
import java.util.*;
import java.util.regex.*;

public class Day20 {
    public static class Tile {
        public int id = -1;
        public List<String> rows = new ArrayList<>();
        protected List<String> originalSides = null;
        public String toString() {
            StringBuffer sb = new StringBuffer();
            sb.append("Tile ");
            sb.append(id);
            sb.append(":\n");
            for(String row: rows) {
                sb.append(row);
                sb.append("\n");
            }
            return sb.toString();
        }
        public static String reverse(String s) {
            return new StringBuilder(s).reverse().toString();
        }
        protected String getColumn(int column) {
            StringBuilder sb = new StringBuilder();
            for(int i=rows.size()-1; i>=0; i--) {
                sb.append(rows.get(i).charAt(column));
            }
            return sb.toString();
        }
        public List<String> getOriginalSides() {
            if(originalSides != null) {
                return originalSides;
            }
            // everything is from the perspective of looking
            // from outside of the box directly at the side
            List<String> sides = new ArrayList<>();
            int rowLength = rows.get(0).length();
            // top
            sides.add(reverse(rows.get(0)));

            // right
            sides.add(getColumn(rowLength - 1));

            // bottom
            sides.add(rows.get(rows.size() - 1));

            // left
            sides.add(getColumn(0));

            originalSides = sides;

            return sides;
        }

        public Set<String> getSideTranslations() {
            List<String> original = getOriginalSides();
            Set<String> sides = new HashSet<>(original);

            // flip one
            List<String> flipOne = new ArrayList<>(original);
            for(int i=0; i<flipOne.size(); i+=2) {
                flipOne.set(i, reverse(flipOne.get(i)));
            }
            sides.addAll(flipOne);

            List<String> flipTwo = new ArrayList<>(original);
            for(int i=1; i<flipTwo.size(); i+=2) {
                flipTwo.set(i, reverse(flipTwo.get(i)));
            }
            sides.addAll(flipTwo);

            return sides;
        }
    }

    public static long getAnswerA(List<Tile> tiles) {
        List<TileMatch> tileMatches = findTileMatches(tiles);
        Collections.sort(tileMatches, 
            (m1, m2) -> Integer.compare(m1.matchCounts.size(), m2.matchCounts.size()));
        System.out.println("Tile matches:");
        // luckily it seems like there are distinct corner
        // pieces (tiles that match only 2 other tiles).
        // side pieces are also distinct (tiles that match
        // only 3 other tiles)
        TileMatchGroupings groupings = new TileMatchGroupings();
        for(TileMatch match: tileMatches) {
            System.out.println(String.format("%d: %s", match.id, match.matchCounts));
            groupings.add(match);
        }

        long product = 1;

        for(int id: groupings.cornerPieces) {
            product *= id;
        }
        return product;
    }

    private static Pattern patTileId = Pattern.compile("Tile (?<id>[0-9]+):");
    public static int parseTileId(String line){
        Matcher m = patTileId.matcher(line);
        m.find();
        return Integer.valueOf(m.group("id"));
    }

    public static List<Tile> parseTiles(String filepath) throws IOException {
        List<Tile> tiles = new ArrayList<>();
        try(BufferedReader reader = new BufferedReader(new FileReader(filepath))) {
            String line = reader.readLine();
            Tile tile = new Tile();

            while(line != null) {
                if(line.startsWith("Tile")) {
                    tile.id = parseTileId(line);
                }
                else if(line.isEmpty()) {
                    if(tile.id > -1) tiles.add(tile);
                    tile = new Tile();
                }
                else {
                    tile.rows.add(line);
                }
                line = reader.readLine();
            }

        }
        return tiles;
    }

    public static class TileMatch {
        public int id = -1;
        public Map<Integer, Integer> matchCounts = new HashMap<>();
    }

    protected static List<TileMatch> findTileMatches(List<Tile> tiles) {
        List<TileMatch> matches = new ArrayList<>();

        for(Tile tile: tiles) {
            TileMatch match = new TileMatch();
            matches.add(match);
            match.id = tile.id;

            Set<String> tileSides = tile.getSideTranslations();
            for(Tile check: tiles) {
                if(check.id == tile.id) continue;

                Set<String> checkSides = new HashSet<>(check.getSideTranslations());
                checkSides.retainAll(tileSides);
                if(checkSides.isEmpty()) continue;

                match.matchCounts.put(check.id, checkSides.size());
            }
        }

        return matches;
    }

    public static class TileMatchGroupings {
        public List<Integer> cornerPieces = new ArrayList<>();
        public List<Integer> sidePieces = new ArrayList<>();
        public List<Integer> interiorPieces = new ArrayList<>();

        public void add(TileMatch match) {
            int size = match.matchCounts.size();
            switch(size) {
                case 2:
                    cornerPieces.add(match.id);
                    break;
                case 3:
                    sidePieces.add(match.id);
                    break;
                case 4:
                    interiorPieces.add(match.id);
                    break;
                default:
                    throw new IllegalArgumentException("Invalid match count " + size);
            }
        }
    }

    public static void main(String[] args) throws IOException {
        List<Tile> tiles = parseTiles(args[0]);
        System.out.println(tiles.size() + " tiles parsed");
        
        // first, we should try to set the border. first place the corners
        // and see if we can make the sides fit from that. If not, try a
        // different arrangement
        System.out.println("First tile:\n" + tiles.get(0));
        System.out.println("if you multiply together the IDs of the four corner tiles you get " + getAnswerA(tiles));
    }    
}
