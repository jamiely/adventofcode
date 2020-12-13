import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;

public class Day7 {
    public static class Graph {
        List<String> nodes = new ArrayList<>();
        Map<String, Integer> nodeIndicesByName = new HashMap<>();
        List<List<Integer>> edges = new ArrayList<>();

        public String getName(int index) {
            return nodes.get(index);
        }

        public int addNode(String name) {
            if(nodeIndicesByName.containsKey(name)) {
                return nodeIndicesByName.get(name);
            }

            nodes.add(name);
            int index = nodes.size() - 1;
            nodeIndicesByName.put(name, index);
            edges.add(new ArrayList<>());
            for(List<Integer> list: edges) {
                while(list.size() < nodes.size()) list.add(0);
            }
            return index;
        }

        public void setEdge(int a, int b, int weight) {
            edges.get(a).set(b, weight);
        }

        public int getEdgeWeight(int a, int b) {
            return edges.get(a).get(b);
        }
    }

    static Pattern edgePattern = Pattern.compile("^(?<colorChildCount>\\d+) (?<colorChild>[\\w ]+) bags?");
    public static void parseEdges(Graph g, int nodeIndex, String edgeList) {
        for(String edgeStr: edgeList.split(", ")) {
            if(edgeStr.equals("no other bags.")) continue;
            Matcher matcher = edgePattern.matcher(edgeStr);
            if(! matcher.find()) {
                System.out.println("Could not find edge in " + edgeStr);
                continue;
            }
            int count = Integer.valueOf(matcher.group("colorChildCount"));
            String color = matcher.group("colorChild");
            int childIndex = g.nodeIndicesByName.containsKey(color) ?
                g.nodeIndicesByName.get(color) :
                g.addNode(color);

            g.setEdge(nodeIndex, childIndex, count);
        }
    }

    static Pattern linePattern = Pattern.compile("^(?<colorParent>[\\w ]+) bags contain (?<edgeList>.+)$");
    public static Graph loadGraph(String filepath) throws IOException {
        Graph graph = new Graph();
        for(String line: Files.readAllLines(Paths.get(filepath))) {
            Matcher matcher = linePattern.matcher(line);
            if(! matcher.find()) {
                System.out.println("Didn't find match in: " + line);
                continue;
            }
            String colorParent = matcher.group("colorParent");
            int nodeId = graph.addNode(colorParent);

            parseEdges(graph, nodeId, matcher.group("edgeList"));
        }
        return graph;
    }

    public static int getAnswerB(String filepath) throws IOException {
        Graph g = loadGraph(filepath);
        int targetColorNodeIndex = g.nodeIndicesByName.get("shiny gold");
        return recursiveCount(g, targetColorNodeIndex);
    }

    public static int recursiveCount(Graph g, int index) {
        // System.out.println(g.getName(index));
        int sum = 0;
        for(int i=0; i<g.edges.get(index).size(); i++) {
            int weight = g.getEdgeWeight(index, i);
            if(weight <= 0) continue;

            int result = recursiveCount(g, i);
            int iter = weight * (result + 1);
            // System.out.println(String.format("%s --> %s = %d * (%d + 1) = %d",
            //     g.getName(index), g.getName(i), weight, result, iter));
            sum += iter;
        }
        return sum;
    }

    public static int getAnswerA(String filepath) throws IOException {
        Graph g = loadGraph(filepath);

        int targetColorNodeIndex = g.nodeIndicesByName.get("shiny gold");


        Set<Integer> visited = new HashSet<>();
        Deque<Integer> toVisit = new ArrayDeque<>();
        Set<Integer> canContain = new HashSet<>();

        // first determine what directly contains shiny gold
        // for(int i=0; i<g.edges.size(); i++) {
        //     if(g.getEdgeWeight(i, targetColorNodeIndex) > 0) {
        //         count++;
        //         toVisit.add(i);
        //     }
        // }
        toVisit.add(targetColorNodeIndex);

        // now we use BFS to search these nodes
        while(! toVisit.isEmpty()) {
            int current = toVisit.removeFirst();
            if(visited.contains(current)) continue;

            for(int i=0; i<g.edges.size(); i++) {
                if(g.getEdgeWeight(i, current) > 0) {
                    canContain.add(i);
                    // System.out.println(String.format("%s can contain %s",
                    //     g.getName(i), g.getName(current)));
                    toVisit.add(i);
                }
            }
            visited.add(current);
        }

        return canContain.size();
    }


    public static void main(String[] args) throws Exception {
        System.out.println(String.format(
            "A. %d bag colors can contain one shiny gold bag",
            getAnswerA(args[0])
        ));
        System.out.println(String.format(
            "B. a shiny gold bag must contain %d other bags",
            getAnswerB(args[0])
        ));
    }    
}
