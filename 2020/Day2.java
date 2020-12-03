/**
 * https://adventofcode.com/2020/day/2
 * 
 * ```
 * javac Day2.java && java Day2 day2.input
 * ```
 */
import java.nio.file.*;
import java.util.stream.Collectors;
import java.util.*;
import java.util.regex.*;

public class Day2 {
    public static class Policy {
        int min;
        int max;
        char character;
    }
    public static class PolicyAndPass {
        Policy policy;
        String password;
    }

    public static PolicyAndPass lineToPolicyAndPassword(String line) {
        String parts[] = line.split("\\b");

        Policy p = new Policy();
        p.min = Integer.valueOf(parts[0]);
        // parts[1] == -
        p.max = Integer.valueOf(parts[2]);
        // parts[3] == " "
        p.character = parts[4].charAt(0);
        // parts[5] == ": "
        
        PolicyAndPass pp = new PolicyAndPass();
        pp.policy = p;
        pp.password = parts[6];
        // System.out.println("Password is " + parts[6]);
        return pp;
    }

    public static boolean passwordIsValid(PolicyAndPass pp) {
        int count = 0;
        for(int i=0; i<pp.password.length(); i++) {
            if(pp.password.charAt(i) == pp.policy.character) {
                count ++;
                if(count > pp.policy.max) return false;
            }
        }
        if(count < pp.policy.min) return false;
        return true;
    }

    public static boolean passwordIsValidB(PolicyAndPass pp) {
        int count = 0;
        String pass = pp.password;
        int firstIndex = pp.policy.min -1;
        if(pass.charAt(firstIndex) == pp.policy.character) count++;
        if(pass.charAt(pp.policy.max - 1) == pp.policy.character) count++;
        return count == 1;
    }
    
    public static void main(String[] args) throws Exception {
        List<String> lines = Files.readAllLines(Paths.get(args[0]));
        int validCount = 0;
        int validCountB = 0;
        for(String line: lines) {
            PolicyAndPass pp = lineToPolicyAndPassword(line);
            if(passwordIsValid(pp)) {
                validCount++;
            }
            if(passwordIsValidB(pp)) {
                validCountB ++;
            }
        }
        System.out.println("Answer to A is " + validCount);
        System.out.println("Answer to B is " + validCountB);
    }
}
