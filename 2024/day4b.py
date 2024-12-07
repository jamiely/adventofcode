from io import open

def run():
  board = []
  with open("day4.input", "r") as f:
    board = f.readlines()

  count = 0
  for row in range(len(board)):
    for col in range(len(board[row])):
      if check_index_for_word(board, row, col):
        print(f"row={row} col={col}")
        count += 1

  print(f"total count: {count}")
  
def check_index_for_word(board, row, col):
  c = get(board, row, col)
  if c != 'A':
    return False

  directions = [
    [(-1, -1), (1, 1)],
    [(-1, 1), (1, -1)],
  ]

  for dirs in directions:
    cs = [get(board, row + dir[0], col + dir[1]) for dir in dirs]
    cs.sort()
    
    if cs[0] == 'M' and cs[1] == 'S':
      continue
    else:
      return False

  return True


def get(board, row, col):
  if row < 0 or col < 0:
    return '?'
  
  try:
    return board[row][col]
  except IndexError:
    return '?'

run()
