import unittest
from day13 import Day13

class TestDay13(unittest.TestCase):
    def test_parse(self):
        day = Day13()
        parsed = day.parse_input(TestDay13.input1)
        rendered = day.render_raw(parsed)
        print(rendered)
        self.assertEqual(rendered, TestDay13.input1.strip())

    input1 = """
/----\\
|    |
|    |
\----/
"""

if __name__ == "__main__":
    unittest.main()
