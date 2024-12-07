from io import open

def run():
  board = []
  with open("day4.input", "r") as f:
    board = f.readlines()

  count = 0
  for row in range(len(board)):
    for col in range(len(board[row])):
      this_count = check_index_for_word(board, row, col, 'XMAS', 0)
      if this_count > 0:
        print(f"row={row} col={col} this count {this_count}")
      count += this_count
      

  print(f"total count: {count}")
  
def check_index_for_word(board, row, col, word, word_index):
  directions = [ [-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, 1], [1, 0], [1, -1] ]

  count = 0
  for dir in directions:
    if check_index_for_word_in_dir(board, row, col, word, word_index, dir):
      count += 1
  
  return count

def check_index_for_word_in_dir(board, row, col, word, word_index, dir):
  if len(word) <= word_index:
    return True
  if col < 0:
    return False
  if row < 0:
    return False

  try:
    c = board[row][col]
  except IndexError:
    return False

  if c != word[word_index]:
    return False

  print(f"{col},{row} {c}")  
  return check_index_for_word_in_dir(board, row + dir[0], col + dir[1], word, word_index + 1, dir)
  

run()
