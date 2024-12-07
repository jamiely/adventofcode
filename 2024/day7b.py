from io import open

def run():
  sum = 0
  with open("day7.input", "r") as f:
    for line in f:
      (correct, test_val) = process_line(line)
      if correct:
        sum += test_val
    print(f"Sum: {sum}")
      
def process_line(line):
  print(f"line: {line}")
  [str_test_val, str_operands] = line.strip().split(':')
  test_val = int(str_test_val)
  operands = [int(x) for x in str_operands.strip().split(' ')]
  result = set(compute(operands))
  return (test_val in result, test_val)

OPERATORS = [
  lambda a, b: a + b,
  lambda a, b: a * b,
  lambda a, b: int(str(a) + str(b)),
]

def compute(operands):
  global OPERATORS

  if len(operands) == 1:
    return [operands[0]]

  [first, second, *rest] = operands

  compute_results = []
  for op in OPERATORS:
    next_val = op(first, second)
    compute_results += compute([next_val, *rest])
    
  return compute_results

run()