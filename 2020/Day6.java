import java.io.*;
import java.util.*;
import java.util.stream.Collectors;

public class Day6 {
    public static int getAnswerB(String filepath) throws IOException {
        int sum = 0;
        int groupCount = 0;
        Map<Character, Integer> characters = new HashMap<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(filepath))) {
            String line = reader.readLine();
            while(line != null) {
                if(line.equals("")) {
                    int count = 0;
                    for(int questionCount: characters.values()) {
                        if(questionCount == groupCount) count++;
                    }
                    sum += count;
                    // System.out.println("groupCount=" + groupCount + " sum=" + sum + " items="
                    //     + characters.entrySet().stream()
                    //         .map((e) -> String.format("%c=%d", e.getKey(), e.getValue()))
                    //         .collect(Collectors.joining(", "))
                    //     );
                    groupCount = 0;
                    characters.clear();
                } else {

                    groupCount++;
                    for(char question: line.toCharArray()) {
                        characters.put(question, characters.getOrDefault(question, 0) + 1);
                    }
                }
                line = reader.readLine();
            }
        }

        if(characters.size() > 0) {
            int count = 0;
            for(int questionCount: characters.values()) {
                if(questionCount == groupCount) count++;
            }
            sum += count;
        }

        return sum;
    }
    public static int getAnswerA(String filepath) throws IOException {
        int sum = 0;
        Set<Character> characters = new HashSet<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(filepath))) {
            String line = reader.readLine();
            while(line != null) {
                if(line.equals("")) {
                    int count = characters.size();
                    sum += count;
                    characters.clear();
                }
                else {

                    for(char question: line.toCharArray()) {
                        characters.add(question);
                    }
                }
                line = reader.readLine();
            }
        }

        if(characters.size() > 0) {
            int count = characters.size();
            sum += count;
        }

        return sum;
    }
    public static void main(String[] args) throws IOException {
        String filepath = args[0];
        System.out.println("A. The sum of the yes answers is " + getAnswerA(filepath));
        System.out.println("B. The sum of the yes answers is " + getAnswerB(filepath));
    }
    
}
