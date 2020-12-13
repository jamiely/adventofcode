import java.io.IOException;

import day8.*;

public class Day8 {
    public static int getAnswerA(String filepath) throws IOException {
        ProgramParser parser = new ProgramParser();
        Program program = parser.parse(filepath);
        Interpreter interpreter = new Interpreter(program);
        interpreter.run();
        return interpreter.getAccumulator();
    }
    public static int getAnswerB(String filepath) throws IOException {
        ProgramParser parser = new ProgramParser();
        Program program = parser.parse(filepath);
        Interpreter interpreter = new Interpreter(program);
        interpreter.run();
        int counterToChange = 0, lastCounter = -1,
            instrCount = program.instructions.size();
        while(interpreter.haltedDueToInfiniteLoop) {
            // System.out.println("infinite loop pc=" + interpreter.infiniteLoopPC);
            if(counterToChange >= instrCount) {
                System.out.println("Exited due to instruction count exceeded.");
                return -1;
            }
            if(lastCounter >= 0) {
                // System.out.println("restoring instruction " + lastCounter);
                // restore the previous instruction
                fixInstruction(program.instructions.get(lastCounter));
            }
            for(; 
                counterToChange < instrCount 
                    && !shouldFixInstruction(program.instructions.get(counterToChange))
                ; counterToChange ++);

            if(counterToChange < instrCount) {
                // System.out.println("Fixing instruction " + counterToChange);
                fixInstruction(program.instructions.get(counterToChange));
            }

            lastCounter = counterToChange;
            counterToChange ++;
            interpreter = new Interpreter(program);
            interpreter.run();
            // if(lastCounter == 7) {
            //     System.out.println(program);
            // }
            // System.out.println("counter=" + counterToChange);
        }
        return interpreter.getAccumulator();
    }

    public static boolean shouldFixInstruction(Instruction instr) {
        return instr.op.equals("nop")
            || instr.op.equals("jmp");
    }

    public static void fixInstruction(Instruction instr) {
        String next = instr.op.equals("nop") ? "jmp" : "nop";

        // System.out.println(String.format("Changed instruction %s to %s",
        //     instr.op, next));

        instr.op = next;
    } 

    public static void main(String[] args) throws IOException {
        System.out.println(String.format("A. The value of the accumulator after a single loop is %d",
            getAnswerA(args[0])));
        System.out.println(String.format("B. The value of the accumulator after a single loop is %d",
            getAnswerB(args[0])));
    }
    
}
