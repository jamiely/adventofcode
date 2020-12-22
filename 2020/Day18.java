import java.io.*;
import java.util.*;
import java.util.function.Function;

public class Day18 {
    public static List<String> getTokens(String line) {
        List<String> tokens = Arrays.asList(line.split(" "));
        return getTokens(tokens);
    }
    public static List<String> getTokens(List<String> tokens) {
        List<String> finalTokens = new ArrayList<>();
        for(String token: tokens) {
            if(token.equals("(")) finalTokens.add(token);
            else if(token.equals(")")) finalTokens.add(token);
            else if(token.startsWith("(")) {
                finalTokens.add("(");
                finalTokens.add(token.substring(1, token.length()));
            }
            else if(token.endsWith(")")) {
                finalTokens.add(token.substring(0, token.length() - 1));
                finalTokens.add(")");
            }
            else {
                finalTokens.add(token);
            }
        }

        if(tokens.size() == finalTokens.size()) return finalTokens;
        return getTokens(finalTokens);
    }

    public static long applyNumber(long number, long lastNumber, char lastOp) {
        if(lastNumber < 0) {
            lastNumber = number;
        }
        else {
            if(lastOp == '+') lastNumber += number;
            else if(lastOp == '*') lastNumber *= number;
            else throw new UnsupportedOperationException("Unsupported operator " + lastOp);
        }
        return lastNumber;
    }

    public static long getValue(String line, Function<Character, Integer> precedenceFunction) {
        List<String> tokens = getTokens(line);
        Deque<Long> operands = new ArrayDeque<>();
        Deque<Character> operators = new ArrayDeque<>();

        for(String token: tokens) {
            char firstChar = token.charAt(0);
            if('0' <= firstChar && firstChar <= '9') {
                operands.addLast(Long.valueOf(token));
            }
            else if(isOperator(firstChar)) {
                while(!operators.isEmpty()
                    && isOperator(operators.peekFirst())
                    && comparePrecedence(firstChar, operators.peekFirst(), precedenceFunction) <= 0) {
                        popOperator(operands, operators);
                    }
                operators.addFirst(firstChar);
            }
            else if(firstChar == '(') {
                operators.addFirst(firstChar);
            }
            else if(firstChar == ')') {
                while(operators.size() > 0 && operators.peekFirst() != '(') {
                    popOperator(operands, operators);
                }

                if(operators.peekFirst() == '(') {
                    popOperator(operands, operators);
                }
            }
            else throw new UnsupportedOperationException("Cannot process token " + token);
        }

        while(!operators.isEmpty()) {
            popOperator(operands, operators);
        }

        if(operands.size() > 1) {
            throw new IllegalStateException("More than one opperands left " + operands);
        }

        if(!operators.isEmpty()) {
            throw new IllegalStateException("Some operators were unused " + operators);
        }

        return operands.getLast();
    }

    public static boolean isOperator(char op) {
        switch(op) {
            case '+':
            case '*':
                return true;
        }
        return false;
    }

    public static int comparePrecedence(char a, char b, Function<Character, Integer> precedenceFunction) {
        return Integer.compare(
            precedenceFunction.apply(a),
            precedenceFunction.apply(b));
    }

    public static int operatorPrecedenceA(char op) {
        switch(op) {
            case '+': return 1;
            case '*': return 1;
            default: return -1;
        }
    }
    public static int operatorPrecedenceB(char op) {
        switch(op) {
            case '+': return 2;
            case '*': return 1;
            default: return -1;
        }
    }

    public static void popOperator(Deque<Long> operands, Deque<Character> operators) {
        char op = operators.pollFirst();
        if(!isOperator(op)) return;
        long first = operands.pollLast();
        long second = operands.pollLast();

        switch(op) {
            case '+':
                operands.addLast(first + second);
                break;
            case '*':
                operands.addLast(first * second);
                break;
            case '(':
                // discard operator
                break;
            default:
                throw new UnsupportedOperationException("Operator " + op + " not supported");
        }
    }

    public static long getAnswerX(String filepath, Function<Character, Integer> precedenceFunction) throws IOException {
        long sum = 0;
        try(BufferedReader reader = new BufferedReader(new FileReader(filepath))) {
            String line = reader.readLine();
            while(line != null) {
                long value = getValue(line, precedenceFunction);
                System.out.println(line + " = " + value);
                sum += value;
                line = reader.readLine();
            }
        }
        return sum;
    }

    public static long getAnswerA(String filepath) throws IOException {
        return getAnswerX(filepath, Day18::operatorPrecedenceA);
    }
    public static long getAnswerB(String filepath) throws IOException {
        return getAnswerX(filepath, Day18::operatorPrecedenceB);
    }

    public static void main(String[] args) throws IOException {
        System.out.println("A. The sum of expressions is " + getAnswerA(args[0]));
        System.out.println("B. The sum of expressions with updated precendence is " + getAnswerB(args[0]));
    }
    
}
