package day8;

import java.util.*;
import java.util.stream.Collectors;

public class Program {
    public List<Instruction> instructions;

    public String toString() {
        return instructions.stream().map(Instruction::toString)
            .collect(Collectors.joining("\n"));
    }
}
