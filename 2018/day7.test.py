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

    def test_get_next_steps(self):
        day = Day7()
        entries = [day.parse(line) for line in TestDay7.lines]
        merged = day.merge_entries(entries)
        next_steps = day.get_next_steps(merged)
        self.assertEqual(next_steps, ['C'])
        next_steps = day.get_next_steps(day.remove_from_work(merged, 'C'))
        self.assertEqual(next_steps, ['A', 'F'])

    def test_remove_from_work(self):
        day = Day7()
        entries = [day.parse(line) for line in TestDay7.lines]
        merged = day.merge_entries(entries)
        updated = day.remove_from_work(merged, 'C')
        self.assertDictEqual(updated, {'A': set(), 'F': set(), 'B': {'A'}, 'D': {'A'}, 'E': {'F', 'D', 'B'}})

    def test_get_task_completion(self):
        day = Day7(time_for_each_task=0)
        result = day.get_task_completion(0, 'A')
        self.assertEqual(result, 1)

        day2 = Day7(time_for_each_task=99)
        result = day2.get_task_completion(0, 'A')
        self.assertEqual(result, 99 + 1)

    def test_run_work(self):
        import copy

        day = Day7(time_for_each_task=0, workers=2)
        entries = [day.parse(line) for line in TestDay7.lines]
        merged = day.merge_entries(entries)
        results = []
        clock = day.run_work(merged, lambda report: results.append(copy.deepcopy(report)), tick_max=20)

        self.assertEqual(clock, 15)

        report = []
        for entry in results:
            parts = [str(entry['clock'])]
            for worker in entry['workers']:
                if worker['is_working']:
                    parts.append(worker['task'])
                else:
                    parts.append('.')
            parts.append("".join(entry['done']))
            report.append(" | ".join(parts))
        actual = "\n".join(report)
        self.assertEqual(actual, """
0 | C | . | 
1 | C | . | 
2 | C | . | 
3 | A | F | C
4 | B | F | CA
5 | B | F | CA
6 | D | F | CAB
7 | D | F | CAB
8 | D | F | CAB
9 | D | . | CABF
10 | E | . | CABFD
11 | E | . | CABFD
12 | E | . | CABFD
13 | E | . | CABFD
14 | E | . | CABFD
15 | . | . | CABFDE        
        """.strip())

    def test_run_work(self):
        import copy

        day = Day7(time_for_each_task=60, workers=5)
        entries = [day.parse(line) for line in TestDay7.lines]
        merged = day.merge_entries(entries)
        results = []
        clock = day.run_work(merged, lambda report: results.append(copy.deepcopy(report)), tick_max=1000)

        report = []
        for entry in results:
            parts = [str(entry['clock'])]
            for worker in entry['workers']:
                if worker['is_working']:
                    parts.append(worker['task'])
                else:
                    parts.append('.')
            parts.append("".join(entry['done']))
            report.append(" | ".join(parts))
        actual = "\n".join(report)
        print(f"{actual}\nclock: {clock}")


# Step C must be finished before step A can begin.
# Step C must be finished before step F can begin.
# Step A must be finished before step B can begin.
# Step A must be finished before step D can begin.
# Step B must be finished before step E can begin.
# Step D must be finished before step E can begin.
# Step F must be finished before step E can begin.

if __name__ == "__main__":
    unittest.main()
