use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use petgraph::visit::{IntoNodeIdentifiers, IntoEdgeReferences, NodeCompactIndexable, EdgeRef};
use petgraph::graph::{DiGraph, NodeIndex};
use std::collections::{HashMap, HashSet};
use petgraph::algo::bellman_ford;

type MyGraph = DiGraph<String, f32>;
type Node = NodeIndex<u32>;

/// ```
/// use aoc2019::day6::{ run };
/// let result = run("../input/6_small.input");
/// assert_eq!(result.unwrap(), 42);
/// ```
pub fn run(filepath: &str) -> io::Result<i32> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);
    let mut nodes = HashMap::<String, Node>::new();
    let mut g: MyGraph = DiGraph::new();
    let mut orbiters = HashSet::<String>::new();
    let mut orbiteds = HashSet::<String>::new();

    reader.lines()
        .filter_map(Result::ok)
        .map(|line| -> Vec<String> {
            return line.split(")").map(str::to_string).collect()
        })
        .filter_map(|parts: Vec<String>|
            Some((parts[0].to_string(), parts[1].to_string())))
        .for_each(|(orbited, orbiter)| {
            orbiters.insert(orbiter.to_string());
            orbiteds.insert(orbited.to_string());

            let a: NodeIndex = match nodes.get(&orbiter) {
                Some(value) => *value,
                None => {
                    let create = g.add_node(orbiter.to_string());
                    nodes.insert(orbiter.to_string(), create);
                    create
                }
            };
            let b: NodeIndex = match nodes.get(&orbited) {
                Some(value) => *value,
                None => {
                    let create = g.add_node(orbited.to_string());
                    nodes.insert(orbited.to_string(), create);
                    create
                }
            };

            g.add_edge(a, b, 0.0);
        });

    // now we can find the root
    for o in orbiters {
        orbiteds.remove(&o);
    }

    let com = orbiteds.iter().next().unwrap();

    let result = bellman_ford(&g, nodes[com]);
    println!("orbiteds={:?} result={:?}", com, result);


    return Ok(g.node_count() as i32);
}