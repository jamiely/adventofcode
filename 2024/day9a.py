from io import open

def run():
  result = load("day9.input")
  head = move(result)
  entries = ll_to_list(head)
  # display_entries(entries)
  sum = calc_entries(entries)
  print(f"Sum: {sum}")

def calc_entries(entries):
  sum = 0
  counter = 0
  for item in entries:
    if item["type"] == "free":
      break
    for i in range(item["blocks"]):
      addend = counter + i
      result = addend * item["id"]
      # print(f"#{addend} * {item["id"]} = {result}")
      sum += result
    counter += item["blocks"]

  return sum

def display_entries(entries):
  parts = []
  for entry in entries:
    if entry["type"] == 'free':
      item = '.' * entry["blocks"]
    else:
      item = str(entry["id"]) * entry['blocks']

    parts.append(item)
  print("".join(parts))

def move(_entries):
  (head, foot) = list_to_ll(_entries)

  # pointers
  forward = head
  backward = foot

  while True:
    if forward is None:
      break
    if backward is None:
      break
    if forward == backward:
      break

    f_entry = forward.data
    b_entry = backward.data

    if f_entry["type"] != "free":
      forward = forward.next
      continue
    if b_entry["type"] != "used":
      backward = backward.prev
      continue
    # now attempt to fill forward with backward

    if b_entry["blocks"] > f_entry["blocks"]:
      # there were too many blocks
      f_entry["id"] = b_entry["id"]
      f_entry["type"] = "used"
      b_entry["blocks"] -= f_entry["blocks"]
      # find more empty space
      forward = forward.next
    elif b_entry["blocks"] < f_entry["blocks"]:
      # there were too few blocks
      new_node = Node({
        "id": b_entry["id"],
        "type": "used",
        "blocks": b_entry["blocks"],
      })
      insert_before(
        forward,
        new_node
      )
      if forward == head:
        head = new_node
      # subtract the space we used
      f_entry["blocks"] -= b_entry["blocks"]
      # clear the old space
      backward = backward.prev
      delete_node(backward.next)
    else:
      # they are the same number of blocks
      f_entry["type"] = "used"
      f_entry["id"] = b_entry["id"]
      forward = forward.next
      backward = backward.prev
      delete_node(backward.next)

  return head

def load(path):
  contents = open(path, "r").read()
  counter = 0
  file_counter = 0
  entries = []
  for entry in list(contents):
    type = "used" if counter % 2 == 0 else "free"
    result = process(entry, type)
    if type == "used":
      result["id"] = file_counter
      file_counter += 1
    counter += 1

    entries.append(result)

  return entries

def process(entry, type):
  if type == 'free':
    return {
      "type": type,
      "blocks": int(entry),
    }
  
  return {
    # assign this later
    "id": None,
    "type": "used",
    "blocks": int(entry),
  }

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

run()
