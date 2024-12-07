def run():
  grid = build_grid("day6.input")
  guard_pos = find_guard(grid)
  print_grid(grid)
  while True:
    (result, guard_pos) = step_grid(grid, guard_pos)
    if result == 'halt':
      break

  positions = count_positions(grid)

  # print_grid(grid)
  print(f"positions: {positions}")

def build_grid(path):
  grid = []
  with open(path, 'r') as f:
    for line in f:
      grid.append(list(line.strip()))
  
  return grid

def step_grid(grid, guard_pos):
  (r, c) = guard_pos
  
  guard = grid[r][c]
  (dr, dc) = get_dir(guard)

  nr = r + dr  
  nc = c + dc

  is_in_bounds = in_bounds(grid, nr, nc)
  if is_in_bounds and has_obstacle(grid, nr, nc):
    grid[r][c] = turn(guard)
    return ('continue', (r, c))
  elif is_in_bounds:
    grid[r][c] = 'X'
    grid[nr][nc] = guard
    return ('continue', (nr, nc))
  else: # out of bounds
    grid[r][c] = 'X'
    return ('halt', None)

  # print_grid(grid)

def count_positions(grid):
  indices = []
  sum = 0
  for r in range(len(grid)):
    for c in range(len(grid[r])):
      if grid[r][c] == 'X':
        indices.append((r, c))
        sum += 1

  print(f"path indices {indices}")

  return sum

def print_grid(grid):
  print("@@@")
  for row in grid:
    print(''.join(row))

def turn(guard):
  turns = ['^', '>', 'v', '<']
  return turns[(turns.index(guard) + 1) % 4]

def has_obstacle(grid, r, c):
  return grid[r][c] == '#'

def in_bounds(grid, r, c):
  if r < 0 or c <0:
    return False  

  if r >= len(grid):
    return False

  if c >= len(grid[r]):
    return False

  return True

def get_dir(guard):
  match guard:
    case '^':
      return (-1, 0)
    case '>':
      return (0, 1)
    case '<':
      return (0, -1)
    case 'v':
      return (1, 0)
    case _:
      raise f"invalid guard: {guard}"

def find_guard(grid):
  for r in range(len(grid)):
    for c in range(len(grid[r])):
      # print(f"grid[{r}][{c}] = {grid[r][c]} matches? {grid[r][c] == "^"}")
      if grid[r][c] == "^":
        return (r, c)

  return None

run()
