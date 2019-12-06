extern crate aoc2019;
use aoc2019::day5;

fn main() {
    let result_a = day5::run("../input/5.input", Some(1));
    println!("result a: {:?}", result_a);
    let result_b = day5::run("../input/5.input", Some(5));
    println!("result b: {:?}", result_b);
    // let _b = day4::run_b(start, end);
}

