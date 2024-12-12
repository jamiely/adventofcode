
from io import open

def run():
  grid = load_grid("day8.input")
  # display_grid(grid)
  (_, antinodes) = process_antinodes(grid)
  # display_grid(grid)
  print(f"antinode count: {len(antinodes)}")
  

def process_antinodes(grid):
  freq_chunks = frequency_chunks(grid)

  nodes = []
  for _, coords in freq_chunks.items():
    _nodes = get_possible_antinodes_from_list(coords)
    nodes += _nodes

  nodes = set(filter(lambda p: coord_in_bounds(grid, p), set(nodes)))

  for entry in grid_entries(grid):
    if entry["coords"] not in nodes:
      continue

    entry["antinodes"] = True

  return (freq_chunks, nodes)

def coord_in_bounds(grid, coord):
  (r, c) = coord

  if r < 0 or c < 0:
    return False
  
  if r >= len(grid) or c >= len(grid[r]):
    return False
  
  return True

def get_possible_antinodes_from_list(coords):
  antinodes = []
  for i in range(len(coords)):
    for j in range(i + 1, len(coords)):
      antinodes += get_antinodes(coords[i], coords[j])
  return antinodes

def get_antinodes(coord1, coord2):
  """Uses the slope between the two coordinates to find antinodes"""

  (c1r, c1c) = coord1
  (c2r, c2c) = coord2
  dr = c1r - c2r
  dc = c1c - c2c

  n1 = (c1r + dr, c1c + dc)
  n2 = (c2r - dr, c2c - dc)

  return [n1, n2]

def frequency_chunks(grid):
  """Chunks antenna by frequency"""
  chunks = {}
  for entry in grid_entries(grid):
    freq = entry["frequency"]
    if freq is None:
      continue

    if freq not in chunks:
      chunks[freq] = []

    chunks[freq].append(entry["coords"])

  return chunks

def grid_positions(grid):
  return [(r, c) for r in range(len(grid)) for c in range(len(grid[r]))]

def grid_entries(grid):
  return [grid[r][c] for (r, c) in grid_positions(grid)]

def display_grid(grid):
  print("@@@@")
  for row in grid:
    display = []
    for item in row:
      if item["antinodes"]:
        display.append('#')
      else:
        display.append(item["original"])
    print("".join(display))

def load_grid(path):
  with open(path, "r") as f:
    r = 0
    rows = []
    for line in f:
      c = 0
      row = []
      for char in list(line.strip()):
        entry = load_grid_char(char)
        entry["coords"] = (r, c)
        row.append(entry)
        c+=1

      rows.append(row)
      r+=1
    return rows

def load_grid_char(char):
  is_empty = char == '.'
  has_antenna = not is_empty
  frequency = char if has_antenna else None
  return {
    "original": char,
    "is_empty": is_empty,
    "frequency": frequency,
    "antinodes": False,
  }

run()
