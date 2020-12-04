import java.io.*;
import java.util.*;
import java.util.function.Function;
import java.util.regex.*;

public class Day4 {
    public static int getAnswerA(String filepath) throws IOException {
        return loadAndValidate(filepath, Day4::validateFieldExistence);
    }

    public static int getAnswerB(String filepath) throws IOException {
        return loadAndValidate(filepath, Day4::validateB);
    }

    public static int loadAndValidate(String filepath, 
        Function<Map<String, String>, Boolean> validationFunction) throws IOException {
        BufferedReader reader = new BufferedReader(
            new FileReader(filepath)
        );

        String line = reader.readLine();
        Map<String, String> fields = new HashMap<>();
        int validPassportCount = 0;

        while(line != null) {
            if(line.equals("")) {
                if(validationFunction.apply(fields)) {
                    validPassportCount ++;
                }
                fields.clear();
            }
            else {
                mergeFields(fields, line);
            }

            line = reader.readLine();
        }

        reader.close();
        return validPassportCount;
    }

    private static Pattern heightPattern = Pattern.compile("^(\\d+)(cm|in)$");
    private static Pattern hairColorPattern = Pattern.compile("^#[0-9a-f]{6}$");
    private static Pattern eyeColorPattern = Pattern.compile("^(amb|blu|brn|gry|grn|hzl|oth)$");
    private static Pattern passportIdPattern = Pattern.compile("^[0-9]{9}$");

    public static boolean validateB(Map<String, String> fieldsMap) {
        return validateFieldExistence(fieldsMap) &&
            validateEachField(fieldsMap);
    }

    public static void showFields(Map<String, String> fieldsMap) {
        System.out.println(fieldsMap);
    }

    public static boolean validateEachField(Map<String, String> fieldsMap) {
        int byr = Integer.valueOf(fieldsMap.get("byr"));
        if(byr < 1920 || byr > 2002) {
            System.out.println("birth year invalid");
            showFields(fieldsMap);
            return false;
        }

        int iyr = Integer.valueOf(fieldsMap.get("iyr"));
        if(iyr < 2010 || iyr > 2020) {
            System.out.println("issue year invalid");
            showFields(fieldsMap);
            return false;
        }

        int eyr = Integer.valueOf(fieldsMap.get("eyr"));
        if(eyr < 2020 || eyr > 2030) {
            System.out.println("expiration year invalid");
            showFields(fieldsMap);
            return false;
        }

        Matcher heightMatcher = heightPattern.matcher(fieldsMap.get("hgt"));
        if(! heightMatcher.find()) {
            System.out.println("height invalid");
            showFields(fieldsMap);
            return false;
        }
        int height = Integer.valueOf(heightMatcher.group(1));
        String heightUnit = heightMatcher.group(2);
        if(heightUnit.equals("cm")) {
            if(height < 150 || height > 193) {
                System.out.println("height invalid");
                showFields(fieldsMap);
                return false;
            }
        }
        else if(heightUnit.equals(("in"))) {
            if(height < 59 || height > 76) {
                System.out.println("height invalid");
                showFields(fieldsMap);
                return false;
            }
        }
        else {
            System.out.println("height invalid");
            showFields(fieldsMap);
            return false;
        }

        if(! hairColorPattern.matcher(fieldsMap.get("hcl")).matches()) {
            System.out.println("hair color invalid");
            showFields(fieldsMap);
            return false;
        }

        if(! eyeColorPattern.matcher(fieldsMap.get("ecl")).matches()) {
            System.out.println("eye color invalid");
            showFields(fieldsMap);
            return false;
        }

        if(! passportIdPattern.matcher(fieldsMap.get("pid")).matches()) {
            System.out.println("passport id invalid");
            showFields(fieldsMap);
            return false;
        }

        return true;
    }

    public static void mergeFields(Map<String, String> existingFields, String line) {
        String[] lineFields = line.split(" ");
        for(String pair: lineFields) {
            String[] parts = pair.split(":");
            existingFields.put(parts[0], parts[1]);
        }
    }

    public static Set<String> requiredFields = new HashSet<>();
    static {
        requiredFields.add("byr");
        requiredFields.add("iyr");
        requiredFields.add("eyr");
        requiredFields.add("hgt");
        requiredFields.add("hcl");
        requiredFields.add("ecl");
        requiredFields.add("pid");
        // requiredFields.add("cid");
    }

    public static boolean validateFieldExistence(Map<String, String> fieldsMap) {
        Set<String> names = fieldsMap.keySet();
        names.retainAll(requiredFields);
        return requiredFields.equals(names);
    }

    public static void main(String[] args) throws IOException {
        System.out.println(String.format(
            "The answer to part a is %d", getAnswerA(args[0])
        ));
        System.out.println(String.format(
            "The answer to part a is %d", getAnswerB(args[0])
        ));
    }
    
}
