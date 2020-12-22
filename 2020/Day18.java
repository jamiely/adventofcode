import java.io.*;
import java.util.*;

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

    public static long getValue(String line) {
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
                    && comparePrecedence(firstChar, operators.peekFirst()) <= 0) {
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
        return operatorPrecedence(op) > 0;
    }

    public static int comparePrecedence(char a, char b) {
        return Integer.compare(
            operatorPrecedence(a),
            operatorPrecedence(b));
    }

    public static int operatorPrecedence(char op) {
        switch(op) {
            case '+': return 1;
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

    public static long getAnswerA(String filepath) throws IOException {
        long sum = 0;
        try(BufferedReader reader = new BufferedReader(new FileReader(filepath))) {
            String line = reader.readLine();
            while(line != null) {
                long value = getValue(line);
                System.out.println(line + " = " + value);
                sum += value;
                line = reader.readLine();
            }
        }
        return sum;
    }

    public static void main(String[] args) throws IOException {
        System.out.println("A. The sum of expressions is " + getAnswerA(args[0]));
    }
    
}
