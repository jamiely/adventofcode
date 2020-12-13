package day8;

import java.util.HashSet;
import java.util.*;

public class Interpreter {
    Program program;
    int accumulator = 0;
    public int pc = 0;
    public int previousPC = 0;
    public boolean haltedDueToInfiniteLoop = false;
    public int infiniteLoopPC = -1;

    public Interpreter(Program program) {
        this.program = program;
    }
    public void run() {
        int maxInstr = program.instructions.size();
        Set<Integer> visited = new HashSet<>();
        while(pc < maxInstr && pc >= 0) {
            if(visited.contains(pc)) {
                haltedDueToInfiniteLoop = true;
                infiniteLoopPC = pc;
                return;
            }
            visited.add(pc);
            Instruction instr = getCurrentInstruction();
            int oldPC = pc;
            processInstruction(instr);
            previousPC = oldPC;
        }
    }
    private void processInstruction(Instruction instr) {
        switch(instr.op) {
            case "nop":
                pc++;
                break;
            case "acc":
                accumulator += instr.arg1;
                pc++;
                break;
            case "jmp":
                pc += instr.arg1;
                break;
        }
    }
    private Instruction getInstruction(int i) {
        return program.instructions.get(i);
    }
    private Instruction getCurrentInstruction() {
        return getInstruction(pc);
    }

    public int getAccumulator() {
        return accumulator;
    }
    public void setAccumulator(int value) {
        accumulator = value;
    }
}
