def run():
  nums = [int(x) for x in "5688 62084 2 3248809 179 79 0 172169".split(" ")]
  # print_ll(nums[0])

  process(nums)

def process(nums):
  result = step(nums, 75)
  print(f"result: {result}")

def step(nums, steps):
  memory = {}
  sum = 0
  for num in nums:
    sum += step_num(num, steps, memory)

  return sum

def step_num(num, steps, memory):
  # print(f"num={num} steps={steps}")
  if num not in memory:
    memory[num] = {}
  elif steps in memory[num]:
    return memory[num][steps]

  if steps == 0:
    return 1
  
  if num == 0:
    result = step_num(1, steps - 1, memory)
    
    memory[num][steps] = result

    return result

  elif len(str(num)) % 2 == 0:
    # even
    val = str(num)
    length = len(val)
    mid = int(length/2)
    v1 = int(val[0:mid])
    v2 = int(val[mid:length])

    result = step_num(v1, steps - 1, memory) + step_num(v2, steps - 1, memory)
    memory[num][steps] = result
    return result

  memory[num][steps] = step_num(num * 2024, steps - 1, memory)

  return memory[num][steps]


class Node:
  def __init__(self, data, prev = None, next = None):
    self.data = data
    self.prev = prev
    if prev is not None:
      prev.next = self
    self.next = next

def list_to_ll(entries):
  last = None
  head = None
  for entry in entries:
    if last is None:
      entry = Node(entry, None)
      head = last = entry
      continue

    entry = Node(entry, last)
    last = entry

  return (head, last)

def insert_before(node, new_node):
  new_node.prev = node.prev
  new_node.next = node

  if node.prev is not None:
    node.prev.next = new_node
  node.prev = new_node

def delete_node(node):
  if node is None:
    return
  node.prev.next = node.next
  if node.next is not None:
    node.next.prev = node.prev

def ll_to_list(head):
  entries = []
  while head:
    entries.append(head.data)
    head = head.next

  return entries

def print_ll(head):
  entries = []
  while head:
    entries.append(str(head.data))
    head = head.next

  print(" ".join(entries))

run()