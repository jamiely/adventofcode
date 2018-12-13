from day11 import Day11
import unittest

class TestDay11(unittest.TestCase):
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
    def test_create_grid(self):
        day = Day11()
        grid = day.create_grid()
        self.assertEqual(len(grid), 300)
        self.assertEqual(len(grid[0]), 300)
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
    def test_get_power_level(self):
        day = Day11()
        day.serial_number = 8
        result = day.get_power_level(3, 5)
        self.assertEqual(result, 4)

    def test_get_hundreds(self):
        day = Day11()
        result = day.get_hundreds(12345)
        self.assertEqual(result, 3)
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

    def test_power_levels(self):
        tests = [
            [[122, 79], 57, -5],
            [[217, 196], 39, 0],
            [[101, 153], 71, 4]
        ]
        day = Day11()
        for test in tests:
            coords, serial, level = test
            x, y = coords
            day.serial_number = serial
            result = day.get_power_level(x, y)
            self.assertEqual(result, level)

    def test_largest_3x3(self):
        day = Day11()
        day.serial_number = 18
        result = day.get_largest_3x3()
        self.assertEqual(result['total_power'], 29)
        print(result)

    def test_largest_3x3_b(self):
        day = Day11()
        day.serial_number = 42
        result = day.get_largest_3x3()
        self.assertEqual(result['total_power'], 30)
        print(result)

    def test_largest_nxn_3(self):
        day = Day11()
        day.serial_number = 42
        result = day.get_largest_nxn(3)
        self.assertEqual(result['total_power'], 30)
        print(result)

    def test_largest_nxn_2(self):
        day = Day11()
        day.serial_number = 42
        result = day.get_largest_nxn(2)
        self.assertEqual(result['total_power'], 16)
        print(result)

    def test_largest_nxn_1(self):
        day = Day11()
        day.serial_number = 42
        result = day.get_largest_nxn(1)
        self.assertEqual(result['total_power'], 4)
        print(result)

    def test_largest_nxn_incremental1(self):
        day = Day11()
        day.serial_number = 42
        result = day.get_largest_nxn_incremental_starting_0(1)
        # print(result)
        self.assertEqual(result['total_power'], 4)

    def test_largest_nxn_incremental2(self):
        day = Day11()
        day.serial_number = 42
        result = day.get_largest_nxn_incremental_starting_0(2)
        # print(result)
        self.assertEqual(result['total_power'], 16)

    def test_largest_nxn_incremental3(self):
        day = Day11()
        day.serial_number = 42
        result = day.get_largest_nxn_incremental_starting_0(3)
        # print(result)
        self.assertEqual(result['total_power'], 30)

    def test_max_power_b(self):
        day = Day11()
        day.serial_number = 42
        result = day.max_power_b(13)

        self.assertEqual(result['top_left_index'], (231,250))
        self.assertEqual(result['n'], 12)
        self.assertEqual(result['total_power'], 119)
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
#
    def test_parse(self):
        day = Day11()
        result = day.parse("""  111
        """)
        self.assertEqual(result, 111)

if __name__ == "__main__":
    unittest.main()
