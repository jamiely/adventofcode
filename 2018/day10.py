# --- Day 10: The Stars Align ---
# 
# It's no use; your navigation system simply isn't capable of providing walking
# directions in the arctic circle, and certainly not in 1018.
# 
# The Elves suggest an alternative. In times like these, North Pole rescue
# operations will arrange points of light in the sky to guide missing Elves
# back to base. Unfortunately, the message is easy to miss: the points move
# slowly enough that it takes hours to align them, but have so much momentum
# that they only stay aligned for a second. If you blink at the wrong time, it
# might be hours before another message appears.
# 
# You can see these points of light floating in the distance, and record their
# position in the sky and their velocity, the relative change in position per
# second (your puzzle input). The coordinates are all given from your
# perspective; given enough time, those positions and velocities will move the
# points into a cohesive message!
# 
# Rather than wait, you decide to fast-forward the process and calculate what
# the points will eventually spell.
# 
# For example, suppose you note the following points:
# 
# position=< 9,  1> velocity=< 0,  2>
# position=< 7,  0> velocity=<-1,  0>
# position=< 3, -2> velocity=<-1,  1>
# position=< 6, 10> velocity=<-2, -1>
# position=< 2, -4> velocity=< 2,  2>
# position=<-6, 10> velocity=< 2, -2>
# position=< 1,  8> velocity=< 1, -1>
# position=< 1,  7> velocity=< 1,  0>
# position=<-3, 11> velocity=< 1, -2>
# position=< 7,  6> velocity=<-1, -1>
# position=<-2,  3> velocity=< 1,  0>
# position=<-4,  3> velocity=< 2,  0>
# position=<10, -3> velocity=<-1,  1>
# position=< 5, 11> velocity=< 1, -2>
# position=< 4,  7> velocity=< 0, -1>
# position=< 8, -2> velocity=< 0,  1>
# position=<15,  0> velocity=<-2,  0>
# position=< 1,  6> velocity=< 1,  0>
# position=< 8,  9> velocity=< 0, -1>
# position=< 3,  3> velocity=<-1,  1>
# position=< 0,  5> velocity=< 0, -1>
# position=<-2,  2> velocity=< 2,  0>
# position=< 5, -2> velocity=< 1,  2>
# position=< 1,  4> velocity=< 2,  1>
# position=<-2,  7> velocity=< 2, -2>
# position=< 3,  6> velocity=<-1, -1>
# position=< 5,  0> velocity=< 1,  0>
# position=<-6,  0> velocity=< 2,  0>
# position=< 5,  9> velocity=< 1, -2>
# position=<14,  7> velocity=<-2,  0>
# position=<-3,  6> velocity=< 2, -1>
# 
# Each line represents one point. Positions are given as <X, Y> pairs: X
# represents how far left (negative) or right (positive) the point appears,
# while Y represents how far up (negative) or down (positive) the point
# appears.
# 
# At 0 seconds, each point has the position given. Each second, each point's
# velocity is added to its position. So, a point with velocity <1, -2> is
# moving to the right, but is moving upward twice as quickly. If this point's
# initial position were <3, 9>, after 3 seconds, its position would become <6, 3>.
# 
# Over time, the points listed above would move like this:
# 
# Initially:
# ........#.............
# ................#.....
# .........#.#..#.......
# ......................
# #..........#.#.......#
# ...............#......
# ....#.................
# ..#.#....#............
# .......#..............
# ......#...............
# ...#...#.#...#........
# ....#..#..#.........#.
# .......#..............
# ...........#..#.......
# #...........#.........
# ...#.......#..........
# 
# After 1 second:
# ......................
# ......................
# ..........#....#......
# ........#.....#.......
# ..#.........#......#..
# ......................
# ......#...............
# ....##.........#......
# ......#.#.............
# .....##.##..#.........
# ........#.#...........
# ........#...#.....#...
# ..#...........#.......
# ....#.....#.#.........
# ......................
# ......................
# 
# After 2 seconds:
# ......................
# ......................
# ......................
# ..............#.......
# ....#..#...####..#....
# ......................
# ........#....#........
# ......#.#.............
# .......#...#..........
# .......#..#..#.#......
# ....#....#.#..........
# .....#...#...##.#.....
# ........#.............
# ......................
# ......................
# ......................
# 
# After 3 seconds:
# ......................
# ......................
# ......................
# ......................
# ......#...#..###......
# ......#...#...#.......
# ......#...#...#.......
# ......#####...#.......
# ......#...#...#.......
# ......#...#...#.......
# ......#...#...#.......
# ......#...#..###......
# ......................
# ......................
# ......................
# ......................
# 
# After 4 seconds:
# ......................
# ......................
# ......................
# ............#.........
# ........##...#.#......
# ......#.....#..#......
# .....#..##.##.#.......
# .......##.#....#......
# ...........#....#.....
# ..............#.......
# ....#......#...#......
# .....#.....##.........
# ...............#......
# ...............#......
# ......................
# ......................
# 
# After 3 seconds, the message appeared briefly: HI. Of course, your message
# will be much longer and will take many more seconds to appear.
# 
# What message will eventually appear in the sky?
# 
# HJBJXRAZ
#
import common
import re

