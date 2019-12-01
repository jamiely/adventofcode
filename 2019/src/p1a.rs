use std::fs::File;
use std::io::{self, prelude::*, BufReader};


/// /// Fuel required to launch a given module is based on its mass. Specifically,
/// /// to find the fuel required for a module, take its mass, divide by three,
/// /// round down, and subtract 2.
/// /// 
/// /// For example:
/// /// 
/// ///     For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
/// ///     For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
/// ///     For a mass of 1969, the fuel required is 654.
/// ///     For a mass of 100756, the fuel required is 33583.
/// /// 
///
/// ```
/// assert_eq!(aoc2019::p1a::calculate_fuel_required(1969), 654);
/// ```
/// 
/// ```
/// assert_eq!(aoc2019::p1a::calculate_fuel_required(100756), 33583);
/// ```
pub fn calculate_fuel_required(mass: i32) -> i32 {
    return (((mass as f32) / 3.0).floor() as i32) - 2;
}

pub fn run() -> io::Result<()> {
    let file = File::open("1.input")?;
    let reader = BufReader::new(file);

    let sum: i32 = reader.lines()
        .map(|line| line.unwrap().parse::<i32>().unwrap())
        .map(|mass| calculate_fuel_required(mass))
        .sum();

    println!("The sum is {}", sum);

    Ok(())
}
