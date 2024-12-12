def run():
  nums = list_to_ll([int(x) for x in "5688 62084 2 3248809 179 79 0 172169".split(" ")])
  # print_ll(nums[0])

  head = process(nums)

  print(f"length: {len(ll_to_list(head))}")
  # print_ll(head)

def process(ll):
  (head, _) = ll
  for i in range(25):
    head = step(head)
    # print_ll(head)
  return head

def step(head):
  curr = head
  while curr:
    # print(f"curr.data={curr.data}")
    if curr.data == 0:
      curr.data = 1
    elif len(str(curr.data)) % 2 == 0:
      # even
      val = str(curr.data)
      length = len(val)
      mid = int(length/2)
      node = Node(int(val[0:mid]))
      insert_before(curr, node)
      if curr == head:
        head = node
      curr.data = int(val[mid:length])
    else:
      curr.data = curr.data * 2024

    curr = curr.next

  return head


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