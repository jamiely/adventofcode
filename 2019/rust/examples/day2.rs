extern crate aoc2019;
use aoc2019::day2;

fn main() {
    let filepath = "../2.input";
    let _ = day2::run_a(filepath);
    let _ = day2::discover_noun_verb(filepath, 19690720);
}

