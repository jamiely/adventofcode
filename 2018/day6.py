# --- Day 6: Chronal Coordinates ---
# 
# The device on your wrist beeps several times, and once again you feel like
# you're falling.
# 
# "Situation critical," the device announces. "Destination indeterminate.
# Chronal interference detected. Please specify new target coordinates."
# 
# The device then produces a list of coordinates (your puzzle input). Are they
# places it thinks are safe or dangerous? It recommends you check manual page
# 729. The Elves did not give you a manual.
# 
# If they're dangerous, maybe you can minimize the danger by finding the
# coordinate that gives the largest distance from the other points.
# 
# Using only the Manhattan distance, determine the area around each coordinate
# by counting the number of integer X,Y locations that are closest to that
# coordinate (and aren't tied in distance to any other coordinate).
# 
# Your goal is to find the size of the largest area that isn't infinite. For
# example, consider the following list of coordinates:
# 
# 1, 1
# 1, 6
# 8, 3
# 3, 4
# 5, 5
# 8, 9
# 
# If we name these coordinates A through F, we can draw them on a grid, putting
# 0,0 at the top left:
# 
# ..........
# .A........
# ..........
# ........C.
# ...D......
# .....E....
# .B........
# ..........
# ..........
# ........F.
# 
# This view is partial - the actual grid extends infinitely in all directions.
# Using the Manhattan distance, each location's closest coordinate can be
# determined, shown here in lowercase:
# 
# aaaaa.cccc
# aAaaa.cccc
# aaaddecccc
# aadddeccCc
# ..dDdeeccc
# bb.deEeecc
# bBb.eeee..
# bbb.eeefff
# bbb.eeffff
# bbb.ffffFf
# 
# Locations shown as . are equally far from two or more coordinates, and so
# they don't count as being closest to any.
# 
# In this example, the areas of coordinates A, B, C, and F are infinite - while
# not shown here, their areas extend forever outside the visible grid. However,
# the areas of coordinates D and E are finite: D is closest to 9 locations, and
# E is closest to 17 (both including the coordinate's location itself).
# Therefore, in this example, the size of the largest area is 17.
# 
# What is the size of the largest area that isn't infinite?
# with our input: 5626

import re
import string
import math


