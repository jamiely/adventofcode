def run():
  grid = load("day12.input")
  (regions, sides) = process(grid)
  sum = 0
  for region in regions:
    if len(region) == 0:
      continue

    (r, c) = next(iter(region))
    plant = grid[r][c]

    side_count = get_sides(region, sides)
    area = len(region)
    product = area * side_count
    # print(f"Plant {plant} {area} * {side_count} = {product}")
    sum += product

  print(sum)

def get_sides(region, sides):
  # the outer plants are all those whose sides set is not-empty

  # we can combine sides by direction
  all = {}

  # add each side as a member
  for coord in region:
    if coord not in sides:
      continue

    for side in sides[coord]:
      if side not in all:
        all[side] = []

      all[side].append(coord)

  count_ud = count_up_down_sides(all)
  count_lr = count_left_right_sides(all)

  # print(f"ud: {count_ud} lr: {count_lr}")

  return count_ud + count_lr  

  

def count_left_right_sides(all):
  all_count = 0
  for dir in ['L', 'R']:
    count = 0
    coords = all[dir]
    sort_by_col_then_row(coords)
    # print(f"Sorted {dir}: {coords}")
    last = None
    for coord in coords:
      if last is None:
        last = coord
        count += 1
        continue

      if coord[1] != last[1]:
        # columns are different
        count += 1
      elif last[0] + 1 != coord[0]:
        # row does not increment by 1
        count += 1
      else:
        # continue side
        pass
      last = coord
    # print(f"dir {dir} count {count}")
    all_count += count
  return all_count

  

def count_up_down_sides(all):
  all_count = 0  

  for dir in ['U', 'D']:    
    count = 0
    coords = all[dir]
    sort_by_row_then_col(coords)
    # print(f"Sorted {dir}: {coords}")
    last = None
    
    for coord in coords:
      if last is None:
        last = coord
        count += 1
        continue

      if coord[0] != last[0]:
        # rows are different
        count += 1
      elif last[1] + 1 != coord[1]:
        # col does not increment by 1
        count += 1
      else:
        # continue side
        pass
      last = coord

    # print(f"Side {dir} count={count}")
    all_count += count
  return all_count

def sort_by_col_then_row(items):
  # we have to sort by the last thing first
  items.sort(key=lambda item: item[0]) # sort by row
  items.sort(key=lambda item: item[1]) # sort by column

def sort_by_row_then_col(items):
  # we have to sort by the last thing first
  items.sort(key=lambda item: item[1]) # sort by column
  items.sort(key=lambda item: item[0]) # sort by row


  # now attempt to merge all the sets in a side

  return sum
    

def load(path):
  with open(path, "r") as f:
    return [list(line.strip()) for line in f]

def process(grid):
  seen = set()
  sides = {}
  regions = []
  for coord in grid_indices(grid):
    if coord in seen:
      continue

    # find the contiguous region by flood fill
    region = set()
    # print(coord)
    flood(grid, coord, seen, region, sides)
    regions.append(region)
    # print(f"region {grid[coord[0]][coord[1]]}: {region}")

  return (regions, sides)
    
def flood(grid, coord, seen, region, sides, plant = None):
  if coord in seen:
    return
    
  (r, c) = coord

  if plant is None:
    plant = grid[r][c]

  if plant != grid[r][c]:
    return

  seen.add(coord)
  region.add(coord)

  directions = get_directions()
  for (neighbor_plant, neighbor_coord, neighbor_dir) in get_neighbors(grid, r, c):
    if neighbor_plant != plant:
      continue

    directions.remove(neighbor_dir)

    flood(grid, neighbor_coord, seen, region, sides, plant)  

  sides[coord] = directions

def get_directions():
  return set(['U', 'D', 'L', 'R'])
  
def grid_bounds(grid):
  return (len(grid), len(grid[0]))

def grid_indices(grid):
  (rows, cols) = grid_bounds(grid)
  return [(r, c) for r in range(rows) for c in range(cols)]

def get_neighbors(grid, r, c):
  (rows, cols) = grid_bounds(grid)

  candidates = [(r + 1, c, 'D'), (r - 1, c, 'U'), (r, c + 1, 'R'), (r, c - 1, 'L')]

  return [(grid[r][c], (r, c), dir) for (r, c, dir) in candidates 
          if r >= 0 and c >= 0 and r < rows and c < cols]

run()
