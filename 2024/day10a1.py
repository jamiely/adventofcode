from io import open

def run():
  grid = load("day10.small.input")
  result = process(grid)

  print(result)

def load(path):
  with open(path, "r") as f:
    return [[{
      "display": int(display),
      "score": 0,
    } for display in list(line.strip())] for line in f]
  
def process(grid):
  heads = 0
  for i in reversed(range(10)):
    for (r, c) in grid_indices(grid):
      if grid[r][c]["display"] != i:
        continue


      if i == 9:
        score = 1
      else:
        # check to see if it neighbors any existing nodes
        score = sum(neighbor["score"] for neighbor in get_neighbors(grid, r, c, i + 1))
        
      grid[r][c]["score"] = score
      
      print(f"i={i} ({r}, {c}) score={score}")

      if i == 0:
        heads += grid[r][c]["score"]

  return heads

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
