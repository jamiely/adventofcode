import unittest
from day13 import Day13

class TestDay13(unittest.TestCase):
    def test_parse(self):
        day = Day13()
        parsed = day.parse_input(TestDay13.input1)
        rendered = day.render_raw(parsed)
        print(rendered)
        self.assertEqual(rendered, TestDay13.input1.strip())

    def test_load_tracks_1(self):
        day = Day13()
        parsed = day.parse_input(TestDay13.input1)
        track_info = day.load_tracks(parsed)
        self.assertEqual(len(track_info['tracks']), 1)
        print(track_info['tracks'][0])
        self.assertEqual(len(track_info['tracks'][0]['indicies']), 16)
        
    def test_load_tracks_2(self):
        day = Day13()
        parsed = day.parse_input(TestDay13.input2)
        print(day.render_raw(parsed))
        track_info = day.load_tracks(parsed)
        self.assertEqual(len(track_info['tracks']), 2)
        self.assertEqual(len(track_info['tracks'][0]['indicies']), 20)
        self.assertEqual(len(track_info['tracks'][1]['indicies']), 20)

    input1 = """
/----\\
|    |
|    |
\----/
"""

    input2 = """
/-----\\
|     |
|  /--+--\\
|  |  |  |
\--+--/  |
   |     |
   \-----/
"""

if __name__ == "__main__":
    unittest.main()
