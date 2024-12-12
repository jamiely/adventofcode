from io import open

def run():
  result = load("day9.input")
  # display_entries(result)
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
      counter += item["blocks"]
      continue
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
  backward = foot
  last = head
  count = 0

  while backward:
    # display_entries(ll_to_list(head))

    # start at the last free space
    forward = last
    # should be set to the first free space
    next_last = None
    # print(f"Backward: {backward}")
    
    b_entry = backward.data
    if b_entry["type"] != "used":
      backward = backward.prev
      continue

    while forward and forward != backward:
      f_entry = forward.data
      if f_entry["type"] != "free":
        forward = forward.next
        continue
      if next_last is None:
        next_last = forward
      if f_entry["blocks"] < b_entry["blocks"]:
        forward = forward.next
        continue
      else:
        # file can be moved
        b_prev = backward.prev
        insert_before(backward, Node({
          "type": "free",
          "blocks": b_entry["blocks"],
        }))
        delete_node(backward)
        insert_before(forward, backward)
        f_entry["blocks"] -= b_entry["blocks"]
        backward = b_prev
        if f_entry["blocks"] == 0:
          delete_node(forward)
        # print(f"f_entry after change: {f_entry}")
        break
        
    # last = next_last or head
    last = head
    # print(f"last: {last}")
    count += 1
    if backward is not None:
      backward = backward.prev
    # if count > 6:
    #   break
    
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
  def __str__(self):
    return f"[Node prev={"X" if self.prev else "None"} {self.data} next={"X" if self.next else "None"}]"

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
  if node.prev is not None:
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
