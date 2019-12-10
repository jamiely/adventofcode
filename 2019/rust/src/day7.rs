///
/// https://adventofcode.com/2019/day/7
/// 
use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use std::collections::{HashMap, VecDeque, HashSet};
use std::iter::FromIterator;

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
    JumpIfTrue = 5,
    JumpIfFalse = 6,
    LessThan = 7,
    Equals = 8,
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
    pub input: VecDeque<i32>,
    output: Vec<i32>,
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
    /// use aoc2019::day5::{OpCode, INSTRUCTION_TYPE_MULT, ParamMode};
    /// // comes from opcode 1002
    /// let parts = ("02".to_string(), "10".to_string());
    /// // 02 is a multiplication
    /// let itype = &INSTRUCTION_TYPE_MULT;
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
        return ContextChange::new();
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
        let input = VecDeque::new();
        let output = Vec::new();
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
    instruction_pointer: Option<usize>,
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
        let instruction_pointer = None;
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

pub type InstructionOperatorFun = fn(context: &ProgramContext) -> Vec<ContextChange>;

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
    // println!("args={:?}", args);
    let sum = operation(args[0], args[1]);
    let mut change = context.change();
    change.set_values = [(params[2].value as usize, sum)].to_vec();
    return [change].to_vec();
}

fn op_add(a: i32, b: i32) -> i32 {
    return a + b;
}

fn op_mult(a: i32, b: i32) -> i32 {
    return a * b;
}

fn jump_test(context: &ProgramContext, jump_predicate: fn(value: i32) -> bool) -> Vec<ContextChange> {
    let mut change = context.change();
    let params = context.get_current_instruction_params();
    let args: Vec<i32> = params.iter()
        .map(|param| match param.mode {
            ParamMode::Position => context.codes[param.value as usize],
            ParamMode::Immediate => param.value
        }).collect();

    let test = args[0];
    if jump_predicate(test) {
        change.instruction_pointer = Some(args[1] as usize);
        return [change].to_vec();
    }
    return [].to_vec();

}

fn cmp_test(context: &ProgramContext, cmp_predicate: fn(a: i32, b: i32) -> bool) -> Vec<ContextChange> {
    let mut change = context.change();
    let params = context.get_current_instruction_params();
    let args: Vec<i32> = params.iter()
        .map(|param| match param.mode {
            ParamMode::Position => context.codes[param.value as usize],
            ParamMode::Immediate => param.value
        }).collect();

    let mut store_value = 0;
    if cmp_predicate(args[0], args[1]) {
        store_value = 1;
    }
    change.set_values.push((params[2].value as usize, store_value));
    return [change].to_vec();

}

pub const INSTRUCTION_TYPE_JUMP_IFTRUE: InstructionType = InstructionType {
    op: InstructionOperator::JumpIfTrue, 
    operand_count: 2,
    operation: |context: &ProgramContext| -> Vec<ContextChange> {
        return jump_test(context, |i| i != 0);
    } };

pub const INSTRUCTION_TYPE_JUMP_IFFALSE: InstructionType = InstructionType {
    op: InstructionOperator::JumpIfFalse, 
    operand_count: 2,
    operation: |context: &ProgramContext| -> Vec<ContextChange> {
        return jump_test(context, |i| i == 0);
    } };

pub const INSTRUCTION_TYPE_LESSTHAN: InstructionType = InstructionType {
    op: InstructionOperator::LessThan, 
    operand_count: 3,
    operation: |context: &ProgramContext| -> Vec<ContextChange> {
        return cmp_test(context, |a,b| a < b);
    } };

pub const INSTRUCTION_TYPE_EQUALS: InstructionType = InstructionType {
    op: InstructionOperator::Equals, 
    operand_count: 3,
    operation: |context: &ProgramContext| -> Vec<ContextChange> {
        return cmp_test(context, |a,b| a == b);
    } };

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
        let params = context.get_current_instruction_params();
        let args: Vec<i32> = params.iter()
            .map(|param| match param.mode {
                ParamMode::Position => context.codes[param.value as usize],
                ParamMode::Immediate => param.value
            }).collect();

        change.write_output = Some(args[0]);
        return [change].to_vec();
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
    &INSTRUCTION_TYPE_JUMP_IFTRUE,
    &INSTRUCTION_TYPE_JUMP_IFFALSE,
    &INSTRUCTION_TYPE_LESSTHAN,
    &INSTRUCTION_TYPE_EQUALS,
];

