from io import open
import math
import re

def run():
  with open("day3.input", "r") as f:
    mults = []
    dos = []
    for line in f:
      mults += get_mults(line)
      dos += get_dos_donts(line)

  # print(f"mults: {mults}\n dos: {dos}")
  sum = process(mults, dos)

  print(f"Sum is {sum}")
      
def process(mults, dos):
  j = 0
  sum = 0

  enabled = True
  for mult in mults:
    start_position = mult[0]

    if len(dos) > j:
      (dos_pos, dos_enabled) = dos[j]
    else:
      dos_pos = math.inf

    print(f"Start: {start_position}")

    if start_position >= dos_pos:
      enabled = dos_enabled
      print(f"Set enabled to {dos_enabled}")
      j += 1

    if enabled:
      sum += process_mult(mult)

  return sum

def get_mults(line):
  return [(x.span()[0], int(x.group(1)), int(x.group(2))) for x in re.finditer(r'mul\((\d+),(\d+)\)', line)]

def get_dos_donts(line):
  return [(x.span()[0], x.group() == 'do()') for x in re.finditer(r"do\(\)|don't\(\)", line)]


def process_mult(mult):
  (s, a, b) = mult
  return a * b

run()