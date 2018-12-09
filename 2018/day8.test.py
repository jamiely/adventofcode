import unittest
from day8 import Day8

class TestDay8(unittest.TestCase):
    def test_example(self):
        self.assertEqual(1, 1)

    def test_add_metadata(self):
        day = Day8()
        tree = day.parse("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2")
        result = day.add_all_metadata(tree)
        self.assertEqual(result, 138)

    def test_value_of_node(self):
        day = Day8()
        tree = day.parse("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2")
        value = day.value_of_node(tree)
        self.assertEqual(value, 66)

    def test_value_of_node1(self):
        day = Day8()
        tree = { 'label': 'D', 'metadata': [99], 'metadata_count': 1, 'children_count': 0, 'children': [] }
        value = day.value_of_node(tree)
        self.assertEqual(value, 99)

    def test_parse(self):
        day = Day8()
        result = day.parse("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2")

        print(result)
        self.assertDictEqual(result, {
            'label': 'A',
            'metadata': [1,1,2],
            'metadata_count': 3,
            'children_count': 2,
            'children': [
                {
                    'label': 'B',
                    'metadata': [10, 11, 12],
                    'metadata_count': 3,
                    'children_count': 0,
                    'children': []
                },
                {
                    'label': 'C',
                    'metadata': [2],
                    'metadata_count': 1,
                    'children_count': 1,
                    'children': [
                        {
                            'label': 'D',
                            'metadata': [99],
                            'metadata_count': 1,
                            'children_count': 0,
                            'children': []
                        }
                    ]
                }
            ]
        })

if __name__ == "__main__":
    unittest.main()