#[derive(Debug, Clone)]
pub struct ProgramResult {
    pub value: i32,
    pub output: Vec<i32>,
    pub diagnostic_code: Option<i32>
}

/// ```
/// use aoc2019::day5::{process_codes2, InstructionOperator, ProgramContext};
/// let mut codes: Vec<i32> = [InstructionOperator::Out as i32, 0, 99].to_vec();
/// let mut program_context = ProgramContext::new();
/// let program_result = process_codes2(&mut program_context, &mut codes).unwrap();
/// assert_eq!(program_result.output, [4].to_vec());
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
/// Tests jumps 1a (position mode)
/// ```
/// use aoc2019::day5::{process_codes2, InstructionOperator, ProgramContext};
/// let mut codes: Vec<i32> = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9].to_vec();
/// let mut program_context = ProgramContext::new();
/// program_context.input = Some(99);
/// let program_result = process_codes2(&mut program_context, &mut codes).unwrap();
/// assert_eq!(program_result.diagnostic_code, Some(1));
/// ```
/// Test jumps 1b (position mode)
/// ```
/// use aoc2019::day5::{process_codes2, InstructionOperator, ProgramContext};
/// let mut codes: Vec<i32> = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9].to_vec();
/// let mut program_context = ProgramContext::new();
/// program_context.input = Some(0);
/// let program_result = process_codes2(&mut program_context, &mut codes).unwrap();
/// assert_eq!(program_result.diagnostic_code, Some(0));
/// ```
/// Test jumps 2a (immediate mode)
/// ```
/// use aoc2019::day5::{process_codes2, InstructionOperator, ProgramContext};
/// let mut codes: Vec<i32> = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1].to_vec();
/// let mut program_context = ProgramContext::new();
/// program_context.input = Some(0);
/// let program_result = process_codes2(&mut program_context, &mut codes).unwrap();
/// assert_eq!(program_result.diagnostic_code, Some(0));
/// ```
/// Test jumps 2b (immediate mode)
/// ```
/// use aoc2019::day5::{process_codes2, InstructionOperator, ProgramContext};
/// let mut codes: Vec<i32> = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1].to_vec();
/// let mut program_context = ProgramContext::new();
/// program_context.input = Some(99);
/// let program_result = process_codes2(&mut program_context, &mut codes).unwrap();
/// assert_eq!(program_result.diagnostic_code, Some(1));
/// ```
/// Test all simple
/// ```
/// use aoc2019::day5::{process_codes2, InstructionOperator, ProgramContext};
/// let mut codes: Vec<i32> = [11108, 0, 0, 1, 4, 1].to_vec();
/// let mut program_context = ProgramContext::new();
/// let program_result = process_codes2(&mut program_context, &mut codes).unwrap();
/// assert_eq!(program_result.diagnostic_code, Some(1));
/// ```
/// Test jumps 3a
/// ```
/// use aoc2019::day5::{process_codes2, InstructionOperator, ProgramContext};
/// let mut codes: Vec<i32> = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31, 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104, 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99].to_vec();
/// let mut program_context = ProgramContext::new();
/// program_context.input = Some(7);
/// let program_result = process_codes2(&mut program_context, &mut codes).unwrap();
/// assert_eq!(program_result.diagnostic_code, Some(999));
/// ```
pub fn process_codes2(program_context: &mut ProgramContext, codes: &mut Vec<i32>) -> io::Result<ProgramResult> {
    let mut instruction_types: HashMap<usize, InstructionType> = HashMap::new();
    let mut head: usize = 0;
    let mut halt = false;
    let mut output: Vec<i32> = Vec::new();

    for _itype in INSTRUCTION_TYPES {
        instruction_types.insert(_itype.op as usize, **_itype);
    }

    program_context.instruction_types_by_opcode = instruction_types;

    loop {
        program_context.codes = codes.clone();
        program_context.instruction_pointer = head;
        program_context.should_halt = halt;
        program_context.output = output.clone();
        // println!("head={} codes={:?}", head, codes);

        if head >= codes.len() {
            // println!("out of instructions");
            break;
        }
 
        if halt {
            // println!("should halt");
            break;
        }

        match program_context.get_current_instruction() {
            Some(instr) => {
                let changes: Vec<ContextChange> = (instr.get_operator_func())(&program_context);
                // println!("instr.opcode={:?} instr.itype=(op={:?} operand_count={}) changes={:?}\n", 
                //     instr.opcode, instr.itype.op, instr.itype.operand_count, changes);
                let mut instruction_pointer_changed = false;
                for change in changes {
                    match change.instruction_pointer {
                        Some(pointer) => {
                            instruction_pointer_changed = true;
                            head = pointer
                        }
                        _ => {}
                    }

                    for (addr, value) in change.set_values {
                        codes[addr] = value;
                    }

                    match change.read_input {
                        Some(address) =>
                            match program_context.input.pop_front() {
                                Some(input) => codes[address as usize] = input,
                                _ => {}
                            }
                        _ => {}
                    }
                    match change.write_output {
                        Some(value) => output.push(value),
                        _ => {}
                    }
                    halt = change.halt;
                }

                if ! instruction_pointer_changed {
                    head += instr.get_operand_count() + 1;
                }
            }
            None => {
                println!("no instruction available");
                break;
            }
        }

    }

    // print!("done");
    let diagnostic_code = output.last().map(i32::to_owned);
    return Ok(ProgramResult{value: codes[0], output: output, diagnostic_code});

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

pub fn get_codes(filepath: &str) -> io::Result<Vec<i32>> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);
    return Ok(parse_codes(reader));
}

