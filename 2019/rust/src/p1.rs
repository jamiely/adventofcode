use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use num_format::{Locale, ToFormattedString};

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
/// assert_eq!(aoc2019::p1::calc1a("../1.input").unwrap(), 3317100);
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
/// assert_eq!(aoc2019::p1::calc1b("../1.input").unwrap(), 4972784);
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
