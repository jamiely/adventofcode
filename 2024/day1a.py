# read from day1.py

from io import open

sum = 0

list1 = []
list2 = []

with open("day1.input", "r") as f:
    input = f.readlines()
    for line in input:
        parts = line.split("   ")

        
        try:
            num1 = int(parts[0])
            num2 = int(parts[1])

            list1.append(num1)
            list2.append(num2)
        except (ValueError, IndexError):
            print(f"Error parsing line: {line.strip()}")
            continue

list1.sort()
list2.sort()

for pair in zip(list1, list2):
    num1, num2 = pair
    sum += abs(num1 - num2)

print(sum)

