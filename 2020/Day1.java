import java.nio.file.*;
import java.util.List;
import java.util.stream.Collectors;
import java.util.Collections;

public class Day1 {
    static class MissingException extends Exception {}

    public static int getAnswerA(List<Integer> expenses) throws MissingException{
        return getAnswerA(expenses, 2020);
    }

    public static int getAnswerA(List<Integer> expenses, int target) throws MissingException{
        return getAnswerA(expenses, target, 0, expenses.size() - 1);
    }

    public static int getAnswerA(List<Integer> expenses, int target, int startIndex, int endIndex) throws MissingException{
        // if we somehow don't find an answer then just return 1 for now
        if(endIndex - startIndex <= 0) throw new MissingException();

        int firstNumber = expenses.get(startIndex);
        int expectedNumber = target - firstNumber;
        System.out.println("Expecting number " + expectedNumber);
        while(expenses.get(endIndex) > expectedNumber) {
            endIndex --;
        }
        int lastNumber = expenses.get(endIndex);
        if(lastNumber == expectedNumber) return firstNumber * lastNumber;
        return getAnswerA(expenses, target, startIndex + 1, endIndex);
    }

    public static int getAnswerB(List<Integer> expenses) {
        // for answer B, we need to sum 3 numbers!
        return getAnswerB(expenses, 2020, 0, expenses.size() - 1);
    }

    public static int getAnswerB(List<Integer> expenses, int target, int startIndex, int endIndex) {
        int firstNumber = expenses.get(startIndex);
        int expectedNumber = target - firstNumber;
        while(expenses.get(endIndex) > expectedNumber) {
            endIndex--;
        }
        try {
            int answerA = getAnswerA(expenses, expectedNumber, startIndex, endIndex);
            return answerA * firstNumber;
        } catch(MissingException e) {
            return getAnswerB(expenses, target, startIndex + 1, endIndex);
        }
    }

    public static void main(String[] args) throws Exception {
        List<String> lines = Files.readAllLines(Paths.get(args[0]));
        List<Integer> expenses = lines.stream().map((line) -> Integer.valueOf(line)).collect(Collectors.toList());
        Collections.sort(expenses);

        int answerA = getAnswerA(expenses);
        System.out.println(String.format("The answer to A is %d", answerA));
        int answerB = getAnswerB(expenses);
        System.out.println(String.format("The answer to B is %d", answerB));
    }
}