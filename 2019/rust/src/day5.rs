///
/// https://adventofcode.com/2019/day/5
/// 
use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use std::collections::HashMap;

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
    pub input: Option<usize>,
    output: Option<usize>,
    instruction_pointer: usize,
    instruction_types_by_opcode: HashMap<usize, InstructionType>,
    codes: Vec<usize>,
    should_halt: bool
}

impl ProgramContext {
    fn change(&self) -> ContextChange {
        let mut change = ContextChange::new();
        change.instruction_pointer = self.instruction_pointer;
        return change;
    }

    fn get_current_opcode(&self) -> usize {
        return self.codes[self.instruction_pointer];
    }
    fn get_current_instruction(&self) -> Option<&InstructionType> {
        let opcode = self.get_current_opcode();
        return self.instruction_types_by_opcode.get(&opcode);
    }
    fn get_current_instruction_operands(&self) -> Vec<usize> {
        match self.get_current_instruction() {
            Some(instr) => {
                let start = self.instruction_pointer + 1;
                let end = start + instr.operand_count;
                return self.codes[start..end].to_vec();
            }
            None => Vec::new()
        }
    }
    pub fn new() -> ProgramContext {
        let input = None;
        let output = None;
        let instruction_pointer = 0;
        let instruction_types_by_opcode = HashMap::new();
        let codes = Vec::new();
        let should_halt = false;

        ProgramContext {
            input,
            output,
            instruction_pointer,
            instruction_types_by_opcode,
            codes,
            should_halt,
        }
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

#[derive(Clone, Copy)]
pub struct InstructionType {
    op: InstructionOperator,
    /// the number of operands used by the instruction
    operand_count: usize,
    operation: fn(context: &ProgramContext) -> Vec<ContextChange>
}

fn three_arg_op(operation: fn(usize, usize) -> usize) -> impl Fn(ProgramContext) -> Vec<ContextChange> {
    move |context: ProgramContext| -> Vec<ContextChange> {
        let args = context.get_current_instruction_operands().clone();
        let sum = operation(args[0], args[1]);
        let mut change = context.change();
        change.set_values = [(args[2], sum)].to_vec();
        return [change].to_vec();
    }
}

fn three_arg_op2(context: &ProgramContext, operation: fn(usize, usize) -> usize) -> Vec<ContextChange> {
    let indicies = context.get_current_instruction_operands().clone();
    let args: Vec<usize> = indicies.iter().map(|i| context.codes[*i]).collect();
    // println!("args={:?}", args);
    let sum = operation(args[0], args[1]);
    let mut change = context.change();
    change.set_values = [(indicies[2], sum)].to_vec();
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
        operation: |context: &ProgramContext| -> Vec<ContextChange> {
            return three_arg_op2(context, op_add);
        } },
    &InstructionType { 
        op: InstructionOperator::Mult, 
        operand_count: 3,
        operation: |context: &ProgramContext| -> Vec<ContextChange> {
            return three_arg_op2(context, op_mult);
        } },
    &InstructionType { 
        op: InstructionOperator::In, 
        operand_count: 1,
        operation: |context: &ProgramContext| -> Vec<ContextChange> {
            let mut change = context.change();
            let addr = context.get_current_instruction_operands()[0];
            change.read_input = Some(addr);
            return [change].to_vec();
        } },
    &InstructionType { 
        op: InstructionOperator::Out, 
        operand_count: 1,
        operation: |context: &ProgramContext| -> Vec<ContextChange> {
            let mut change = context.change();
            let index = context.get_current_instruction_operands()[0];
            change.write_output = Some(context.codes[index]);
            return [change].to_vec();
        } },
    &InstructionType { 
        op: InstructionOperator::Halt, 
        operand_count: 0,
        operation: |context: &ProgramContext| -> Vec<ContextChange> {
            let mut change = context.change();
            change.halt = true;
            return [change].to_vec();
        } },
];

const EmptyInstruction: InstructionType = InstructionType { op: InstructionOperator::Halt, operand_count: 0, 
    operation: |context: &ProgramContext| -> Vec<ContextChange> {
        let mut change = context.change();
        change.halt = true;
        return [change].to_vec();
    } };

fn lookup_instruction_type(opcode: usize) -> Option<InstructionType> {
    return InstructionTypes
        .iter()
        .map(|i| i.clone().to_owned())
        .find(|itype| itype.op as usize == opcode);
}

#[derive(Debug, Clone)]
pub struct ProgramResult {
    pub value: usize,
    pub output: Option<usize>
}

/// ```
/// use aoc2019::day5::{process_codes2, InstructionOperator, ProgramContext};
/// let mut codes: Vec<usize> = [InstructionOperator::Out as usize, 0, 99].to_vec();
/// let mut program_context = ProgramContext::new();
/// let program_result = process_codes2(&mut program_context, &mut codes).unwrap();
/// assert_eq!(program_result.output, Some(4));
/// ```
/// ```
/// use aoc2019::day5::{process_codes2, InstructionOperator, ProgramContext};
/// let mut codes: Vec<usize> = [InstructionOperator::In as usize, 0, 99].to_vec();
/// let mut program_context = ProgramContext::new();
/// program_context.input = Some(13);
/// let program_result = process_codes2(&mut program_context, &mut codes).unwrap();
/// assert_eq!(program_result.value, 13);
/// ```
pub fn process_codes2(program_context: &mut ProgramContext, codes: &mut Vec<usize>) -> io::Result<ProgramResult> {
    let mut instruction_types: HashMap<usize, InstructionType> = HashMap::new();
    let mut head: usize = 0;
    let mut halt = false;
    let mut output: Option<usize> = None;

    for _itype in InstructionTypes {
        instruction_types.insert(_itype.op as usize, **_itype);
    }

    program_context.instruction_types_by_opcode = instruction_types;

    loop {
        program_context.codes = codes.clone();
        program_context.instruction_pointer = head;
        program_context.should_halt = halt;
        program_context.output = output;
        println!("head={} codes={:?}", head, codes);

        if head >= codes.len() {
            println!("out of instructions");
            break;
        }
 
        if halt {
            println!("should halt");
            break;
        }

        match program_context.get_current_instruction() {
            Some(instr) => {
                let changes: Vec<ContextChange> = (instr.operation)(&program_context);
                println!("operation={:?} changes={:?}", instr.op, changes);
                for change in changes {
                    head = change.instruction_pointer;

                    for (addr, value) in change.set_values {
                        codes[addr] = value;
                    }

                    match change.read_input {
                        Some(address) =>
                            match program_context.input {
                                Some(input) => codes[address] = input,
                                _ => {}
                            }
                        _ => {}
                    }
                    match change.write_output {
                        Some(value) => output = Some(value),
                        _ => {}
                    }
                    halt = change.halt;
                }

                head += instr.operand_count + 1;
            }
            None => {
                println!("no instruction available");
                break;
            }
        }

    }

    print!("done");
    return Ok(ProgramResult{value: codes[0], output: output});

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
    let mut program_context = ProgramContext::new();
    let result = process_codes2(&mut program_context, codes).unwrap();
    println!("Result {:?}", result);
    return Ok(result.value);
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