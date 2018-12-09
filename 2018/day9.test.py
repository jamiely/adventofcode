import unittest
from day9 import Day9

class TestDay9(unittest.TestCase):
    def test_a(self):
        print(1)
    
    def test_play(self):
        import copy
        day = Day9()
        results = []
        day.play(players=9, turns=25, reporter=lambda a: results.append(day.entry_formatter(a)))
        report = "\n".join(results)
        print(f"Results: \n{report}")
        self.assertEqual(results, """
[2] 0 (2) 1
[3] 0 2 1 (3)
[4] 0 (4) 2 1 3
[5] 0 4 2 (5) 1 3
[6] 0 4 2 5 1 (6) 3
[7] 0 4 2 5 1 6 3 (7)
[8] 0 (8) 4 2 5 1 6 3 7
[9] 0 8 4 (9) 2 5 1 6 3 7
[1] 0 8 4 9 2 (10) 5 1 6 3 7
[2] 0 8 4 9 2 10 5 (11) 1 6 3 7
[3] 0 8 4 9 2 10 5 11 1 (12) 6 3 7
[4] 0 8 4 9 2 10 5 11 1 12 6 (13) 3 7
[5] 0 8 4 9 2 10 5 11 1 12 6 13 3 (14) 7
[6] 0 8 4 9 2 10 5 11 1 12 6 13 3 14 7 (15)
[7] 0 (16) 8 4 9 2 10 5 11 1 12 6 13 3 14 7 15
[8] 0 16 8 (17) 4 9 2 10 5 11 1 12 6 13 3 14 7 15
[9] 0 16 8 17 4 (18) 9 2 10 5 11 1 12 6 13 3 14 7 15
[1] 0 16 8 17 4 18 9 (19) 2 10 5 11 1 12 6 13 3 14 7 15
[2] 0 16 8 17 4 18 9 19 2 (20) 10 5 11 1 12 6 13 3 14 7 15
[3] 0 16 8 17 4 18 9 19 2 20 10 (21) 5 11 1 12 6 13 3 14 7 15
[4] 0 16 8 17 4 18 9 19 2 20 10 21 5 (22) 11 1 12 6 13 3 14 7 15
[5] 0 16 8 17 4 18 (19) 2 20 10 21 5 22 11 1 12 6 13 3 14 7 15
[6] 0 16 8 17 4 18 19 2 (24) 20 10 21 5 22 11 1 12 6 13 3 14 7 15
[7] 0 16 8 17 4 18 19 2 24 20 (25) 10 21 5 22 11 1 12 6 13 3 14 7 15
""".strip().splitlines())


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
