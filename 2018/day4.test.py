import unittest
from day4 import Day4

class TestDay4(unittest.TestCase):
    def test_run(self):        
        day = Day4("""[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""".split("\n"))
        day.run()
        self.assertEqual(day.entry_max['minutes_asleep'], 50)
        
    def test_minutes_between(self):
        d = Day4([])
        d1 = {
                'minute': 1,
                'hour': 0,
                'month': 3,
                'day': 15,
                'year': 1518
            }
        d2 = {
                'minute': 31,
                'hour': 0,
                'month': 3,
                'day': 15,
                'year': 1518
            }
        self.assertEqual(d.minutes_between_dates(d1, d2), 30)
        self.assertEqual(d.minutes_between_dates(d2, d1), 30)
        
    def test_load(self):
        lines = [
            '[1518-03-15 00:01] Guard #709 begins shift',
            '[1518-03-15 00:12] falls asleep',
            '[1518-03-15 00:53] wakes up'
        ]
        result = Day4([]).load(lines)
        print(result)
        self.assertDictEqual(result[0], {
            'guard': 709,
            'events': [
                {
                    'date': {
                        'minute': 1,
                        'hour': 0,
                        'month': 3,
                        'day': 15,
                        'year': 1518
                        },
                    'action': 'begin',
                    'guard': 709
                },
                {
                    'action': 'asleep',
                    'date': {
                        'minute': 12,
                        'hour': 0,
                        'month': 3,
                        'day': 15,
                        'year': 1518
                    }
                },
                {
                    'action': 'awake',
                    'date': {
                        'minute': 53,
                        'hour': 0,
                        'month': 3,
                        'day': 15,
                        'year': 1518
                    }
                }
            ]
        })

    def test_parse(self):
        result = Day4([]).parse("[1518-11-01 00:00] Guard #10 begins shift")
        print(result)
        self.assertEqual(result, {
            'guard': 10,
            'date': {'minute': 0,
            'hour': 0,
            'month': 11,
            'day': 1,
            'year': 1518},
            'action': 'begin'
        })
        
    def test_parse_asleep(self):
        result = Day4([]).parse("[1518-11-01 00:00] falls asleep")
        print(result)
        self.assertEqual(result, {
            'date': {'minute': 0,
            'hour': 0,
            'month': 11,
            'day': 1,
            'year': 1518},
            'action': 'asleep'
        })
        
        
    def test_parse_awake(self):
        result = Day4([]).parse("[1518-11-01 00:00] wakes up")
        print(result)
        self.assertEqual(result, {
            'date': {'minute': 0,
            'hour': 0,
            'month': 11,
            'day': 1,
            'year': 1518},
            'action': 'awake'
        })

if __name__ == '__main__':
    unittest.main()