class Day10:
    def __init__(self):
        self.counter = 0

    def parse(self, line):
        m = re.search("position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>", line)
        if not m:
            print(f'No match for line {line}')
            return None

        captures = [int(m.group(i)) for i in range(1, 5)]

        result = {'position': [captures[0], captures[1]], 'velocity': [captures[2], captures[3]]}
        return result

    def get_input(self, input):
        entries = map(self.parse, input.strip().splitlines())
        return list(filter(lambda a: a is not None, entries))

    def draw_grid(self, entries):
        box = self.get_bounding_box(entries)
        width = box['width']
        height = box['height']

        grid = [['.' for y in range(height + 1)] for x in range(width + 1)]

        for entry in entries:
            x, y = entry['position']
            x += box['dx']
            y += box['dy']
            grid[x][y] = '#'

        return "\n".join(["".join([grid[x][y] for x in range(width + 1)]) for y in range(height + 1)])

    def draw_grid_fast(self, entries, scale = 1):
        from PIL import Image

        import sys
        box = self.get_bounding_box(entries)
        print(f"Box: {box} scale={scale}")
        width = int(box['width'] / scale) + 1
        height = int(box['height'] / scale) + 1
        print(f'creating image {width} x {height}')
        img = Image.new('RGB', (width, height), "black")
        print(f'created image {self.counter}')
        pixels = img.load()

        grid = {}
        for entry in entries:
            x, y = entry['position']
            x += box['dx']
            y += box['dy']
            x = int(x / scale)
            y = int(y / scale)
            pixels[x,y] = (255, 255, 255)

        img.save(f'day10/image.{str(self.counter).zfill(5)}.png')
        self.counter += 1

    def update_position(self, entry):
        x, y = entry['position']
        dx, dy = entry['velocity']
        return {'position': [x + dx, y + dy], 'velocity': [dx, dy]}

    def update_entries(self, entries):
        return list(map(self.update_position, entries))

    def get_indices(self, box):
        return [(x, y) for x in range(box['width'] + 1) for y in range(box['height'] + 1)]
    
    def get_bounding_box(self, entries):
        xs = list(map(lambda a: a['position'][0], entries))
        ys = list(map(lambda a: a['position'][1], entries))

        x0 = min(xs)
        y0 = min(ys)
        x1 = max(xs)
        y1 = max(ys)

        return {'width': abs(x1 - x0), 'height': abs(y1 - y0), 'dx': -x0, 'dy': -y0}

    def draw_tick_interactive(self, input, drawer):
        import sys

        entries = self.get_input(input)
        x = ''
        updates_per_loop = 10
        max_area = 100 * 100
        import math
        last_area = math.inf
        seconds = 0
        while x != 'q':
            box = self.get_bounding_box(entries)
            area = box['height'] * box['width']
            if last_area < area:
                print('Picture is getting biggger, stop.')
                break

            if area < max_area:
                print('Grid:')
                print(drawer(entries))
                entries = self.update_entries(entries)
                seconds += 1
            else:
                if seconds % 1000 == 0:
                    print(f'box is too big, with area {area}')
                for i in range(updates_per_loop):
                    entries = self.update_entries(entries)
                    seconds += 1
                    if area < max_area:
                        print('box getting small')
                        break

            last_area = area

        return seconds - 1


    def run_a(self, input):
        print("Generating image")
        self.draw_tick_interactive(input, drawer=lambda entries: self.draw_grid_fast(entries, scale = 1))
        print("Writing to console")
        self.draw_tick_interactive(input, drawer=lambda entries: self.draw_grid(entries))

# --- Part Two ---
# 
# Good thing you didn't have to wait, because that would have taken a long time
# - much longer than the 3 seconds in the example above.
# 
# Impressed by your sub-hour communication capabilities, the Elves are curious:
# exactly how many seconds would they have needed to wait for that message to
# appear?
# 
# 10641

    def run_b(self, input):
        seconds = self.draw_tick_interactive(input, drawer=lambda entries: self.draw_grid(entries, scale = 1))
        print(f"Completed in {seconds} seconds.")

if __name__ == "__main__":
    day = Day10()
    common.main(day, 'day10.input')
