# --- Day 11: Chronal Charge ---

import math
import time

class Day11:

# 
# You watch the Elves and their sleigh fade into the distance as they head
# toward the North Pole.
# 
# Actually, you're the one fading. The falling sensation returns.
# 
# The low fuel warning light is illuminated on your wrist-mounted device.
# Tapping it once causes it to project a hologram of the situation: a 300x300
# grid of fuel cells and their current power levels, some negative. You're not
# sure what negative power means in the context of time travel, but it can't be
# good.
# 
# Each fuel cell has a coordinate ranging from 1 to 300 in both the X
# (horizontal) and Y (vertical) direction. In X,Y notation, the top-left cell
# is 1,1, and the top-right cell is 300,1.
    def __init__(self):
        self.dimensions = 300

    def create_grid(self, dim = 300, init=None):
        return [[init for y in range(dim)] for x in range(dim)]
# 
# The interface lets you select any 3x3 square of fuel cells. To increase your
# chances of getting to your destination, you decide to choose the 3x3 square
# with the largest total power.
# 
# The power level in a given fuel cell can be found through the following
# process:
# 
#     Find the fuel cell's rack ID, which is its X coordinate plus 10.
#     Begin with a power level of the rack ID times the Y coordinate.
#     Increase the power level by the value of the grid serial number (your puzzle input).
#     Set the power level to itself multiplied by the rack ID.
#     Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
#     Subtract 5 from the power level.
    def get_power_level(self, x, y):
        rack_id = x + 10
        level = rack_id * y
        level += self.serial_number
        level *= rack_id
        level = self.get_hundreds(level) # the index of the hundreths place
        level -= 5
        return level

    def get_hundreds(self, number):
        return int(number % 1000 / 100)

    def indicies(self):
        dim = self.dimensions
        return [(x, y) for y in range(dim) for x in range(dim)]

    def get_power_levels(self):
        grid = self.create_grid()
        for _x, _y in self.indicies():
            grid[_x][_y] = self.get_power_level(_x + 1, _y + 1)
        return grid

    def get_largest_3x3(self):
        return self.get_largest_nxn(3)

    def get_largest_nxn_incremental_starting_0(self, n):
        previous_increment = self.create_grid(init = 0)
        result = None
        for n in range(1, n + 1):
            print(f'n={n}')
            result = self.get_largest_nxn_incremental(n, previous_increment)
            if result is None or 'sum_n' not in result:
                print(f'Error in previous increment {result}')
                return None
            previous_increment = result['sum_n']

        return result

    def get_largest_nxn_incremental(self, n, previous_n):
        "Expects a previous_n which is the sum of all n before it."
        print(self.serial_number)
        # print(self.fill_power_levels())
        max_bound = self.dimensions - 1
        levels = self.get_power_levels()
        sum_levels = self.create_grid()

        start = time.time()
        largest_sum = {'coord': None, 'value': None, 'index': None}
        for index in self.indicies():
            _x, _y = index
            if _x == 0 or _y == 0 or _x == max_bound or _y == max_bound:
                sum_levels[_x][_y] = None
                continue

            sum_levels[_x][_y] = self.get_box_sum_at_top_left_incremental(n, levels, index, previous_n)
            if sum_levels[_x][_y] is None: continue

            if largest_sum['value'] is None or largest_sum['value'] < sum_levels[_x][_y]:
                largest_sum['index'] = index
                largest_sum['value'] = sum_levels[_x][_y]
        end = time.time()
        print(f"n={n} calculated box sums in {end - start} seconds.")
        
        if largest_sum['index'] is None:
            return {
                'total_power': None, 
                'top_left_index': None, 
                'coordinates': None
                }
        x, y = largest_sum['index']

        return {
            'total_power': largest_sum['value'], 
            'top_left_index': largest_sum['index'],
            'coordinates': [x + 1, y + 1],
            'sum_n': sum_levels
            # 'box': self.get_box_around(levels, largest_sum['index'])
            }
    def get_largest_nxn(self, n):
        print(self.serial_number)
        # print(self.fill_power_levels())
        max_bound = self.dimensions - 1
        levels = self.get_power_levels()
        sum_levels = self.create_grid()
        for index in self.indicies():
            _x, _y = index
            if _x == 0 or _y == 0 or _x == max_bound or _y == max_bound:
                sum_levels[_x][_y] = None
                continue

            sum_levels[_x][_y] = self.get_box_sum_at_top_left(n, levels, index)

        largest_sum = {'coord': None, 'value': None}
        for index in self.indicies():
            x, y = index
            if sum_levels[x][y] is None: continue
            if largest_sum['value'] is None or largest_sum['value'] < sum_levels[x][y]:
                largest_sum['index'] = index
                largest_sum['value'] = sum_levels[x][y]
        
        x, y = largest_sum['index']

        return {
            'total_power': largest_sum['value'], 
            'top_left_index': largest_sum['index'],
            'coordinates': [x + 1, y + 1]
            # 'box': self.get_box_around(levels, largest_sum['index'])
            }

    def get_delta_indicies(self):
        return [(dx, dy) for dy in range(-1, 2) for dx in range(-1, 2)]

    # def get_box_around(self, grid, coords):
    #     box = self.create_grid(3)
    #     print(box)
    #     x, y = coords
    #     for dy in range(-1, 2):
    #         for dx in range(-1, 2):
    #             box[dx + 1][dy + 1] = grid[x + dx][y + dy]
    #     return box

    def debug(self, msg, condition):
        if not condition: return

        # print(msg)

    def get_box_sum_at_top_left_incremental(self, n, grid, coords, previous_n):
        "We assume that previous_n is a grid containing the sums of (n-1)x(n-1) box at the given coordinate"
        x, y = coords
        if previous_n[x][y] is None: return None

        # self.debug(f'box_sum coord={coords} n={n}', x < 2 and y < 2)
        total = 0
        # when n = 1, coord (0, 0), we look at []
        # when n = 2, coord (0, 0), we look at [0, 1], [1, 1], [1, 0]
        # when n = 3, coord (0, 0), we look at [0, 2], [1, 2], [2, 2], [2, 1], [2, 0]

        # now the diagonal
        dx = n - 1
        dy = n - 1
        _x = x + dx
        _y = y + dy
        if not (len(grid) > _x and len(grid[_x]) > _y): return None
        diag_x = _x
        diag_y = _y
        # self.debug(f'box_sum coord={coords} diagonal=({_x}, {_y})', x < 2 and y < 2)
        total += grid[_x][_y]

        # this is the right edge
        _x = x + n - 1
        for dy in range(n):
            _y = y + dy
            if _x == diag_x and _y == diag_y: continue
            if not (len(grid) > _x and len(grid[_x]) > _y): return None
            # self.debug(f'box_sum coord={coords} top=({_x}, {_y})', x < 2 and y < 2)
            total += grid[_x][_y]

        # this is the bottom edge
        _y = y + n - 1
        for dx in range(n):
            _x = x + dx
            if _x == diag_x and _y == diag_y: continue
            if not (len(grid) > _x and len(grid[_x]) > _y): return None
            # self.debug(f'box_sum coord={coords} bottom=({_x}, {_y})', x < 2 and y < 2)
            total += grid[_x][_y]
        
        total += previous_n[x][y]
        
        return total

    def get_box_sum_at_top_left(self, n, grid, coords):
        x, y = coords
        total = 0
        for dy in range(n):
            for dx in range(n):
                _x = x + dx
                _y = y + dy
                if not (len(grid) > _x and len(grid[_x]) > _y): return None

                total += grid[x + dx][y + dy]
                
        return total

