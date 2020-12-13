package day8;

import java.nio.file.*;
import java.util.stream.Collectors;
import java.io.*;

public class ProgramParser {
    public Program parse(String filepath) throws IOException {
        Program program = new Program();
        program.instructions =
            Files.readAllLines(Paths.get(filepath)).stream()
                .map(ProgramParser::parseLine)
                .collect(Collectors.toList());
        return program;
    }

    public static Instruction parseLine(String line) {
        String[] parts = line.split(" ");
        Instruction instr = new Instruction();
        instr.op = parts[0];
        instr.arg1 = Integer.valueOf(parts[1]);
        return instr;
    }
}
