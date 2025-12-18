dial = 50
#print(f"Starting at {dial}")
zero_count = 0
with open("input1.txt") as input_file:
  for line in input_file:
    direction = line[0]
    str_steps = line[1:]
    if str_steps == "": continue
    steps = int(line[1:])
    sign = -1 if direction == "L" else 1
    dial = (dial + sign * steps) % 100
    #print(f"Moving {direction} {steps} steps to {dial}")
    if dial == 0:
      zero_count += 1

print(f"{zero_count} zeros")