# 
# For example, to find the power level of the fuel cell at 3,5 in a grid with
# serial number 8:
# 
#     The rack ID is 3 + 10 = 13.
#     The power level starts at 13 * 5 = 65.
#     Adding the serial number produces 65 + 8 = 73.
#     Multiplying by the rack ID produces 73 * 13 = 949.
#     The hundreds digit of 949 is 9.
#     Subtracting 5 produces 9 - 5 = 4.
# 
# So, the power level of this fuel cell is 4.
# 
# Here are some more example power levels:
# 
#     Fuel cell at  122,79, grid serial number 57: power level -5.
#     Fuel cell at 217,196, grid serial number 39: power level  0.
#     Fuel cell at 101,153, grid serial number 71: power level  4.
# 
# Your goal is to find the 3x3 square which has the largest total power. The
# square must be entirely within the 300x300 grid. Identify this square using
# the X,Y coordinate of its top-left fuel cell. For example:
# 
# For grid serial number 18, the largest total 3x3 square has a top-left corner
# of 33,45 (with a total power of 29); these fuel cells appear in the middle of
# this 5x5 region:
# 
# -2  -4   4   4   4
# -4   4   4   4  -5
#  4   3   3   4  -4
#  1   1   2   4  -3
# -1   0   2  -5  -2
# 
# For grid serial number 42, the largest 3x3 square's top-left is 21,61 (with a
# total power of 30); they are in the middle of this region:
# 
# -3   4   2   2   2
# -4   4   3   3   4
# -5   3   3   4  -4
#  4   3   3   4  -3
#  3   3   3  -5  -1
# 
# What is the X,Y coordinate of the top-left fuel cell of the 3x3 square with
# the largest total power?
# 
# Your puzzle input is 9995.
    def runA(self, input):
        self.serial_number = self.parse(input)
        result = self.get_largest_3x3()
        print(result)

