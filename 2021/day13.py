import copy
lines = open('day13.input', 'r').readlines()

i = 0
points = []
while len(lines) > i:
    if lines[i] == '\n':
        break

    x, y = lines[i].strip().split(',')
    point = (int(x), int(y))
    points.append(point)

    i += 1

# print(points)

folds = []
while len(lines) > i:
    if not lines[i].startswith('fold'):
        i += 1
        continue
    _, _, coord = lines[i].strip().split(' ')
    axis, value = coord.split('=')
    folds.append((axis, int(value)))
    i += 1

print(folds)

max_x = max([pt[0] for pt in points])
max_y = max([pt[1] for pt in points])
max_pt = (max_x, max_y)

print(max_pt)

grid = [['.' for j in range(max_x + 1)] for i in range(max_y + 1)]

for c, r in points:
    grid[r][c] = '#'

def display_grid(grid):
    for row in grid:
        print(''.join(row))

# display_grid(grid)

def fold_grid(grid, fold):
    axis, value = fold
    grid = copy.deepcopy(grid)

    # print(grid)


    if axis == 'y':
        count_after_fold = len(grid) - value
        i = value - count_after_fold + 1
        print(f"Starting i={i}")

        while i < value:
            last_row = grid.pop()
            for c in range(len(grid[i])):
                if last_row[c] == '#':
                    grid[i][c] = last_row[c]
            i += 1
    else:
        count_after_fold = len(grid[0]) - value
        i = value - count_after_fold + 1
        print(f"Starting i={i}")

        while i < value:
            last_col = []
            for r in range(len(grid)):
                last_col.append(grid[r].pop())
            for r in range(len(grid)):
                if last_col[r] == '#':
                    grid[r][i] = last_col[r]    
            i += 1

    return grid

def question_b(grid):
    for fold in folds:
        print(f"before: {fold} rows={len(grid)} cols={len(grid[0])}")
        grid = fold_grid(grid, fold)
        print(f"after: {fold} rows={len(grid)} cols={len(grid[0])}")
    display_grid(grid)

def count_grid(grid):
    count = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '#':
                count += 1
    return count

def question_a(grid):
    grid = fold_grid(grid, folds[0])
    print(count_grid(grid))

# question_a(grid)
question_b(grid) 
