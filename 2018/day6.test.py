import unittest
from day6 import Day6a
from day6 import Day6b

class TestDay6a(unittest.TestCase):
    test_coords = [
        { 'x': 1, 'y': 1 },
        { 'x': 1, 'y': 6 },
        { 'x': 8, 'y': 3 },
        { 'x': 3, 'y': 4 },
        { 'x': 5, 'y': 5 },
        { 'x': 8, 'y': 9 }]

    test_box  = { 'left': 1, 'right': 8, 'top': 1, 'bottom': 9, 'width': 8, 'height': 9}

    def test_parse(self):
        self.assertEqual(Day6a().parse("1, 1"), {'x': 1, 'y': 1})
        self.assertEqual(Day6a().parse("11, 11"), {'x': 11, 'y': 11})

    def test_bounds(self):
        self.assertDictEqual(Day6a().get_bounding_box(TestDay6a.test_coords),
            TestDay6a.test_box)

    def test_normalized_box(self):
        self.assertDictEqual(Day6a().get_normalized_bounding_box(TestDay6a.test_box),
            { 'left': 0, 'right': 7, 'top': 0, 'bottom': 8,
            'normalized': True, 'original': TestDay6a.test_box, 'dx': -1, 'dy': -1,
            'width': 8, 'height': 9})

    def test_plot(self):
        day6 = Day6a()
        coords = TestDay6a.test_coords
        day6.label_coords(coords)
        box = day6.get_normalized_bounding_box(day6.get_bounding_box(coords))
        grid = Day6a().plot_bounding_box(box, coords)
        drawn = day6.draw_fill(grid)
        self.assertEqual(drawn, "\n".join([line for line in """
A.......
........
.......C
..D.....
....E...
B.......
........
........
.......F
""".splitlines() if line.strip() != ""]))

    def test_fill(self):
        day6 = Day6a()
        coords = TestDay6a.test_coords
        day6.label_coords(coords)
        box = day6.get_normalized_bounding_box(day6.get_bounding_box(coords))
        grid = Day6a().plot_bounding_box(box, coords)
        grid = Day6a().fill_bounding_box(grid, coords)
        print(grid['grid'][4][0])
        print(grid['grid'][5][0])
        drawn = day6.draw_fill(grid)
        self.assertEqual(drawn, "\n".join([line for line in """
Aaaa.ccc
aaddeccc
adddeccC
.dDdeecc
b.deEeec
Bb.eeee.
bb.eeeff
bb.eefff
bb.ffffF
""".splitlines() if line.strip() != ""]))

    def test_get_coordinates_on_bounds(self):
        day6 = Day6a()
        coords = TestDay6a.test_coords
        day6.label_coords(coords)
        box = day6.get_normalized_bounding_box(day6.get_bounding_box(coords))
        norm_coords = day6.get_normalized_coordinates(box, coords)
        on_bounds = day6.get_coordinates_lying_on_bounds(box, norm_coords)
        print(f'On bounds: {on_bounds}')



    def test_area_count(self):
        day6 = Day6a()
        coords = TestDay6a.test_coords
        day6.label_coords(coords)
        box = day6.get_normalized_bounding_box(day6.get_bounding_box(coords))
        grid = day6.plot_bounding_box(box, coords)
        grid = day6.fill_bounding_box(grid, coords)
        counts = day6.get_area_counts(grid, day6.get_normalized_coordinates(box, coords))
        self.assertEqual(counts['d'], 9)
        self.assertEqual(counts['e'], 17)

    def test_run(self):
        content = """
    1, 1
    1, 6
    8, 3
    3, 4
    5, 5
    8, 9
        """
        day6 = Day6a()
        result = day6.run([line for line in content.splitlines() if line.strip() != ""])
        self.assertDictEqual(result, {'label': 'e', 'value': 17})

class TestDay6b(unittest.TestCase):
    test_coords = [
        { 'x': 1, 'y': 1 },
        { 'x': 1, 'y': 6 },
        { 'x': 8, 'y': 3 },
        { 'x': 3, 'y': 4 },
        { 'x': 5, 'y': 5 },
        { 'x': 8, 'y': 9 }]

    test_box  = { 'left': 1, 'right': 8, 'top': 1, 'bottom': 9, 'width': 8, 'height': 9}

    def test_parse(self):
        self.assertEqual(Day6b().parse("1, 1"), {'x': 1, 'y': 1})
        self.assertEqual(Day6b().parse("11, 11"), {'x': 11, 'y': 11})

    def test_bounds(self):
        self.assertDictEqual(Day6b().get_bounding_box(TestDay6b.test_coords),
            TestDay6b.test_box)

    def test_normalized_box(self):
        self.assertDictEqual(Day6b().get_normalized_bounding_box(TestDay6b.test_box),
            { 'left': 0, 'right': 7, 'top': 0, 'bottom': 8,
            'normalized': True, 'original': TestDay6b.test_box, 'dx': -1, 'dy': -1,
            'width': 8, 'height': 9})

    def test_calculate(self):
        day6 = Day6b(max_distance=32)
        coords = TestDay6b.test_coords
        day6.label_coords(coords)
        box = day6.get_normalized_bounding_box(day6.get_bounding_box(coords))
        box_and_grid = day6.plot_bounding_box(box, coords)
        norm_coords = day6.get_normalized_coordinates(box, coords)
        calculation = day6.calculate(box_and_grid, norm_coords)
        result = day6.draw_calc(box, norm_coords, calculation)
        print(f'Grid: {result}')
        self.assertEqual(result, "\n".join([line for line in """
A.......
........
..###..C
.#D###..
.###E#..
B.###...
........
........
.......F
""".splitlines() if line.strip() != ""]))
        area = day6.get_area_of_calc(box_and_grid, calculation)
        self.assertEqual(area, 16)


    # def test_run(self):
    #     content = """
    # 1, 1
    # 1, 6
    # 8, 3
    # 3, 4
    # 5, 5
    # 8, 9
    #     """
    #     day6 = Day6b(32)
    #     result = day6.run([line for line in content.splitlines() if line.strip() != ""])
    #     self.assertEqual(result, 1)

if __name__ == "__main__":
    unittest.main()
