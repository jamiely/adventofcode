/// ```
/// assert_eq!(aoc2019::day4::is_valid_password_a(11111), true);
/// ```
/// ```
/// assert_eq!(aoc2019::day4::is_valid_password_a(223450), false);
/// ```
/// ```
/// assert_eq!(aoc2019::day4::is_valid_password_a(123789), false);
/// ```
pub fn is_valid_password_a(original_num: usize) -> bool {
    let mut last_digit: i32 = -1;
    let mut had_adjacent_digit = false;
    let mut num = original_num as i32;
    for i in &[100000, 10000, 1000, 100, 10, 1] {
        let digit: i32 = num / i;
        num -= digit * i;
        // println!("num={} digit={} last_digit={}", num, digit, last_digit);
        if digit < last_digit {
            return false;
        }
        had_adjacent_digit = had_adjacent_digit || (digit == last_digit);
        last_digit = digit;
    }
    return had_adjacent_digit;
}
pub fn run_generic(start: usize, end: usize, is_valid: fn(usize) -> bool) -> usize {
    let number_of_possibilities = (start..=end)
        .filter(|i| is_valid(*i))
        .count();
    println!("The number of possibilities is {}", number_of_possibilities);
    return number_of_possibilities;
}
/// ```
/// assert_eq!(aoc2019::day4::run_a(134792, 675810), 1955);
/// ```
pub fn run_a(start: usize, end: usize) -> usize {
    return run_generic(start, end, is_valid_password_a);
}
/// ```
/// assert_eq!(aoc2019::day4::run_b(134792, 675810), 1319);
/// ```
pub fn run_b(start: usize, end: usize) -> usize {
    return run_generic(start, end, is_valid_password_b);
}
/// ```
/// assert_eq!(aoc2019::day4::is_valid_password_b(112233), true);
/// ```
/// ```
/// assert_eq!(aoc2019::day4::is_valid_password_b(123444), false);
/// ```
/// ```
/// assert_eq!(aoc2019::day4::is_valid_password_b(111122), true);
/// ```
pub fn is_valid_password_b(original_num: usize) -> bool {
    let mut last_digit: i32 = -1;
    let mut had_adjacent_digit = false;
    let mut last_had_adjacent_digit = false;
    let mut adjacent_digit_count = 1;
    let mut num = original_num as i32;
    for i in &[100000, 10000, 1000, 100, 10, 1] {
        let digit: i32 = num / i;
        num -= digit * i;
        // println!("num={} digit={} last_digit={}", num, digit, last_digit);
        if digit < last_digit {
            return false;
        }
        if digit == last_digit {
            adjacent_digit_count += 1;
            if adjacent_digit_count == 2 {
                last_had_adjacent_digit = true;
            }
            else if adjacent_digit_count > 2 {
                last_had_adjacent_digit = false;
            }
        } else {
            adjacent_digit_count = 1;
            had_adjacent_digit |= last_had_adjacent_digit;
            last_had_adjacent_digit = false;
        }
        last_digit = digit;
    }
    had_adjacent_digit |= last_had_adjacent_digit;
    // println!("num={} valid?={}s", original_num, had_adjacent_digit);
    return had_adjacent_digit;
}