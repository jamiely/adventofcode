/// ```
/// assert_eq!(aoc2019::day4::is_valid_password(11111), true);
/// ```
/// ```
/// assert_eq!(aoc2019::day4::is_valid_password(223450), false);
/// ```
/// ```
/// assert_eq!(aoc2019::day4::is_valid_password(123789), false);
/// ```
pub fn is_valid_password(original_num: usize) -> bool {
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
/// ```
/// assert_eq!(aoc2019::day4::run_a(134792, 675810), 1955);
/// ```
pub fn run_a(start: usize, end: usize) -> usize {
    let number_of_possibilities = (start..=end)
        .filter(|i| is_valid_password(*i))
        .count();
    println!("The number of possibilities is {}", number_of_possibilities);
    return number_of_possibilities;
}