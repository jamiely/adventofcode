# read from day1.py

from io import open
import copy

def run():
    safe_count = 0

    with open("day2.input", "r") as f:
        for line in f:
            rest = [int(x) for x in line.split(" ")]
            if line_safe(rest):
                safe_count += 1
            elif attempt_recover(rest):
                safe_count += 1
                
    print(safe_count)

def attempt_recover(orig):
    for i in range(len(orig)):
        line = copy.copy(orig)
        line.pop(i)
        if line_safe(line):
            return True
    return False

            
def line_safe(rest):
    direction = None
    last = None

    for num in rest:
        if last is None:
            last = num
            continue

        diff = num - last
        last = num
        adiff = abs(diff)

        if diff == 0:
            return False

        if direction is None:
            direction = 'inc' if diff > 0 else 'dec'

        if direction == 'inc':
            if diff <= 0:
                return False
        elif diff >= 0:
            return False

        if adiff < 1:
            return False

        elif adiff > 3:
            return False
    
    return True

run()