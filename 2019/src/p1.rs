use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use num_format::{Locale, ToFormattedString};


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
/// assert_eq!(aoc2019::p1::calculate_fuel_required(1969), 654);
/// ```
/// 
/// ```
/// assert_eq!(aoc2019::p1::calculate_fuel_required(100756), 33583);
/// ```
pub fn calculate_fuel_required(mass: i32) -> i32 {
    return (((mass as f32) / 3.0).floor() as i32) - 2;
}

/// /// A module of mass 14 requires 2 fuel. This fuel requires no further fuel
/// /// (2 divided by 3 and rounded down is 0, which would call for a negative fuel),
/// /// so the total fuel required is still just 2.
/// 
/// /// At first, a module of mass 1969 requires 654 fuel. Then, this fuel
/// /// requires 216 more fuel (654 / 3 - 2). 216 then requires 70 more fuel, which
/// /// requires 21 fuel, which requires 5 fuel, which requires no further fuel. So,
/// /// the total fuel required for a module of mass 1969 is 654 + 216 + 70 + 21 + 5
/// /// = 966.
/// 
/// /// The fuel required by a module of mass 100756 and its fuel is: 33583 +
/// /// 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.
///
/// ```
/// assert_eq!(aoc2019::p1::calculate_fuel_required_recurse(1969), 966);
/// ```
/// 
/// ```
/// assert_eq!(aoc2019::p1::calculate_fuel_required_recurse(100756), 50346);
/// ```
pub fn calculate_fuel_required_recurse(mass: i32) -> i32 {
    if mass <= 0 {
        return 0;
    }

    let fuel = calculate_fuel_required(mass);
    if fuel <= 0 {
        return 0;
    }

    return fuel + calculate_fuel_required_recurse(fuel);
}

/// ```
/// assert_eq!(aoc2019::p1::calc1a("1.input").unwrap(), 3317100);
/// ```
pub fn calc1a(filepath: &str) -> io::Result<i32> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);

    let sum: i32 = reader.lines()
        .map(|line| line.unwrap().parse::<i32>().unwrap())
        .map(|mass| calculate_fuel_required(mass))
        .sum();

    return Ok(sum);
}

pub fn run1a(filepath: &str) -> io::Result<()> {
    let sum = calc1a(filepath)?;
    println!("The sum is {}", sum);
    Ok(())
}

///
/// ```
/// assert_eq!(aoc2019::p1::calc1b("1.input").unwrap(), 4972784);
/// ```
pub fn calc1b(filepath: &str) -> io::Result<i32> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);

    let sum: i32 = reader.lines()
        .map(|line| line.unwrap().parse::<i32>().unwrap())
        .map(|mass| {
            let sum = calculate_fuel_required(mass);
            sum + calculate_fuel_required_recurse(sum)
        })
        .sum();

    return Ok(sum);
}

pub fn run1b(filepath: &str) -> io::Result<()> {
    let sum = calc1b(filepath)?;
    println!("The sum is {} ({})", sum.to_formatted_string(&Locale::en), sum);

    Ok(())
}
