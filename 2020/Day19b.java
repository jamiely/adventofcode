import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class Day19b {
    public static class RuleSet {
        public Map<Integer, Rule> rules = new HashMap<>();
        Pattern pattern = null;
        public boolean isMatch(String s) {
            if(pattern == null) {
                pattern = Pattern.compile("^" + getRegex() + "$");
            }
            Matcher m = pattern.matcher(s);
            return m.matches();
        }
        public void addRule(Rule rule) {
            rules.put(rule.getId(), rule);
        }
        public List<Rule> getRuleList() {
            List<Rule> ruleList = new ArrayList<>(rules.values());
            Collections.sort(ruleList, (a, b) -> 
                Integer.compare(a.getId(), b.getId()));
            return ruleList;
        }
        public String toString() {
            return getRuleList().stream().map(Rule::toString)
                .collect(Collectors.joining("\n"));
        }
        public String getRegex(int id) {
            return getRegex(rules.get(id));
        }
        public String getRegex(Rule r) {
            String pattern = "ERROR";

            if(r.getId() == 8) {
                pattern = String.format("(?<eight>%s)+", getRegex(42));
            }
            else if(r.getId() == 11) {

                // this hacky implementation just adds versions oft he patterns up to 10 times
                // needed b/c I used regex for the implementation, and Java's doesn't support
                // recursive expressions https://www.regular-expressions.info/recurse.html.
                // In hindsight, they probably want me to implement some sort of push-down
                // automata for this?
                String r42 = getRegex(42), r31 = getRegex(31);

                List<String> options = new ArrayList<>();
                for(int i=1; i<10; i++) {
                    List<String> parts = new ArrayList<>();
                    for(int j=0; j<i; j++) {
                        parts.add(r42);
                    }
                    for(int j=0; j<i; j++) {
                        parts.add(r31);
                    }
                    options.add(String.format("(?:%s)", String.join("", parts)));
                }
                pattern = String.format("(?:%s)",
                    String.join("|", options));
            }
            else if(r instanceof RuleChar) {
                pattern = getRegexChar((RuleChar) r);
            }
            else if(r instanceof RuleList) {
                pattern = getRegexList((RuleList) r);
            }
            else if(r instanceof RuleOr) {
                pattern = getRegexOr((RuleOr)r );
            }

            
            return pattern;
        }
        public String getRegexChar(RuleChar r) {
            return String.valueOf(r.letter);
        }
        public String getRegexList(RuleList r) {
            return String.format("(?:%s)", r.ruleIds.stream()
                .map(id -> getRegex(rules.get(id)))
                .collect(Collectors.joining("")));
        }
        public String getRegexOr(RuleOr r) {
            return String.format("(?:%s)", 
                r.ruleLists.stream()
                    .map(this::getRegexList)
                    .collect(Collectors.joining("|")));
        }

        public String getRegex() {
            return getRegex(rules.get(0));
        }
    }

    public static interface Rule {
        public int getId();
    }

    public static class RuleChar implements Rule {
        public char letter;
        private int id;
        public int getId() { return id; }
        public RuleChar(int id, char c) { 
            this.id = id;
            letter = c; 
        }
        public String toString() {
            return String.format("%d: \"%c\"", getId(), letter);
        }
    }

    public static class RuleList implements Rule {
        private int id;
        public int getId() { return id; }
        public List<Integer> ruleIds = new ArrayList();
        public String toString() {
            return String.format("%d: %s", 
                getId(),
                getRuleListString());
        }
        public String getRuleListString() {
            return ruleIds.stream().map(String::valueOf)
                .collect(Collectors.joining(" "));
        }
    }

    public static class RuleOr implements Rule {
        private int id;
        public int getId() { return id; }
        public List<RuleList> ruleLists = new ArrayList<>();
        public String toString() {
            return String.format("%d: %s", getId(),
                ruleLists.stream().map(RuleList::getRuleListString)
                    .collect(Collectors.joining(" | ")));
        }
    }

    public static Rule parseRule(String line) {
        List<String> parts = Arrays.asList(line.split(" "));
        Rule rule = null;
        int id = parseId(parts.get(0));
        if(line.contains("\"")) {
            rule = new RuleChar(id, parts.get(1).charAt(1));
        }
        else if(line.contains("|")) {
            RuleOr ruleOr = new RuleOr();
            ruleOr.id = id;
            rule = ruleOr;
            int index = parts.indexOf("|");
            ruleOr.ruleLists.add(parseRuleList(parts.subList(1, index)));
            ruleOr.ruleLists.add(parseRuleList(parts.subList(index + 1, parts.size())));
        }
        else {
            RuleList ruleList = parseRuleList(parts.subList(1, parts.size()));
            rule = ruleList;
            ruleList.id = id;
        }
        return rule;
    }

    public static RuleList parseRuleList(List<String> parts) {
        RuleList list = new RuleList();
        list.ruleIds = parts.stream().map(Integer::valueOf).collect(Collectors.toList());
        return list;
    }

    public static int parseId(String part) {
        String[] parts = part.split(":");
        return Integer.valueOf(parts[0]);
    }

    public static boolean doesMatch(RuleSet ruleSet, String line) {
        return ruleSet.isMatch(line);
    }

    public static int getAnswerA(String filepath) throws IOException {
        RuleSet ruleSet = new RuleSet();
        int countMatches = 0;
        int countTotal = 0;

        try(BufferedReader reader = new BufferedReader(new FileReader(filepath))) {
            String line = reader.readLine();
            boolean processingRules = true;
            while(line != null) {
                if(line.isEmpty()) {
                    processingRules=false;
                    line = reader.readLine();
                    continue;
                }

                if(processingRules) {
                    Rule rule = parseRule(line);
                    if(rule == null) {
                        processingRules = false;
                        line = reader.readLine();
                        continue;
                    }

                    System.out.println("Parsed rule: " + rule);

                    ruleSet.addRule(rule);
                }
                else if(doesMatch(ruleSet, line)){
                    countMatches ++;
                    countTotal ++;
                }
                else {
                    countTotal ++;
                    // System.out.println("RuleSet:\n" + ruleSet);
                }

                line = reader.readLine();

            }
        }

        System.out.println("rules\n" + ruleSet);
        System.out.println("regex=" + ruleSet.getRegex());
        System.out.println("total = " + countTotal);
        return countMatches;
    }

    public static void main(String[] args) throws IOException {
        System.out.println(String.format("B. How many messages completely match rule 0? %d", 
            getAnswerA(args[0])));
    }
    
}
