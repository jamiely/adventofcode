# read from day1.py

from io import open

safe_count = 0

with open("day2.input", "r") as f:
    for line in f:
        rest = [int(x) for x in line.split(" ")]
        
        direction = None
        is_safe = True
        last = None
        bad_count = 0
        # print(f"@@@@ #{rest}")
        for num in rest:
          last_bad = False
          if last is None:
              last = num
              continue

          diff = num - last
          adiff = abs(diff)

          if adiff == 0:
            bad_count += 1
            is_safe = False
            print(f"same number {rest} bad_count={bad_count}")
            # do not set the last number since we're skipping
            continue
          
        #   print(f"adiff={adiff} last={last} num={num}")
        
          if direction is None:
              if diff < 0:
                  direction = 'd'
              else:
                  direction = 'i'
            #   print(f"set direction to {direction}")

          if direction == 'i':
              if diff <= 0:
                  last_bad = True
                  print(f"a diff={diff} last={last} num={num}")
          else: # decreasing
              if diff >= 0:
                  last_bad = True
                  print("b")
              
          if adiff < 1:
              last_bad = True
              print("c")

          elif adiff > 3:
              last_bad = True
              print(f"d diff={diff} last={last} num={num}")

          if last_bad:
              print(f"last_bad True bad_count={bad_count} last={last} num={num} adiff={adiff}")
              bad_count += 1
              is_safe = False
              print(f"last_bad True bad_count={bad_count} last={last} num={num} adiff={adiff}")
          else:
              last = num
            #   print(f"set last to {num} ")

        if is_safe or bad_count < 2:
            safe_count += 1
            if bad_count > 0:
                print(f"Safe: bad_count={bad_count} {rest}")

print(safe_count)
          
          
          
            
        