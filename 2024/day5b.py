from io import open

def run():
  ordering = []
  updates = []

  with open("day5.input") as f:
    done_ordering = False
    for line in f:
      if done_ordering:
        updates.append(line)
      elif line == "\n":
        done_ordering = True
      else:
        ordering.append(line)

  order_results = process_ordering(ordering)
  # print(f"Order: {order_results}")
  processed = process_updates(updates, order_results)
  # print(f"processed: {processed}")
  results = [get_middle(update) for update in processed if update is not None]
  print(f"sum: {sum(results)}")

def get_middle(update):
  if update is None:
    return None

  num = int(update[int(len(update) / 2)])
  print(f"middle num: {num}")
  return num
    
def process_ordering(ordering):
  order = {}
  for item in ordering:
    [a, b] = item.strip().split("|")
    if b not in order:
      order[b] = set()
    order[b].add(a)
  
  return order

def process_updates(updates, order):
  results = []
  for raw in updates:
    update = raw.strip().split(',')
    if is_valid_update(update, order):
      # print(f"valid update: {update}")
      # results.append(update)
      pass
    else:
      # print(f"pre-sort: {update}")
      sort_update(update, order)
      cp1 = update.copy()
      sort_update(update, order)

      if cp1 != update:
        print(f"THERE WAS A PROBLEM, sort is not stable: cp1={cp1} update={update}")
        return

      # sort_update(update, order)
      print(f"post-sort: {update}")
      if not is_valid_update(update, order):
        print(f"THERE WAS A PROBLEM: {update}")
        return
      results.append(update)

  return results

def is_valid_update(update, order):
  # print(f"is valid: {update}")
  seen = set()
  for index in range(len(update)):
    num = update[index]
    if num in order:
      n_index = index + 1
      while n_index < len(update):
        dependency = update[n_index]
        if dependency in order[num]:
          if dependency not in seen:
            # print(f"num={num} dependency={dependency} not in seen {seen} order={order[num]}")
            return False
        n_index += 1
    seen.add(num)
  
  return True

def sort_update(update, ordering):
  # print(f"Sorting update: {update}")
  # move each number back before the last dependency
  move_index = 1
  i = 0
  while move_index is not None and i < len(update):
    move_index = None
    num = update[i]
    if num not in ordering:
      # print(f"num not in ordering {num}")
      i += 1
      move_index = 0
      continue

    order = ordering[num]

    # print(f"move_index={move_index} i={i} num={num} order={order}")
    
    # move as far back as needed
    for j in range(len(update)):
      if update[j] in order:
        move_index = j + 1
        # print(f"i={i} j={j} num={num} depends on {update[j]}, update={update}, order={order}")

    if move_index is None or move_index == i:
      i += 1
      move_index = 0 # just to maintain loop condition
      continue

    # move the item
    update.insert(move_index, num)
    update.pop(i)
    i = 0
    # print(f"moved update[{i}]={num} to {move_index}")




run()