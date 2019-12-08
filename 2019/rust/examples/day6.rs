extern crate aoc2019;
use aoc2019::day6;

fn main() {
    let result_a = day6::run_a("../input/6.input");
    println!("result a: {:?}", result_a);
    let result_b = day6::run_b("../input/6.input", "YOU", "SAN");
    println!("result b: {:?}", result_b);
}

