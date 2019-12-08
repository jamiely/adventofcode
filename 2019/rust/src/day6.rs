use std::fs::File;
use std::io::{self, prelude::*, BufReader};
use petgraph::graph::{DiGraph, NodeIndex};
use std::collections::{HashMap, HashSet};
use petgraph::algo::{bellman_ford, astar};

type NodeId = String;
type EdgeWeight = f32;
type NodeIx = NodeIndex<u32>;
type OrbitGraph = DiGraph<NodeId, EdgeWeight>;
type NodeIxMap = HashMap<NodeId, NodeIx>;

struct Orbit {
    orbiter: NodeId,
    orbited: NodeId
}

fn get_index(g: &mut OrbitGraph, node_indices: &mut NodeIxMap, node_id: NodeId) -> NodeIx {
    let orbiter_index: NodeIx = 
        node_indices.get(&node_id)
            .map(NodeIndex::to_owned)
            .unwrap_or_else(|| {
                let node = g.add_node(node_id.to_owned());
                node_indices.insert(node_id.to_owned(), node);
                node
            });

    return orbiter_index.to_owned();
}

struct Problem {
    orbits: Vec<Orbit>,
    node_indicies: NodeIxMap,
    g: OrbitGraph
}

fn load_problem(filepath: &str, add_both_edges: bool) -> io::Result<Problem> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);
    let mut orbits = Vec::<Orbit>::new();
    let mut g: OrbitGraph = DiGraph::new();
    
    reader.lines()
        .filter_map(Result::ok)
        .for_each(|line| {
            let parts: Vec<String> = line.split(")").map(str::to_owned).collect();
            let orbited: String = parts[0].to_owned();
            let orbiter: String = parts[1].to_owned();

            orbits.push(Orbit{orbited, orbiter});
        });

    // create the graph    
    let mut node_indicies: NodeIxMap = HashMap::new();
    orbits.iter().for_each(|orbit| {
        let orbiter_index = get_index(&mut g, &mut node_indicies, orbit.orbiter.to_owned());
        let orbited_index = get_index(&mut g, &mut node_indicies, orbit.orbited.to_owned());

        if add_both_edges {
          g.add_edge(orbiter_index, orbited_index, 1.0);
        }
        g.add_edge(orbited_index, orbiter_index, 1.0);
    });

    return Ok(Problem { orbits, node_indicies, g });
}

/// ```
/// use aoc2019::day6;
/// let result = day6::run_a("../input/6_small.input");
/// assert_eq!(result.unwrap(), 42);
/// ```
/// ```
/// use aoc2019::day6;
/// let result = day6::run_a("../input/6.input");
/// assert_eq!(result.unwrap(), 119831);
/// ```
pub fn run_a(filepath: &str) -> io::Result<i32> {
    let problem = load_problem(filepath, false)?;
    let orbits = problem.orbits;
    let node_indicies = problem.node_indicies;
    let g = problem.g;

    // figure out the root
    let mut orbited: HashSet<NodeId> = HashSet::new();
    node_indicies.keys().for_each(|k| { orbited.insert(k.to_owned()); } );
    orbits.iter().for_each(|orbit| {
        orbited.remove(&orbit.orbiter);
    });
    let com = orbited.iter().next().unwrap();

    let mut result = -1;
    match bellman_ford(&g, node_indicies[com]) {
        Ok((path_costs, _predecessors)) =>
            result = path_costs.iter()
                .map(|f| f.floor() as i32)
                .sum(),
        _ => {}
    }
    // let result = 0;
    println!("orbiteds={:?} sum of orbits={:?}", com, result);


    return Ok(result);
}

////// ```
////// use aoc2019::day6;
////// let result = day6::run_a("../input/6b_small.input");
////// assert_eq!(result.unwrap(), 42);
////// ```
/// ```
/// use aoc2019::day6;
/// let result = day6::run_b("../input/6.input", "YOU", "SAN");
/// assert_eq!(result.unwrap(), 119831);
/// ```
pub fn run_b(filepath: &str, body1: &str, body2: &str) -> io::Result<i32> {
    let problem = load_problem(filepath, true)?;
    let orbits = problem.orbits;
    let node_indicies = problem.node_indicies;
    let g = problem.g;

    let mut result = -1;
    let start = node_indicies.get(body1).unwrap();
    let goal = node_indicies.get(body2).unwrap();
    let path_calc = astar(&g, *start, |n| n == *goal, |_| -> f32 { 1.0 }, |_| 0.0);

    match path_calc {
        // we subtract 2 because the problem doesn't want us to include YOU AND SAN themselves
        Some((path, _)) => result = path.floor() as i32 - 2,
        _ => {}
    }
    // let result = 0;
    println!("path={:?}", result);

    return Ok(result);
}