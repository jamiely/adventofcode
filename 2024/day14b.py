from math import floor

def run():
  # [path, bounds] = ("day14.small.input", (11, 7))
  [path, bounds] = ("day14.input", (101, 103))
  bots = load(path)
  
  steps = 0
  step_size = 1
  last_positions = {}
  for bot in bots:
    last_positions[bot["id"]] = None
  while True:
    bots_moved = 0
    for bot in bots:
      step(bot, step_size, bounds)
      if last_positions[bot["id"]] is None:
        bots_moved = len(bots)
      elif last_positions[bot["id"]] != bot["pos"]:
        bots_moved += 1
      last_positions[bot["id"]] = bot["pos"]
    # plot(bots, bounds)
    steps += step_size
    print(f"Steps: {steps}")
    if bots_moved < len(bots) / 2:
      print(f"not many bots moved: {bots_moved}")
      break
    if bots_in_line(bots):
      plot(bots, bounds)
      print(f"Found possible christmas tree at {steps}")
      break
    # input("Pause")



def bots_in_line(bots):
  rows = {}
  for bot in bots:
    (x, y) = bot["pos"]
    if y not in rows:
      rows[y] = set()
    rows[y].add(x)

  for (y, entries) in rows.items():
    entries = list(entries)
    entries.sort()
    contiguous = 0
    last = None
    for i in range(len(entries)):
      if last is None:
        last = entries[i]
        continue

      if entries[i] == last + 1 or entries[i] == last:
        contiguous += 1
      else:
        contiguous = 0
      
      # got 10 from trial and error
      if contiguous > 10:
        print(f"Found contiguous at row {y}")
        return True
      
      last = entries[i]

  return False






def count_quads(bots, bounds):
  (bx, by) = bounds

  mx = floor(bx / 2)
  my = floor(by / 2)

  # print(f"mx={mx} my={my}")

  q1 = 0
  q2 = 0
  q3 = 0
  q4 = 0

  for bot in bots:
    (x, y) = bot["pos"]
    # print((x, y))
    if x < mx:
      if y < my:
        q1 += 1
        # print("q1")
      elif y > my:
        q3 += 1
        # print("q3")
    elif x > mx:
      if y < my:
        q2 += 1
        # print("q2")
      elif y > my:
        q4 += 1
        # print("q4")

  quads = [q1, q2, q3, q4]

  prod = q1 * q2 * q3 * q4

  return (quads, prod)

def plot(bots, bounds):
  locs = {}
  for bot in bots:
    if bot["pos"] not in locs:
      locs[bot["pos"]] = 1
    else:
      locs[bot["pos"]] += 1

  grid = []
  (bx, by) = bounds

  counter = 0
  for r in range(by):
    row = [str(counter)]
    for c in range(bx):
      i = (c, r)
      row.append(str(locs[i]) if i in locs else ".")
    grid.append("".join(row))
    counter += 1

  print("\n".join(grid))  

def step(bot, steps, bounds):
  (x, y) = bot["pos"]
  (vx, vy) = bot["vel"]
  (bx, by) = bounds

  x += steps * vx
  y += steps * vy

  x %= bx
  y %= by

  bot["pos"] = (x, y)


def load(path):
  bots = []
  id = 0
  with open(path, "r") as f:
    for line in f:
      # p=0,4 v=3,-3
      [s_position, s_velocity] = line.strip().split(' ')
      (_, px, py) = split_nums(s_position)
      (_, vx, vy) = split_nums(s_velocity)
      bots.append({
        "id": id,
        "pos": (px, py),
        "vel": (vx, vy),
      })
      id += 1
  return bots

def split_nums(str):
  [what, s_coords] = str.split('=')
  [s_x, s_y] = s_coords.split(',')

  return (what, int(s_x), int(s_y))

run()