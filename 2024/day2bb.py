# read from day1.py

from io import open

safe_count = 0

def is_safe(rest):
    direction = None
    bad_count = 0
    last = None

    for num in rest:
        if last is None:
            last = num
            continue
        
        diff = num - last
        adiff = abs(diff)

        if adiff == 0:
            bad_count += 1
        
        if bad_count > 1:
            return False

        if direction is None:
            if bad_count > 0:
                return False
            elif diff > 0:
                direction = 'i'
            elif diff < 0:
                direction = 'd'
            else:
                continue
                
        if direction:
        



with open("day2.input", "r") as f:
    for line in f:
        rest = [int(x) for x in line.split(" ")]
        if is_safe(rest):
            safe_count += 1
        