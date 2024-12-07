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
  print(f"processed: {processed}")
  results = [get_middle(update) for update in processed if update is not None]
  print(f"sum: {sum(results)}")

def get_middle(update):
  if update is None:
    return None

  return int(update[int(len(update) / 2)])
    
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

run()