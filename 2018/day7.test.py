import unittest
from day7 import Day7

class TestDay7(unittest.TestCase):
    lines = [line for line in """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""".splitlines() if line.strip() != ""
        ]

    def test_example(self):
        self.assertEqual(1,1)

    def test_parse(self):
        day = Day7()
        result = day.parse("Step C must be finished before step A can begin.")
        self.assertDictEqual(result, {'step': 'A', 'dependency': 'C'})

    def test_merge_entries(self):
        day = Day7()
        entries = [day.parse(line) for line in TestDay7.lines]
        merged = day.merge_entries(entries)
        self.assertEqual(merged, {'A': {'C'}, 'F': {'C'}, 'C': set(), 'B': {'A'}, 'D': {'A'}, 'E': {'F', 'D', 'B'}})

    def test_order(self):
        day = Day7()
        entries = [day.parse(line) for line in TestDay7.lines]
        result = day.get_order(entries)

        self.assertEqual(result, 'CABDFE')

# Step C must be finished before step A can begin.
# Step C must be finished before step F can begin.
# Step A must be finished before step B can begin.
# Step A must be finished before step D can begin.
# Step B must be finished before step E can begin.
# Step D must be finished before step E can begin.
# Step F must be finished before step E can begin.

if __name__ == "__main__":
    unittest.main()
