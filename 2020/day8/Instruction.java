package day8;

public class Instruction {
    public String op;
    public int arg1;
    public String toString() {
        return String.format("%s %d", op, arg1);
    }
}

