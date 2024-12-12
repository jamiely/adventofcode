from io import open

def run():
  grid = load("day10.input")
  result = process(grid)

  print(result)

def load(path):
  with open(path, "r") as f:
    return [[{
      "display": int(display),
      "score": 0,
    } for display in list(line.strip())] for line in f]
  
def process(grid):
  # just going to brute force this

  count = 0
  for (r, c) in grid_indices(grid):
    grid[r][c]["coords"] = (r, c)

  for (r, c) in grid_indices(grid):
    if grid[r][c]["display"] != 0:
      continue
    
    count += traverse(grid, (r, c), 0)


  return count

def traverse(grid, coords, match):
  # print(f"coords={coords} match={match}")
  (r, c) = coords
  display = grid[r][c]["display"]
  if display != match:
    return 0
  elif display == 9:
    return 1
  
  next_match = match + 1

  count = 0
  for neighbor in get_neighbors(grid, r, c, next_match):
    result = traverse(grid, neighbor["coords"], next_match)
    count += result

  return count

def grid_bounds(grid):
  return (len(grid), len(grid[0]))

def get_neighbors(grid, r, c, match):
  (rows, cols) = grid_bounds(grid)

  candidates = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]

  return [grid[r][c] for (r, c) in candidates 
          if r >= 0 and c >= 0 and r < rows and c < cols 
          and grid[r][c]["display"] == match]
  

def grid_indices(grid):
  (rows, cols) = grid_bounds(grid)
  return [(r, c) for r in range(rows) for c in range(cols)]

run()