class Day6a:
    def __init__(self, labels=string.ascii_lowercase):
        self.labels = labels
    def parse(self, line):
        """Parses a string into x,y coordinates"""
        m = re.search(r'(?P<lat>\d+), (?P<long>\d+)', line)
        if not m:
            print(f'Failed to parse line "{line}"')
            return None
        return { 'x': int(m.group('lat')), 'y': int(m.group('long')) }

    def label_coords(self, coords):
        for entry in zip(coords, self.labels):
            coord, label = entry
            coord['label'] = label

    def get_bounding_box(self, coordinates):
        """Finds the bounding box for the coordinates"""
        x1 = 10 * 20
        y1 = x1
        x2 = -1
        y2 = -1
        for coord in coordinates:
            x1 = min(x1, coord['x'])
            y1 = min(y1, coord['y'])
            x2 = max(x2, coord['x'])
            y2 = max(y2, coord['y'])
            
        return {'left': x1, 'right': x2, 'top': y1, 'bottom': y2, 'width': x2-x1 + 1, 'height': y2-y1 + 1}

    def get_normalized_bounding_box(self, box):
        """Returns the bounding box normalized so that it's top left corner is at 0, 0"""
        dx = -box['left']
        dy = -box['top']

        return {'left': box['left'] + dx, 'right': box['right'] + dx,
                'top': box['top'] + dy, 'bottom': box['bottom'] + dy,
                'normalized': True, 'original': box,
                'height': box['height'], 'width': box['width'],
                'dx': dx, 'dy': dy}

    def get_normalized_coordinates(self, box, coordinates):
        return [{
            'x': coord['x'] + box['dx'],
            'y': coord['y'] + box['dy'],
            'label': coord['label']
        } for coord in coordinates]

    def fill_bounding_box(self, plot, coordinates):
        box = plot['bounding_box']
        grid = plot['grid']

        normalized_coords = self.get_normalized_coordinates(box, coordinates)

        for coord in normalized_coords:
            for x in range(box['width']):
                for y in range(box['height']):
                    self.fill_grid_point(grid, coord, x, y)

        return {'bounding_box': box, 'grid': grid}

    def get_coordinates_lying_on_bounds(self, box, coordinates):
        labels = {}
        for coord in coordinates:
            x = coord['x']
            y = coord['y']
            if x == 0 or x == box['width'] - 1:
                labels[coord['label']] = True
            elif y == 0 or y == box['height'] - 1:
                labels[coord['label']] = True
        return labels

    def get_area_counts(self, box_and_grid, coords):
        grid = box_and_grid['grid']
        box = box_and_grid['bounding_box']

        label_counts = {}
        for x in range(box['width']):
            for y in range(box['height']):
                entry = grid[x][y]
                if 'coord' not in entry: continue
                label = entry['coord']['label']
                if label not in label_counts:
                    label_counts[label] = 0
                label_counts[label] += 1

        for label in self.get_coordinates_lying_on_bounds(box, coords).keys():
            label_counts[label] = math.inf

        return label_counts

    def fill_grid_point(self, grid, coord, x, y):
        point = {'x': x, 'y': y}
        if not grid[x][y]:
            grid[x][y] = {
                'coord': coord, 
                'is_canonical': False,
                'point': point,
                'distance': self.manhattan_distance(coord, point)
                }
            return

        existing = grid[x][y]
        # a canonical point is one of the main coordinates. these are not
        # overriden
        if existing['is_canonical']:
            return

        distance = self.manhattan_distance(coord, point)
        if existing['distance'] == distance:
            grid[x][y] = {
                'equivalent': [coord], 
                'is_canonical': False,
                'point': point,
                'distance': distance
                }
            return

        if existing['distance'] > distance:
            grid[x][y] = {
                'coord': coord, 
                'is_canonical': False,
                'point': point,
                'distance': distance
                }
            return

    def manhattan_distance(self, a, b):
        return abs(a['x'] - b['x']) + abs(a['y'] - b['y'])

    def plot_bounding_box(self, box, coordinates):
        fill = [[None for y in range(box['height'])] for x in range(box['width'])]
        # first plot all the coordinates
        for coord in coordinates:
            try:
                x = coord['x'] + box['dx']
                y = coord['y'] + box['dy']
                fill[x][y] = {'coord': coord, 'is_canonical': True}
            except Exception as inst:
                print(f'Failled to fill coord {coord}: {inst}')
        return {'bounding_box': box, 'grid': fill}

    def draw_fill(self, box_and_fill):
        fill = box_and_fill['grid']
        box = box_and_fill['bounding_box']
        
        grid = "\n".join(["".join([self.draw_item(fill[x][y]) for x in range(box['width'])]) for y in range(box['height'])])
        return grid

    def draw_item(self, item):
        if item:
            if 'equivalent' in item:
                return '.'
                
            label = item['coord']['label']
            if item['is_canonical']:
                return label.upper()
            return label
        else:
            return '.'

    def run(self, lines):
        coords = [x for x in [self.parse(line) for line in lines] if x]
        self.label_coords(coords)
        print(f"Coordinates: {coords[:3]}")
        box = self.get_normalized_bounding_box(self.get_bounding_box(coords))
        print(f"Box: {box}")
        box_and_grid = self.plot_bounding_box(box, coords)
        box_and_fill = self.fill_bounding_box(box_and_grid, coords)
        counts = self.get_area_counts(box_and_fill, self.get_normalized_coordinates(box, coords))
        # drawn = self.draw_fill(filled)
        # print(f'Filled:\n{drawn}')

        max_item = None
        for label, value in counts.items():
            if value >= math.inf:
                continue
            elif not max_item:
                max_item = {'label': label, 'value': value}
            elif max_item['value'] < value:
                max_item = {'label': label, 'value': value}

        print(f'The max area is {max_item}')
        return max_item

if __name__ == "__main__":
    with open('day6.input') as f:
        day6a = Day6a(range(1000))
        result = day6a.run(list(f))
        print(f'Result:\n{result}')


# --- Part Two ---
# 
# On the other hand, if the coordinates are safe, maybe the best you can do is
# try to find a region near as many coordinates as possible.
# 
# For example, suppose you want the sum of the Manhattan distance to all of the
# coordinates to be less than 32. For each location, add up the distances to
# all of the given coordinates; if the total of those distances is less than
# 32, that location is within the desired region. Using the same coordinates as
# above, the resulting region looks like this:
# 
# ..........
# .A........
# ..........
# ...###..C.
# ..#D###...
# ..###E#...
# .B.###....
# ..........
# ..........
# ........F.
# 
# In particular, consider the highlighted location 4,3 located at the top
# middle of the region. Its calculation is as follows, where abs() is the
# absolute value function:
# 
#     Distance to coordinate A: abs(4-1) + abs(3-1) =  5
#     Distance to coordinate B: abs(4-1) + abs(3-6) =  6
#     Distance to coordinate C: abs(4-8) + abs(3-3) =  4
#     Distance to coordinate D: abs(4-3) + abs(3-4) =  2
#     Distance to coordinate E: abs(4-5) + abs(3-5) =  3
#     Distance to coordinate F: abs(4-8) + abs(3-9) = 10
#     Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30
# 
# Because the total distance to all coordinates (30) is less than 32, the
# location is within the region.
# 
# This region, which also includes coordinates D and E, has a total size of 16.
# 
# Your actual region will need to be much larger than this example, though,
# instead including all locations with a total distance of less than 10000.
# 
# What is the size of the region containing all locations which have a total
# distance to all given coordinates of less than 10000?
#