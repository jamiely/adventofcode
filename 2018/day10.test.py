import unittest
from day10 import Day10

class TestDay10(unittest.TestCase):
    def test_parse(self):
        day = Day10()
        result = day.parse("position=< 9,  1> velocity=< 0,  2>")
        self.assertDictEqual(result, {
            'position': [9, 1],
            'velocity': [0, 2]
        })

    def get_bounding_Box(self):
        day = Day10()
        result = day.get_bounding_box([
            {'position': [-1, -1]},
            {'position': [1, 1]}
        ])
        self.assertDictEqual(result, {
            'width': 2,
            'height': 2,
            'dx': 1,
            'dy': 1
        })

    def test_draw_grid_simple(self):
        day = Day10()
        result = day.draw_grid([
            {'position': [-1, -1]},
            {'position': [1, 1]},
            {'position': [0, 1]}
        ])
        self.assertEqual(result, """
#..
...
.##
""".strip())

    def test_bounds_2(self):
        day = Day10()
        input = self.get_input(day)
        bounds = day.get_bounding_box(input)
        self.assertDictEqual(bounds, {'dx': 6, 'dy': 4, 'height': 15, 'width': 21})

    def test_draw_grid(self):
        day = Day10()
        input = self.get_input(day)
        result = day.draw_grid(input)
        self.assertEqual(result, """
........#.............
................#.....
.........#.#..#.......
......................
#..........#.#.......#
...............#......
....#.................
..#.#....#............
.......#..............
......#...............
...#...#.#...#........
....#..#..#.........#.
.......#..............
...........#..#.......
#...........#.........
...#.......#..........
""".strip())

    def test_draw_grid_tick1(self):
        day = Day10()
        input = self.get_input(day)
        result = day.draw_grid(day.update_entries(input))
        self.assertEqual(result.splitlines(), """
........#....#....
......#.....#.....
#.........#......#
..................
....#.............
..##.........#....
....#.#...........
...##.##..#.......
......#.#.........
......#...#.....#.
#...........#.....
..#.....#.#.......
""".strip().splitlines())

    def get_input(self, day):
        return day.get_input("""
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
""".strip())

        

if __name__ == "__main__":
    unittest.main()
