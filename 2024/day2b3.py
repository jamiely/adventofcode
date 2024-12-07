
def run():
  from io import open
  with open("day2test.input", "r") as f:
    safe_count = 0
    for line in f:
      if is_safe(line):
        safe_count+=1
    print(f"Safe count is {safe_count}")

def is_safe(line):
  nums = [int(x) for x in line.split(' ')]
  safe_result = nums_safe(nums, None, 0, 1, None)
  if safe_result["safe"] and safe_result["without"] is not None:
    print(f"Safe #{nums} #{safe_result}")
  return safe_result["safe"]
  
def nums_safe(nums, direction, last_index, current_index, without):
  if current_index >= len(nums):
    return { "safe": True, "without": without }

  while last_index == without:
    last_index += 1
  while current_index == without or current_index <= last_index:
    current_index += 1

  if last_index >= len(nums) or current_index >= len(nums):
    return { "safe": True, "without": without }

  last = nums[last_index]
  current = nums[current_index]

  diff = current - last
  ad = abs(diff)

  # if without is not None:
  print(f"nums=#{nums} without={without} direction={direction} last={last} current={current} diff={diff} adiff={ad}")

  bad = False

  if ad == 0:
    bad = True
  
  if bad:
    pass
  elif direction is None:
    if diff < 0:
      return nums_safe(nums, 'dec', last_index, current_index, without)
    elif diff > 0:
      return nums_safe(nums, 'inc', last_index, current_index, without)


  if bad:
    pass
  elif direction == 'inc' and diff < 0:
    bad = True
  elif direction == 'dec' and diff > 0:
    bad = True

  bad = bad or ad < 1 or ad > 3

  if bad:
    # we already tried without a number
    if without:
      return { "safe": False, "without": without }

    # try skipping the current number
    current_result = nums_safe(nums, direction, last_index, current_index + 1, current_index)
    if current_result["safe"]:
      return { "safe": True, "without": without }
    
    # skip the last number
    return nums_safe(nums, direction, last_index + 1, last_index + 2, last_index)
  
  return nums_safe(nums, direction, current_index, current_index + 1, without)

run()