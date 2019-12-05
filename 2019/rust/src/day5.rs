///
/// https://adventofcode.com/2019/day/5
/// 
use std::fs::File;
use std::io::{self, prelude::*, BufReader};

fn parse_code_line(line: String) -> Vec<usize> {
    return line.split(',')
        .map(|code| code.parse::<usize>())
        .filter_map(Result::ok)
        .collect();
}

pub fn parse_codes(reader: BufReader<File>) -> Vec<usize> {
    let codes: Vec<usize> = reader.lines()
        .filter_map(Result::ok)
        .flat_map(parse_code_line)
        .collect();

    return codes;
}

#[derive(Debug, Clone, Copy, Eq, PartialEq, PartialOrd)]
pub enum InstructionOperator {
    Add = 1,
    Mult = 2,
    In = 3,
    Out = 4,
    Halt = 99
}

pub struct ProgramContext {
    input: String,
    output: String,
    instruction_pointer: usize,
    current_instruction_type: InstructionType,
    current_instruction_operands: Vec<usize>
}

impl ProgramContext {
    fn change(&self) -> ContextChange {
        let mut change = ContextChange::new();
        change.instruction_pointer = self.instruction_pointer;
        return change;
    }
}

// changes to apply to the program context
#[derive(Debug, Clone)]
pub struct ContextChange {
    // change the instruction pointer
    instruction_pointer: usize,
    halt: bool,
    // (address, value) pairs to set
    set_values: Vec<(usize, usize)>,
    // read input to the given address
    read_input: Option<usize>,
    // write output from the given address
    write_output: Option<usize>
}

impl ContextChange {
    fn new() -> ContextChange {
        let instruction_pointer = 0;
        let halt = false;
        let set_values = Vec::new();
        let read_input = None;
        let write_output = None;

        return ContextChange {
            instruction_pointer,
            halt,
            set_values,
            read_input,
            write_output,
        };
    }
}

#[derive(Debug, Clone, Copy)]
pub struct InstructionType {
    op: InstructionOperator,
    /// the number of operands used by the instruction
    operand_count: usize,
    operation: fn(context: ProgramContext) -> Vec<ContextChange>
}

fn three_arg_op(operation: fn(usize, usize) -> usize) -> impl Fn(ProgramContext) -> Vec<ContextChange> {
    move |context: ProgramContext| -> Vec<ContextChange> {
        let args = context.current_instruction_operands.clone();
        let sum = operation(args[0], args[1]);
        let mut change = context.change();
        change.set_values = [(args[2], sum)].to_vec();
        return [change].to_vec();
    }
}

fn three_arg_op2(context: ProgramContext, operation: fn(usize, usize) -> usize) -> Vec<ContextChange> {
    let args = context.current_instruction_operands.clone();
    let sum = operation(args[0], args[1]);
    let mut change = context.change();
    change.set_values = [(args[2], sum)].to_vec();
    return [change].to_vec();
}

fn op_add(a: usize, b: usize) -> usize {
    return a + b;
}

fn op_mult(a: usize, b: usize) -> usize {
    return a * b;
}

const InstructionTypes: &'static [&'static InstructionType] = &[
    &InstructionType { 
        op: InstructionOperator::Add, 
        operand_count: 3,
        operation: |context: ProgramContext| -> Vec<ContextChange> {
            return three_arg_op2(context, op_add);
        } },
    &InstructionType { 
        op: InstructionOperator::Mult, 
        operand_count: 3,
        operation: |context: ProgramContext| -> Vec<ContextChange> {
            return three_arg_op2(context, op_mult);
        } },
    &InstructionType { 
        op: InstructionOperator::In, 
        operand_count: 1,
        operation: |context: ProgramContext| -> Vec<ContextChange> {
            let mut change = context.change();
            change.read_input = Some(context.current_instruction_operands[0]);
            return [change].to_vec();
        } },
    &InstructionType { 
        op: InstructionOperator::Out, 
        operand_count: 1,
        operation: |context: ProgramContext| -> Vec<ContextChange> {
            let mut change = context.change();
            change.write_output = Some(context.current_instruction_operands[0]);
            return [change].to_vec();
        } },
    &InstructionType { 
        op: InstructionOperator::Halt, 
        operand_count: 0,
        operation: |context: ProgramContext| -> Vec<ContextChange> {
            let mut change = context.change();
            change.halt = true;
            return [change].to_vec();
        } },
];

