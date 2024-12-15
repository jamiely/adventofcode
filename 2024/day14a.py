from math import floor

def run():
  # [path, bounds] = ("day14.small.input", (11, 7))
  [path, bounds] = ("day14.input", (101, 103))
  bots = load(path)
  
  for bot in bots:
    step(bot, 100, bounds)
  # plot(bots, bounds)

  (quads, prod) = count_quads(bots, bounds)

  print(f"prod={prod} quads={quads}")

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
  for r in range(by):
    row = []
    for c in range(bx):
      i = (c, r)
      row.append(str(locs[i]) if i in locs else ".")
    grid.append("".join(row))

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