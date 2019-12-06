///
/// https://adventofcode.com/2019/day/3
/// 
use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use std::cmp::{max, min};
use std::collections::HashMap;

#[derive(Debug, Clone, Copy)]
pub enum Direction {
    Up,
    Down,
    Left,
    Right
}

#[derive(Debug, Clone, Copy)]
pub struct Instruction {
    direction: Direction,
    steps: i32
}

#[derive(Debug, Clone, Copy)]
pub struct Size {
    width: i32,
    height: i32
}

#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq)]
pub struct Point {
    x: i32,
    y: i32
}

#[derive(Debug, Clone, Copy)]
pub struct Box {
    origin: Point,
    size: Size
}

pub struct Wire {
    instructions: Vec<Instruction>,
    bounding_box: Box
}

pub fn bounding_box(instructions: &Vec<Instruction>) -> Box {
    let mut x_left = 0;
    let mut x_right = 0;
    let mut y_top = 0;
    let mut y_bottom = 0;
    let mut x = 0;
    let mut y = 0;

    for instruction in instructions {
        match instruction.direction {
            Direction::Up => y += instruction.steps,
            Direction::Down => y -= instruction.steps,
            Direction::Left => x -= instruction.steps,
            Direction::Right => x -= instruction.steps
        }

        x_right = max(x, x_right);
        x_left = min(x, x_left);
        y_top = max(y, y_top);
        y_bottom = min(y, y_bottom);
    }

    let width = x_right - x_left;
    let height = y_top - y_bottom;
    let size = Size { width, height };
    let origin = Point { x: x_left, y: y_bottom };

    return Box { origin, size };
}

pub fn parse_dir(s: &str) -> Option<Direction> {
    return match s {
        "U" => Some(Direction::Up),
        "D" => Some(Direction::Down),
        "R" => Some(Direction::Right),
        "L" => Some(Direction::Left),
        _ => None
    };
}

pub fn parse_instruction_str(s: &str) -> Option<Instruction> {
    if s.len() < 2 {
        return None;
    }

    let (s_dir, s_steps) = s.split_at(1);

    return match (parse_dir(s_dir), s_steps.parse::<i32>().ok()) {
        (Some(direction), Some(steps)) => Some(Instruction { direction, steps }),
        _ => None
    };
}

pub fn parse_instruction_line(line: &String) -> Vec<Instruction> {
    return line.split(',')
        .map(parse_instruction_str)
        .filter_map(|x| x)
        .collect();
}

pub fn instruction_points(instructions: &Vec<Instruction>) -> Vec<Point> {
    let mut x = 0;
    let mut y = 0;

    let mut points: Vec<Point> = Vec::new();
    points.push(Point{x,y});

    for instruction in instructions {
        for _i in 1..=instruction.steps {
            match instruction.direction {
                Direction::Up => y += 1,
                Direction::Down => y -= 1,
                Direction::Left => x -= 1,
                Direction::Right => x += 1
            }
            points.push(Point{x,y});
        }
    }

    return points;
}

#[derive(Debug, Copy, Clone)]
pub struct Intersection {
    point: Point,
    sum_steps_to_point: usize
}

pub fn find_instruction_intersection_points(primary: &Vec<Instruction>, other: &Vec<Instruction>) -> Vec<Point> {
    return find_instruction_intersections(primary, other)
        .iter()
        .map(|i| i.point)
        .collect();
}

pub fn find_instruction_intersections(primary: &Vec<Instruction>, other: &Vec<Instruction>) -> Vec<Intersection> {
    let points = instruction_points(primary);
    // we want to convert this to a Set for easy lookup
    let points_set: HashMap<Point, usize> = points.iter().enumerate()
        .map(|(i, p)| (p.to_owned(), i)) 
        .collect();
    
    println!("Contains {} points", points.len());

    let other_points = instruction_points(other);

    return other_points
        .iter().enumerate()
        .filter(|(_i, p)| points_set.contains_key(p))
        .map(|(i, p)| Intersection{
            point: p.to_owned(),
            sum_steps_to_point: i + points_set[p]
        })
        .collect()
}

pub fn manhattan_distance(p1: &Point, p2: &Point) -> i32 {
    return (p1.x - p2.x).abs() + (p1.y - p2.y).abs();
}

pub fn load_instruction_sets(filepath: &str) -> io::Result<Vec<Vec<Instruction>>> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);
    let lines: Vec<String> = reader.lines()
        .filter_map(Result::ok)
        .collect();
    let instruction_sets: Vec<Vec<Instruction>> = lines
        .iter()
        .map(|line| -> Vec<Instruction> {
            let instructions: Vec<Instruction> = parse_instruction_line(line);
            return instructions;
        })
        .collect();
    return Ok(instruction_sets);
}

// a: 1064
/// ```
/// assert_eq!(aoc2019::day3::run_a("../input/3.input").unwrap(), 1064);
/// ```
pub fn run_a(filepath: &str) -> io::Result<i32> {
    let instruction_sets = load_instruction_sets(filepath)?;
    
    let origin = Point{x: 0, y: 0};
    let mut result = -1;
    match &instruction_sets[0..2] {
        [i1, i2] => {
            let intersections: Vec<Point> = find_instruction_intersection_points(i1, i2);
            let mut distances: Vec<i32> = intersections.iter()
                .map(|p| manhattan_distance(p, &origin))
                .collect();
            distances.sort();

            result = distances[1];

            // println!("intersections {:?}", intersections);
            println!("sorted distances {:?}", distances);
        }
        _ => println!("unexpected")
    }
    
    return Ok(result);
}

/// ```
/// assert_eq!(aoc2019::day3::run_b("../input/3.input").unwrap(), 25676);
/// ```
pub fn run_b(filepath: &str) -> io::Result<usize> {
    let instruction_sets = load_instruction_sets(filepath)?;
    
    let mut result = 0;
    match &instruction_sets[0..2] {
        [i1, i2] => {
            let mut intersections: Vec<Intersection> = find_instruction_intersections(i1, i2);
            intersections.sort_by(|a, b| a.sum_steps_to_point.cmp(&b.sum_steps_to_point));

            result = intersections[1].sum_steps_to_point;

            // println!("intersections {:?}", intersections);
            println!("sorted intersections {:?}", intersections);
        }
        _ => println!("unexpected")
    }
    
    println!("Result is {}", result);
    return Ok(result);
}