fn process_codes2(codes: &mut Vec<usize>) -> io::Result<usize> {
    let mut head: usize = 0;
    let len: usize = codes.len();

    loop {
        let end = head + 3;
        if end >= len {
            break;
        }

        // println!("opcode = {}", codes[head]);

        let result: Result<usize, &'static str> = match codes[head..end] {
            [opcode, op_index1, op_index2] => {
                let operand1 = if (op_index1 as usize) < len {
                    codes[op_index1 as usize]
                } else { std::usize::MAX };

                let operand2 = if (op_index2 as usize) < len {
                    codes[op_index2 as usize]
                } else { std::usize::MAX };

                match opcode {
                    1 => {
                        let result = operand1 + operand2;
                        // println!("[{}] + [{}] == {} + {} == {}", op_index1, op_index2, operand1, operand2, result);
                        Ok(result)
                    }
                    2 => {
                        let result = operand1 * operand2;
                        // println!("[{}] * [{}] == {} * {} == {}", op_index1, op_index2, operand1, operand2, result);
                        Ok(result)
                    }
                    99 => Err("INFO: HALT"),
                    _ => Err("ERROR: Unrecognized opcode"),
                }
            }
            _ => Err("ERROR: Not enough arguments")
        };
        match result {
            Ok(value) => {
                let op_index = head + 3 as usize;
                let out_index = codes[op_index] as usize;
                // println!("[{}] <- {}", out_index, value);
                codes[out_index] = value;
            }
            Err(value) => {
                println!("Error {}", value);
                break;
            }
        };
        head = head + 4;
        if head >= codes.len() {
            break
        }
    }
    print!("done");
    return Ok(codes[0]);

}

fn process_codes(codes: &mut Vec<usize>) -> io::Result<usize> {
    let mut head: usize = 0;
    let len: usize = codes.len();

    loop {
        let end = head + 3;
        if end >= len {
            break;
        }

        // println!("opcode = {}", codes[head]);

        let result: Result<usize, &'static str> = match codes[head..end] {
            [opcode, op_index1, op_index2] => {
                let operand1 = if (op_index1 as usize) < len {
                    codes[op_index1 as usize]
                } else { std::usize::MAX };

                let operand2 = if (op_index2 as usize) < len {
                    codes[op_index2 as usize]
                } else { std::usize::MAX };

                match opcode {
                    1 => {
                        let result = operand1 + operand2;
                        // println!("[{}] + [{}] == {} + {} == {}", op_index1, op_index2, operand1, operand2, result);
                        Ok(result)
                    }
                    2 => {
                        let result = operand1 * operand2;
                        // println!("[{}] * [{}] == {} * {} == {}", op_index1, op_index2, operand1, operand2, result);
                        Ok(result)
                    }
                    99 => Err("INFO: HALT"),
                    _ => Err("ERROR: Unrecognized opcode"),
                }
            }
            _ => Err("ERROR: Not enough arguments")
        };
        match result {
            Ok(value) => {
                let op_index = head + 3 as usize;
                let out_index = codes[op_index] as usize;
                // println!("[{}] <- {}", out_index, value);
                codes[out_index] = value;
            }
            Err(value) => {
                println!("Error {}", value);
                break;
            }
        };
        head = head + 4;
        if head >= codes.len() {
            break
        }
    }
    print!("done");
    return Ok(codes[0]);
}

/// ```
/// let mut codes = vec![1,9,10,3,2,3,11,0,99,30,40,50];
/// assert_eq!(aoc2019::day5::run_codes(&mut codes).unwrap(), 3500);
/// ```
pub fn run_codes(codes: &mut Vec<usize>) -> io::Result<usize> {
    let mut limit = 20;
    if limit > codes.len() {
        limit = codes.len() - 1;
    }
    println!("Codes Before {:?}", &codes[0..limit]);
    let result = process_codes(codes).unwrap();
    println!("Result {:?}", result);
    return Ok(result);
}

/// ```
/// let mut codes = aoc2019::day5::get_codes("../input/2.input").unwrap();
/// assert_eq!(aoc2019::day5::run_with(&mut codes, 12, 2).unwrap(), 11590668);
/// ```
pub fn run_with(codes: &mut Vec<usize>, noun: usize, verb: usize) -> io::Result<usize> {
    // init
    codes[1] = noun;
    codes[2] = verb;
    return run_codes(codes);
}

pub fn get_codes(filepath: &str) -> io::Result<Vec<usize>> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);
    return Ok(parse_codes(reader));
}

/// ```
/// assert_eq!(aoc2019::day5::run_a("../input/2.input").unwrap(), 11590668);
/// ```
pub fn run_a(filepath: &str) -> io::Result<usize> {
    let mut codes = get_codes(filepath).unwrap();
    return run_with(&mut codes, 12, 2);
}

/// ```
/// let mut codes = aoc2019::day5::get_codes("../input/2.input").unwrap();
/// assert_eq!(aoc2019::day5::run_b_with(&mut codes, 12, 2, 11590668).unwrap(), 1202);
/// ```
pub fn run_b_with(codes: &mut Vec<usize>, noun: usize, verb: usize, target: usize) -> Result<usize, &'static str> {
    let output = run_with(codes, noun, verb).unwrap();
    if output == target {
        let result = 100 * noun + verb;
        return Ok(result);
    }
    return Err("Invalid target result");
}

// 19690720
pub fn discover_noun_verb(filepath: &str, target: usize) -> io::Result<()> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);
    let original_codes = parse_codes(reader);

    for noun in 0..99 {
        for verb in 0..99 {
            let mut codes = original_codes.clone();
            match run_b_with(&mut codes, noun, verb, target) {
                Ok(result) => {
                    println!("Found target {} noun={} verb={} result={}", target, noun, verb, result);
                    return Ok(());
                }
                _ => {}
            }
        }
        print!(".");
    }

    println!("No matching verb and noun found.");
    return Ok(());
}