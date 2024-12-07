# read from day1.py

from io import open

sum = 0

list1 = []
list2 = {}

with open("day1.input", "r") as f:
    input = f.readlines()
    for line in input:
        parts = line.split("   ")

        
        try:
            num1 = int(parts[0])
            num2 = int(parts[1])

            list1.append(num1)
            list2[num2] = list2.get(num2, 0) + 1
        except (ValueError, IndexError):
            print(f"Error parsing line: {line.strip()}")
            continue

for num1 in list1:
    sum += num1 * list2.get(num1, 0)

print(sum)