# 
# Your puzzle answer was 33,45.
#

# --- Part Two ---
# 
# You discover a dial on the side of the device; it seems to let you select a
# square of any size, not just 3x3. Sizes from 1x1 to 300x300 are supported.
# 
# Realizing this, you now must find the square of any size with the largest
# total power. Identify this square by including its size as a third parameter
# after the top-left coordinate: a 9x9 square with a top-left corner of 3,5 is
# identified as 3,5,9.

# For example:
# 
#     For grid serial number 18, the largest total square (with a total power of
#     113) is 16x16 and has a top-left corner of 90,269, so its identifier is
#     90,269,16.
#     
#     For grid serial number 42, the largest total square (with a total power of
#     119) is 12x12 and has a top-left corner of 232,251, so its identifier is
#     232,251,12.
# 
# What is the X,Y,size identifier of the square with the largest total power?
# 233,116,15

    def max_power_b(self, size_limit):
        max_result = {'total_power': - math.inf}
        previous_increment = self.create_grid(init = 0)
        for n in range(1, size_limit + 1):
            start = time.time()
            print(f'Computing n={n}')
            result = self.get_largest_nxn_incremental(n, previous_increment)
            previous_increment = result['sum_n']
            if result['total_power'] > max_result['total_power']:
                max_result = result
                max_result['n'] = n
            end = time.time()
            print(f'Max total power: {max_result["total_power"]} origin: {max_result["top_left_index"]} n={max_result["n"]} in {end - start} seconds.')
            x, y = max_result['top_left_index']
            print(f"The answer so far is \"{x+1},{y+1},{max_result['n']}\"")

        print(f'Max total power: {max_result["total_power"]} origin: {max_result["top_left_index"]}')
        x, y = max_result['top_left_index']
        print(f"The answer is \"{x+1},{y+1},{max_result['n']}\"")

        return max_result

    def runB(self, input):
        self.serial_number = self.parse(input)
        return self.max_power_b(301)

    def parse(self, input):
        return int(input.strip())

if __name__ == "__main__":
    import common
    day = Day11()
    common.main(day, 'day11.input')
