import unittest
from day5 import Day5

class TestDay5(unittest.TestCase):
    def test_collapse(self):
        self.assertEqual(Day5("aA").collapse(), "")
        self.assertEqual(Day5("abAB").collapse(), "abAB")
        self.assertEqual(Day5("aabAAB").collapse(), "aabAAB")
        self.assertEqual(Day5("abBA").collapse(), "")
        self.assertEqual(Day5("dabAcCaCBAcCcaDA").collapse(), "dabCBAcaDA")
    def test_collapse2(self):
        self.assertEqual(Day5("AAaAaA").collapse(), "AA")

    def test_strip_polymer(self):
        self.assertEqual(Day5("").strip_polymer("AAAAAAaaabA", "a"), "b")
        self.assertEqual(Day5("").strip_polymer("AAAAAAaaabA", "A"), "b")


if __name__ == '__main__':
    unittest.main()
