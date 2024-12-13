from io import open
import re

CATEGORY_A = "Button A"
CATEGORY_B = "Button B"
BUTTONS = set([CATEGORY_A, CATEGORY_B])
CATEGORY_PRIZE = "Prize"
CATEGORIES = set([CATEGORY_PRIZE]) | BUTTONS

def run():
  machines = load("day13.input")
  for machine in machines:
    # positions are wrong, update them
    machine[CATEGORY_PRIZE]["X"] += 10000000000000
    machine[CATEGORY_PRIZE]["Y"] += 10000000000000
  sum = 0
  for machine in machines:
    matrices = machine_matrices(machine)
    # print(f"machine: {machine} matrices: {matrices}")
    presses = get_presses(matrices)
    if presses is None:
      print(f"no combination possible for machine {machine["id"]}")
      continue

    sum += calc_presses(presses)

    print(presses)
  print(sum)

def calc_presses(presses):
  [a, b] = presses
  return a*3 + b
    

def machine_matrices(machine):
  A = [[machine[CATEGORY_A]["X"], machine[CATEGORY_B]["X"]],
          [machine[CATEGORY_A]["Y"], machine[CATEGORY_B]["Y"]]]
  
  a, b, c, d = A[0][0], A[0][1], A[1][0], A[1][1]
    
  # Calculate determinant
  det = a * d - b * c
  invertible = det != 0
  
  # Adjugate matrix
  adj = [[d, -b], [-c, a]]
  
  # Inverse matrix
  if invertible:
    inv = [[adj[i][j] / det for j in range(2)] for i in range(2)]
  else:
    inv = None

  b_matrix = [[machine[CATEGORY_PRIZE]["X"]], [machine[CATEGORY_PRIZE]["Y"]]]

  return {
    "A": A,
    "A^-1": inv,
    "b": b_matrix,
  }

def get_presses(matrices):
  Ainv = matrices["A^-1"]
  if Ainv is None:
    return None

  b = matrices["b"]

  presses_A = Ainv[0][0] * b[0][0] + Ainv[0][1] * b[1][0]
  presses_B = Ainv[1][0] * b[0][0] + Ainv[1][1] * b[1][0]

  A = matrices["A"]
  a, b, c, d = A[0][0], A[0][1], A[1][0], A[1][1]

  presses_A = round(presses_A)
  presses_B = round(presses_B)

  maybeX = a * presses_A + b * presses_B
  maybeY = c * presses_A + d * presses_B

  good = abs(matrices["b"][0][0] - maybeX) < 0.001 and abs(matrices["b"][1][0] - maybeY) < 0.001

  # results = []
  # for num in [presses_A, presses_B]:
  #   if num < 0:
  #     # cannot press negative times
  #     continue
  #   elif abs(num - round(num)) < 0.00001:
  #     results.append(int(num))
  #   else:
  #     print(f"invalid: {num}")

  # if len(results) < 2:
  #   return None
  if not good:
    return None

  return [presses_A, presses_B]

def load(path):
  machine = {"id": 0}
  machines = [machine]
  with open(path, "r") as f:
    for line in f:
      line = line.strip()

      if line == "":
        machine = {"id": machine["id"] + 1}
        machines.append(machine)
        continue

      [category, nums] = line.split(": ")
      if category not in CATEGORIES:
        raise 'problem'

      machine[category] = {}
      for part in nums.split(", "):
        result = re.split(r'(?:=|\+)', part)
        [var, num] = result
        machine[category][var] = int(num)

  return machines


run()