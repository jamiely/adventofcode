from io import open
import re

def run():
  with open("day3.input", "r") as f:
    sum = 0
    for line in f:
      for mult in get_mults(line):
        result = process_mult(mult)
        sum += result
        print(f"Mult `{mult}` = {result}. New sum={sum}")

def get_mults(line):
  return [(int(x.group(1)), int(x.group(2))) for x in re.finditer(r'mul\((\d+),(\d+)\)', line)]

def process_mult(mult):
  (a, b) = mult
  return a * b

run()