from io import open
import re

def run():
  sum = 0
  mults = []
  with open("day3.input", "r") as f:
    for line in f:
      mults += get_mults(line)

  enabled = True
  for mult in mults:
    op = mult[0]
    if op == 'mul' and enabled:
      [_, a, b] = mult
      sum += a * b
    elif op == 'disable':
      enabled = False
    elif op == 'enable':
      enabled = True

  print(f"sum: {sum}")

def get_mults(line):
  instances = re.finditer(r"(mul\((\d+),(\d+)\)|do\(\)|don't\(\))", line)
  results = []

  for x in instances:
    if x.group().startswith("m"):
      results.append(['mul', int(x.group(2)), int(x.group(3))])
    elif x.group().startswith("don"):
      results.append(['disable'])
    elif x.group().startswith("do"):
      results.append(['enable'])
              
  return results

def process_mult(mult):
  (a, b) = mult
  return a * b

run()