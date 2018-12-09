# --- Day 8: Memory Maneuver ---
# 
# The sleigh is much easier to pull than you'd expect for something its weight.
# Unfortunately, neither you nor the Elves know which way the North Pole is
# from here.
# 
# You check your wrist device for anything that might help. It seems to have
# some kind of navigation system! Activating the navigation system produces
# more bad news: "Failed to start navigation system. Could not read software
# license file."
# 
# The navigation system's license file consists of a list of numbers (your
# puzzle input). The numbers define a data structure which, when processed,
# produces some kind of tree that can be used to calculate the license number.
# 
# The tree is made up of nodes; a single, outermost node forms the tree's root,
# and it contains all other nodes in the tree (or contains nodes that contain
# nodes, and so on).
# 
# Specifically, a node consists of:
# 
#     A header, which is always exactly two numbers:
#         The quantity of child nodes.
#         The quantity of metadata entries.
#     Zero or more child nodes (as specified in the header).
#     One or more metadata entries (as specified in the header).
# 
# Each child node is itself a node that has its own header, child nodes, and
# metadata. For example:
# 
# 2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
# A----------------------------------
#     B----------- C-----------
#                      D-----
# 
# In this example, each node of the tree is also marked with an underline
# starting with a letter for easier identification. In it, there are four
# nodes:
# 
#     A, which has 2 child nodes (B, C) and 3 metadata entries (1, 1, 2).
#     B, which has 0 child nodes and 3 metadata entries (10, 11, 12).
#     C, which has 1 child node (D) and 1 metadata entry (2).
#     D, which has 0 child nodes and 1 metadata entry (99).
# 
# The first check done on the license file is to simply add up all of the
# metadata entries. In this example, that sum is 1+1+2+10+11+12+2+99=138.
# 
# What is the sum of all metadata entries?
# 

import string

class Day8:
    def __init__(self, labels = string.ascii_uppercase):
        self.labels = list(labels)

    def split(self, input):
        return [int(c) for c in input.split(' ')]

    def parse(self, input):
        numbers = self.split(input)
        # we create a dummy root and remove it later
        root = {
            'label': 'sentinel',
            'children_count': 1,
            'metadata': None,
            'children': []
        }
        # print(f"Root {root}")
        self.recurse(root, numbers)
        # remove the dummey root
        return root['children'][0]

    def add_all_metadata(self, tree):
        total = 0
        for child in tree['children']:
            total += self.add_all_metadata(child)
        total += sum(tree['metadata'])
        return total

    def make_node(self, numbers):
        return {
            'label': self.labels.pop(0),
            'children_count': numbers.pop(0),
            'metadata_count': numbers.pop(0),
            'metadata': [],
            'children': []
        }

    def recurse(self, current, numbers):
        for i in range(current['children_count']):
            child = self.make_node(numbers)
            # print(f"Made child {child}")
            self.recurse(child, numbers)
            for i in range(child['metadata_count']):
                child['metadata'].append(numbers.pop(0))
            current['children'].append(child)

    def runA(self, input):
        tree = self.parse(input)
        total = self.add_all_metadata(tree)
        print(f'The sum of all metadata is {total}')
        return total

if __name__ == "__main__":
    import sys, getopt
    opts, _ = getopt.getopt(sys.argv[1:], "ab", [])
    day = Day8(labels=list(range(10000)))

    should_run_b = False
    for o, a in opts:
        if o == "-a":
            pass
        elif o == "-b":
            should_run_b = True
        else:
            assert False, "unhandled option"
    input = ""
    with open('day8.input') as f:
        input = f.read()

    if should_run_b:
        day.runB(input)
    else:
        day.runA(input)
