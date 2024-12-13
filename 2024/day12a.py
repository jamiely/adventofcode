def run():
  grid = load("day12.input")
  (regions, neighbors) = process(grid)
  sum = 0
  for region in regions:
    per = perimeter(region, neighbors)
    area = len(region)
    product = area * per
    # print(f"{area} * {per} = {product}")
    sum += product

  print(sum)

def perimeter(region, neighbors):
  sum = 0
  for coord in region:
    sum += (4 - neighbors[coord])

  return sum
    

def load(path):
  with open(path, "r") as f:
    return [list(line.strip()) for line in f]

def process(grid):
  seen = set()
  neighbors = {}
  regions = []
  for coord in grid_indices(grid):
    if coord in seen:
      continue

    # find the contiguous region by flood fill
    region = set()
    regions.append(region)
    # print(coord)
    flood(grid, coord, seen, region, neighbors)
    # print(f"region {grid[coord[0]][coord[1]]}: {region}")

  return (regions, neighbors)
    
def flood(grid, coord, seen, region, neighbors, plant = None):
  if coord in seen:
    return
    
  (r, c) = coord

  if plant is None:
    plant = grid[r][c]

  if plant != grid[r][c]:
    return

  seen.add(coord)
  region.add(coord)

  neighbor_count = 0
  for (neighbor_plant, neighbor_coord) in get_neighbors(grid, r, c):
    if neighbor_plant != plant:
      continue

    neighbor_count += 1

    flood(grid, neighbor_coord, seen, region, neighbors, plant)  

  neighbors[coord] = neighbor_count
  
def grid_bounds(grid):
  return (len(grid), len(grid[0]))

def grid_indices(grid):
  (rows, cols) = grid_bounds(grid)
  return [(r, c) for r in range(rows) for c in range(cols)]

def get_neighbors(grid, r, c):
  (rows, cols) = grid_bounds(grid)

  candidates = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]

  return [(grid[r][c], (r, c)) for (r, c) in candidates 
          if r >= 0 and c >= 0 and r < rows and c < cols]

run()
