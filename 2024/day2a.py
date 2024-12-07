# read from day1.py

from io import open

safe_count = 0

with open("day2.input", "r") as f:
    for line in f:
        first, second, *rest = [int(x) for x in line.split(" ")]

        diff = second - first
        adiff = abs(diff)
        if diff == 0:
            continue
        if adiff < 1: 
            continue
        if adiff > 3:
            continue
        
        increasing = diff > 0

        last = second
        is_safe = True
        for num in rest:
          diff = num - last
          last = num
          adiff = abs(diff)

          if increasing:
              if diff <= 0:
                  is_safe = False
                  break
          else: # decreasing
              if diff >= 0:
                  is_safe = False
                  break
              

          if adiff < 1:
              is_safe = False
              break

          elif adiff > 3:
              is_safe = False
              break

        if is_safe:
            safe_count += 1
            print(f"Safe: {first}, {second}, {rest}")

print(safe_count)
          
          
          
            
        