use std::fs::File;
use std::io::{self, prelude::*, BufReader};

fn parse_code_line(line: String) -> Vec<i32> {
    return line.split(',')
        .map(|code| code.parse::<i32>())
        .filter_map(Result::ok)
        .collect();
}

fn parse_codes(reader: BufReader<File>) -> Vec<i32> {
    let codes: Vec<i32> = reader.lines()
        .filter_map(Result::ok)
        .flat_map(parse_code_line)
        .collect();

    return codes;
}

fn process_codes(codes: &mut Vec<i32>) -> io::Result<i32> {
    let mut head: usize = 0;
    let len: usize = codes.len();

    loop {
        let end = head + 3;
        if end >= len {
            break;
        }

        println!("opcode = {}", codes[head]);

        let result: Result<i32, &'static str> = match codes[head..end] {
            [opcode, op_index1, op_index2] => {
                println!("?");
                let operand1 = if (op_index1 as usize) < len {
                    codes[op_index1 as usize]
                } else { -1 };

                let operand2 = if (op_index2 as usize) < len {
                    codes[op_index2 as usize]
                } else { -1 };

                match opcode {
                    1 => {
                        let result = operand1 + operand2;
                        println!("[{}] + [{}] == {} + {} == {}", op_index1, op_index2, operand1, operand2, result);
                        Ok(result)
                    }
                    2 => {
                        let result = operand1 * operand2;
                        println!("[{}] * [{}] == {} * {} == {}", op_index1, op_index2, operand1, operand2, result);
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
                println!("[{}] <- {}", out_index, value);
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
        print!(".");
    }
    print!("done");
    return Ok(codes[0]);
}

/// ```
/// let mut codes = vec![1,9,10,3,2,3,11,0,99,30,40,50];
/// assert_eq!(aoc2019::day2::run_codes(&mut codes).unwrap(), 3500);
/// ```
pub fn run_codes(codes: &mut Vec<i32>) -> io::Result<i32> {
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
/// assert_eq!(aoc2019::day2::run_a("../2.input").unwrap(), 11590668);
/// ```
pub fn run_a(filepath: &str) -> io::Result<i32> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);

    let mut codes = parse_codes(reader);
    // init
    codes[1] = 12;
    codes[2] = 2;
    return run_codes(&mut codes);
}