////// Day 2
////// ```
////// assert_eq!(aoc2019::day7::run("../input/2.input", Vec::new()).unwrap().value, 1870666);
////// ```
////// Part A
////// ```
////// assert_eq!(aoc2019::day7::run("../input/5.input", [1].to_vec()).unwrap().diagnostic_code, Some(15426686));
////// ```
////// Part B
////// ```
////// assert_eq!(aoc2019::day7::run("../input/5.input", [5].to_vec()).unwrap().diagnostic_code, Some(11430197));
////// ```
/// Day 7 tests
/// ```
/// let codes = aoc2019::day7::get_codes("../input/7a.input").unwrap();
/// assert_eq!(aoc2019::day7::get_max_thruster_signal(&codes, [4,3,2,1,0]).unwrap(), 43210);
/// ```
/// ```
/// let codes = aoc2019::day7::get_codes("../input/7b.input").unwrap();
/// assert_eq!(aoc2019::day7::get_max_thruster_signal(&codes, [0,1,2,3,4]).unwrap(), 54321);
/// ```
/// ```
/// let codes = aoc2019::day7::get_codes("../input/7c.input").unwrap();
/// assert_eq!(aoc2019::day7::get_max_thruster_signal(&codes, [1,0,4,3,2]).unwrap(), 65210);
/// ```
pub fn get_max_thruster_signal(codes: &Vec<i32>, phase_setting_sequence: [i32; 5]) -> io::Result<i32> {
    let mut last_output = 0;
    for phase_setting in phase_setting_sequence.iter() {
        let result = run_for_phase_sequence(
            &codes, *phase_setting, last_output)?;
        if result.output.len() != 1 {
            return Err(io::Error::new(io::ErrorKind::Other, "Expected only one output"));
        }
        last_output = result.output[0];
    }
    return Ok(last_output);
}

pub fn run_for_phase_sequence(
    original_codes: &Vec<i32>, phase_setting: i32, 
    input_signal: i32) -> io::Result<ProgramResult> {
    let mut codes = original_codes.clone();
    let mut context = ProgramContext::new();
    context.input = VecDeque::from(vec![phase_setting, input_signal]);
    return process_codes2(&mut context, &mut codes);
}

/// ```
/// let result = aoc2019::day7::run_a("../input/7.input");
/// assert_eq!(result.unwrap(), 914828);
/// ```
pub fn run_a(filepath: &str) -> io::Result<i32> {
    let mut max_signal: i32 = -1;
    let codes = get_codes(filepath).unwrap();

    for i in (0..=4) {
        for j in (0..=4) {
            for k in (0..=4) {
                for l in (0..=4) {
                    for m in (0..=4) {
                        let set = HashSet::<i32>::from_iter(vec![i, j, k, l, m]);
                        if set.len() != 5 { 
                            continue; 
                        }

                        let result = get_max_thruster_signal(
                            &codes, [i, j, k, l, m]
                        );
            
                        match result {
                            Ok(signal) if signal > max_signal => {
                                max_signal = signal;
                                println!("Got larger value {}{}{}{}{} => {}", i, j, k, l, m, signal);
                            }
                            Ok(signal) => println!("Got smaller value {}", signal),
                            _ => println!("There was some problem")
                        }
                    }
                }
            }
        }
    }
    return Ok(max_signal);
}
