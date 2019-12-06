///
/// https://adventofcode.com/2019/day/5
/// 
use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use std::collections::HashMap;

extern crate num;

fn parse_code_line(line: String) -> Vec<i32> {
    return line.split(',')
        .map(|code| code.parse::<i32>())
        .filter_map(Result::ok)
        .collect();
}

pub fn parse_codes(reader: BufReader<File>) -> Vec<i32> {
    let codes: Vec<i32> = reader.lines()
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

pub struct Instruction {
    itype: InstructionType,
    opcode: OpCode
}

impl Instruction {
    pub fn get_operand_count(&self) -> usize {
        return self.itype.operand_count;
    }
    pub fn get_param_modes(&self) -> &Vec<ParamMode> {
        return &self.opcode.param_modes;
    }
    pub fn get_operator_func(&self) -> InstructionOperatorFun {
        return self.itype.operation;
    }
    pub fn get_operator(&self) -> InstructionOperator {
        return self.itype.op;
    }
}

pub struct ProgramContext {
    pub input: Option<i32>,
    output: Option<i32>,
    instruction_pointer: usize,
    instruction_types_by_opcode: HashMap<usize, InstructionType>,
    codes: Vec<i32>,
    should_halt: bool
}

#[derive(Debug, Eq, PartialEq)]
pub struct OpCode {
    /// this is the opcode as a i32
    pub op: i32,
    /// this is the opcode in str format (with leading 0s)
    pub raw_op: String,
    pub param_modes: Vec<ParamMode>,
}

/// ```
/// use aoc2019::day5::{split_opcode};
/// let actual = split_opcode(1002);
/// let expected: (String, String) = ("02".to_string(), "10".to_string());
/// assert_eq!(actual, expected);
/// ```
pub fn split_opcode(raw_opcode: i32) -> (String, String) {
    let opcode = raw_opcode.to_string();
    let len = opcode.len();
    if len < 2 {
        return (opcode, "".to_owned());
    }
    let (p1, p2) = opcode.split_at(len - 2);
    (p2.to_owned(), p1.to_owned())
}

impl OpCode {
    /// ```
    /// use aoc2019::day5::{OpCode, InstructionTypeMult, ParamMode};
    /// // comes from opcode 1002
    /// let parts = ("02".to_string(), "10".to_string());
    /// // 02 is a multiplication
    /// let itype = &InstructionTypeMult;
    /// let actual = OpCode::parse(parts.clone(), itype);
    /// let expected = OpCode {
    ///     op: 2,
    ///     raw_op: parts.0,
    ///     param_modes: [ParamMode::Position, ParamMode::Immediate, ParamMode::Position].to_vec()
    /// };
    /// 
    /// assert_eq!(actual, expected);
    /// ```
    pub fn parse(opcode_parts: (String, String), itype: &InstructionType) -> OpCode {
        let (raw_op, str_params) = opcode_parts;
        let op = raw_op.parse::<i32>().unwrap();
        let mut param_modes = Vec::new();
        for s in str_params.chars().rev() {
            let pm = s.to_string().parse::<u32>().unwrap();
            param_modes.push(num::FromPrimitive::from_u32(pm).unwrap());

        }

        while param_modes.len() < itype.operand_count {
            param_modes.push(ParamMode::Position);
        }

        return OpCode { op, raw_op, param_modes};
    }
}

impl ProgramContext {
    fn change(&self) -> ContextChange {
        let mut change = ContextChange::new();
        change.instruction_pointer = self.instruction_pointer;
        return change;
    }

    fn get_current_opcode(&self) -> i32 {
        return self.codes[self.instruction_pointer];
    }
    fn get_current_instruction(&self) -> Option<Instruction> {
        let raw_opcode = self.get_current_opcode();
        let opcode_parts = split_opcode(raw_opcode);
        let op = opcode_parts.0.parse::<i32>().unwrap();
        
        return self.instruction_types_by_opcode.get(&(op as usize))
            .map(|itype| {
                let opcode = OpCode::parse(opcode_parts, itype);
                Instruction {itype: *itype, opcode}
            });
    }
    fn get_current_instruction_params(&self) -> Vec<InstructionParam> {
        match self.get_current_instruction() {
            Some(instr) => {
                let modes = instr.get_param_modes();
                let start = self.instruction_pointer + 1;
                let end = start + instr.get_operand_count();
                let codes = self.codes[start..end].to_vec();

                modes.iter()
                    .zip(codes)
                    .map(|(mode, value)| InstructionParam{mode: *mode, value})
                    .collect()
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

#[derive(Debug, Copy, Clone, FromPrimitive, Eq, PartialEq)]
pub enum ParamMode {
    Position = 0,
    Immediate = 1
}

#[derive(Debug, Copy, Clone)]
pub struct InstructionParam {
    mode: ParamMode,
    value: i32
}

impl InstructionParam {
    pub fn is_position(&self) -> bool {
        return self.mode == ParamMode::Position;
    }
}

// changes to apply to the program context
#[derive(Debug, Clone)]
pub struct ContextChange {
    // change the instruction pointer
    instruction_pointer: usize,
    halt: bool,
    // (address, value) pairs to set
    set_values: Vec<(usize, i32)>,
    // read input to the given address
    read_input: Option<i32>,
    // write output from the given address
    write_output: Option<i32>
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

type InstructionOperatorFun = fn(context: &ProgramContext) -> Vec<ContextChange>;

#[derive(Clone, Copy)]
pub struct InstructionType {
    op: InstructionOperator,
    /// the number of operands used by the instruction
    operand_count: usize,
    operation: InstructionOperatorFun
}

fn three_arg_op2(context: &ProgramContext, operation: fn(i32, i32) -> i32) -> Vec<ContextChange> {
    let params = context.get_current_instruction_params();
    let args: Vec<i32> = params.iter()
        .map(|param| match param.mode {
            ParamMode::Position => context.codes[param.value as usize],
            ParamMode::Immediate => param.value
        }).collect();
    println!("args={:?}", args);
    let sum = operation(args[0], args[1]);
    let mut change = context.change();
    change.set_values = [(args[2] as usize, sum)].to_vec();
    return [change].to_vec();
}

fn op_add(a: i32, b: i32) -> i32 {
    return a + b;
}

fn op_mult(a: i32, b: i32) -> i32 {
    return a * b;
}

pub const INSTRUCTION_TYPE_MULT: InstructionType = InstructionType { 
    op: InstructionOperator::Mult, 
    operand_count: 3,
    operation: |context: &ProgramContext| -> Vec<ContextChange> {
        return three_arg_op2(context, op_mult);
    } };

pub const INSTRUCTION_TYPE_ADD: InstructionType = InstructionType { 
    op: InstructionOperator::Add, 
    operand_count: 3,
    operation: |context: &ProgramContext| -> Vec<ContextChange> {
        return three_arg_op2(context, op_add);
    } };

pub const INSTRUCTION_TYPE_IN: InstructionType = InstructionType { 
    op: InstructionOperator::In, 
    operand_count: 1,
    operation: |context: &ProgramContext| -> Vec<ContextChange> {
        let mut change = context.change();
        let param = context.get_current_instruction_params()[0];
        if param.is_position() {
            change.read_input = Some(param.value);
            return [change].to_vec();
        }
        println!("Unexpected input param");
        return [].to_vec();
    } };

pub const INSTRUCTION_TYPE_OUT: InstructionType = InstructionType { 
    op: InstructionOperator::Out, 
    operand_count: 1,
    operation: |context: &ProgramContext| -> Vec<ContextChange> {
        let mut change = context.change();
        let param = context.get_current_instruction_params()[0];
        if param.is_position() {
            change.write_output = Some(context.codes[param.value as usize]);
            return [change].to_vec();
        }
        println!("unexpected output param");
        return [].to_vec();
    } };

pub const INSTRUCTION_TYPE_HALT: InstructionType = InstructionType { 
    op: InstructionOperator::Halt, 
    operand_count: 0,
    operation: |context: &ProgramContext| -> Vec<ContextChange> {
        let mut change = context.change();
        change.halt = true;
        return [change].to_vec();
    } };

pub const INSTRUCTION_TYPES: &'static [&'static InstructionType] = &[
    &INSTRUCTION_TYPE_ADD,
    &INSTRUCTION_TYPE_MULT,
    &INSTRUCTION_TYPE_IN,
    &INSTRUCTION_TYPE_OUT,
    &INSTRUCTION_TYPE_HALT,
];

fn lookup_instruction_type(opcode: i32) -> Option<InstructionType> {
    return INSTRUCTION_TYPES
        .iter()
        .map(|i| i.clone().to_owned())
        .find(|itype| itype.op as i32 == opcode);
}

#[derive(Debug, Clone)]
pub struct ProgramResult {
    pub value: i32,
    pub output: Option<i32>
}

/// ```
/// use aoc2019::day5::{process_codes2, InstructionOperator, ProgramContext};
/// let mut codes: Vec<i32> = [InstructionOperator::Out as i32, 0, 99].to_vec();
/// let mut program_context = ProgramContext::new();
/// let program_result = process_codes2(&mut program_context, &mut codes).unwrap();
/// assert_eq!(program_result.output, Some(4));
/// ```
/// 
/// ```
/// use aoc2019::day5::{process_codes2, InstructionOperator, ProgramContext};
/// let mut codes: Vec<i32> = [InstructionOperator::In as i32, 0, 99].to_vec();
/// let mut program_context = ProgramContext::new();
/// program_context.input = Some(13);
/// let program_result = process_codes2(&mut program_context, &mut codes).unwrap();
/// assert_eq!(program_result.value, 13);
/// ```
pub fn process_codes2(program_context: &mut ProgramContext, codes: &mut Vec<i32>) -> io::Result<ProgramResult> {
    let mut instruction_types: HashMap<usize, InstructionType> = HashMap::new();
    let mut head: usize = 0;
    let mut halt = false;
    let mut output: Option<i32> = None;

    for _itype in INSTRUCTION_TYPES {
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
                let changes: Vec<ContextChange> = (instr.get_operator_func())(&program_context);
                println!("operation={:?} changes={:?}", instr.get_operator(), changes);
                for change in changes {
                    head = change.instruction_pointer;

                    for (addr, value) in change.set_values {
                        codes[addr] = value;
                    }

                    match change.read_input {
                        Some(address) =>
                            match program_context.input {
                                Some(input) => codes[address as usize] = input,
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

                head += instr.get_operand_count() + 1;
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
pub fn run_codes(codes: &mut Vec<i32>) -> io::Result<i32> {
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
pub fn run_with(codes: &mut Vec<i32>, noun: i32, verb: i32) -> io::Result<i32> {
    // init
    codes[1] = noun;
    codes[2] = verb;
    return run_codes(codes);
}

pub fn get_codes(filepath: &str) -> io::Result<Vec<i32>> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);
    return Ok(parse_codes(reader));
}

/// ```
/// assert_eq!(aoc2019::day5::run_a("../input/2.input").unwrap(), 11590668);
/// ```
pub fn run_a(filepath: &str) -> io::Result<i32> {
    let mut codes = get_codes(filepath).unwrap();
    return run_with(&mut codes, 12, 2);
}

/// ```
/// let mut codes = aoc2019::day5::get_codes("../input/2.input").unwrap();
/// assert_eq!(aoc2019::day5::run_b_with(&mut codes, 12, 2, 11590668).unwrap(), 1202);
/// ```
pub fn run_b_with(codes: &mut Vec<i32>, noun: i32, verb: i32, target: i32) -> Result<i32, &'static str> {
    let output = run_with(codes, noun, verb).unwrap();
    if output == target {
        let result = 100 * noun + verb;
        return Ok(result);
    }
    return Err("Invalid target result");
}

// 19690720
pub fn discover_noun_verb(filepath: &str, target: i32) -> io::Result<()> {
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