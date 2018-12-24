import unittest
from day12 import Day12
from day12 import State

class TestDay12(unittest.TestCase):
    def test_parse_state(self):
        result = Day12().parse_state("initial state: #..")
        self.assertDictEqual(result, {
            'category': 'initial_state',
            'state': ['#', '.', '.']
        })
    def test_parse_rule(self):
        result = Day12().parse_rule(".#. => .")
        self.assertDictEqual(result, {
            'id': 0,
            'category': 'rule',
            'pattern': ['.', '#', '.'],
            'result': '.'
        })

    def test_init_state(self):
        result = Day12().init_state(list('###'))
        self.assertDictEqual(result, {
            'first_index': -3,
            'origin_index': 3,
            'length': 3 * 7,
            'state': list('...###...............')
        })

    def test_load_input(self):
        day = Day12()
        result = day.load_input(TestDay12.input1)
        self.assertTrue(result['initial_state'] is not None)
        self.assertEqual(len(result['rules']), 14)

    def test_run_a(self):
        day = Day12()
        result = day.runA(TestDay12.input1)
        self.assertEqual(result['sum_of_pot_numbers'], 325)

    def test_run_b_small_in(self):
        day = Day12()
        result = day.runB(TestDay12.input1)
        self.assertEqual(result, 999999999374)

    def test_run_b(self):
        day = Day12()
        result = day.runB(self.get_real_input())
        self.assertEqual(result, 4350000000957)

    def test_state_pattern_at(self):
        day = Day12()
        input = day.load_input(TestDay12.input1)
        state_list = day.init_state(input['initial_state']['state'])
        state = State(state_list)
        self.assertEqual(state.pattern_at(0), list('..#..'))
        self.assertEqual(state.pattern_at(3), list('..#.#'))

    def test_get_rule_result(self):
        state = { 'current_state': list('....#') }
        rule = {
            'id': 0,
            'pattern': list('....#'),
            'result': '#'
        }
        result = Day12().get_rule_result(state, 2, rule)
        self.assertDictEqual(result, {
            'rule_id': 0,
            'index': 2,
            'value': '#'
        })

    def test_apply_rule_results_to_state(self):
        state = { 'current_state': list('...') }
        rule = {
            'id': 0,
            'pattern': list('.....'),
            'result': '#'
        }
        day = Day12()
        results = day.get_rules_results_for_all_indices(state, [rule])
        day.apply_rule_results_to_state(state, results)
        self.assertEqual(state['current_state'], list('###'))

    def test_get_rules_results_for_all_indices(self):
        state = { 'current_state': list('...') }
        rule = {
            'id': 0,
            'pattern': list('.....'),
            'result': '#'
        }
        result = Day12().get_rules_results_for_all_indices(state, [rule])
        self.assertEqual(len(result), 3)
        self.assertEqual(result, [{
            'rule_id': 0,
            'index': 0,
            'value': '#'
        }, {
            'rule_id': 0,
            'index': 1,
            'value': '#'
        }, {
            'rule_id': 0,
            'index': 2,
            'value': '#'
        }
        ])


    def test_get_rules_results(self):
        state = { 'current_state': list('.....') }
        rule = {
            'id': 0,
            'pattern': list('.....'),
            'result': '#'
        }
        result = Day12().get_rules_results(state, 2, [rule])
        self.assertDictEqual(result[0], {
            'rule_id': 0,
            'index': 2,
            'value': '#'
        })

    def get_real_input(self):
        with open('day12.input') as f:
            return f.read()

    input1 = """
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
""".strip()

    input2 = """
initial state: #..#.#..##......###...###

...## => #
""".strip()



if __name__ == "__main__":
    unittest.main()
