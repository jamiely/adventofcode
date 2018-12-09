import unittest
from day9 import Day9

class TestDay9(unittest.TestCase):
    def test_a(self):
        print(1)
    
    def test_play(self):
        import copy
        day = Day9()
        results = []
        day.play(turns=8, reporter=lambda a: results.append(day.entry_formatter(a)))
        report = "\n".join(results)
        print(f"Results: {results}")
        self.assertEqual(report, """
[2]  0 (2) 1
[3]  0 2 1 (3)
[4]  0 (4) 2 1 3
[5]  0 4 2 (5) 1 3
[6]  0 4 2 5 1 (6) 3
[7]  0 4 2 5 1 6 3 (7)
[8]  0 (8) 4 2 5 1 6 3 7
""".strip())


# notes
# last index 0, next insert index is 1
#      0  1  2  3  4  5  6  7  8
# [-] (0)                           # insert 0, last ?, proj ?
# [1]  0 (1)                        # insert 1, last 0, proj 2
# [2]  0 (2) 1                      # insert 1, last 1, proj 3
# [3]  0  2  1 (3)                  # insert 3, last 1, proj 3
# [4]  0 (4) 2  1  3                # insert 1, last 3, proj 5
# [5]  0  4  2 (5) 1  3             # insert 3, last 1, proj 3
# [6]  0  4  2  5  1 (6) 3          # insert 5, last 3, proj 5
# [7]  0  4  2  5  1  6  3 (7)      # insert 7, last 5, proj 7
# [8]  0 (8) 4  2  5  1  6  3  7    # insert 1, last 7, proj 9

# insert 0
# insert 1
# in



if __name__ == "__main__":
    unittest.main()
