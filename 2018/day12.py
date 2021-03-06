import re

class Day12:
# --- Day 12: Subterranean Sustainability ---
# 
# The year 518 is significantly more underground than your history books
# implied. Either that, or you've arrived in a vast cavern network under the
# North Pole.
# 
# After exploring a little, you discover a long tunnel that contains a row of
# small pots as far as you can see to your left and right. A few of them
# contain plants - someone is trying to grow things in these
# geothermally-heated caves.
# 
# The pots are numbered, with 0 in front of you. To the left, the pots are
# numbered -1, -2, -3, and so on; to the right, 1, 2, 3.... Your puzzle input
# contains a list of pots from 0 to the right and whether they do (#) or do not
# (.) currently contain a plant, the initial state. (No other pots currently
# contain plants.) For example, an initial state of #..##.... indicates that
# pots 0, 3, and 4 currently contain plants.
    def __init__(self):
        self.has_parsed_initial_state = False
        self.rule_counter = 0

    def parse_state(self, line):
        "initial state: #..#.#..##......###...###"
        m = re.search(r"initial state: (?P<state>[\.#]+)", line)
        if not m: return None

        state = m.group('state')
        return {
            'category': 'initial_state',
            'state': list(state)
        }


# 
# Your puzzle input also contains some notes you find on a nearby table:
# someone has been trying to figure out how these plants spread to nearby pots.
# Based on the notes, for each generation of plants, a given pot has or does
# not have a plant based on whether that pot (and the two pots on either side
# of it) had a plant in the last generation. These are written as LLCRR => N,
# where L are pots to the left, C is the current pot being considered, R are
# the pots to the right, and N is whether the current pot will have a plant in
# the next generation. For example:
# 
#     A note like ..#.. => . means that a pot that contains a plant but with no
#     plants within two pots of it will not have a plant in it during the next
#     generation.
#
#     A note like ##.## => . means that an empty pot with two plants on each side
#     of it will remain empty in the next generation.
#
#     A note like .##.# => # means that a pot has a plant in a given generation if,
#     in the previous generation, there were plants in that pot, the one
#     immediately to the left, and the one two pots to the right, but not in the
#     ones immediately to the right and two to the left.
# 
    def parse_rule(self, line):
        "...## => #"
        m = re.search(r"(?P<pattern>[\.#]+) => (?P<result>[\.#])", line)
        if not m: return None

        id = self.rule_counter
        self.rule_counter += 1

        return {
            'id': id,
            'category': 'rule',
            'pattern': list(m.group('pattern')),
            'result': m.group('result')
        }

    def parse(self, line):
        if self.has_parsed_initial_state:
            return self.parse_rule(line)

        result = self.parse_state(line)
        if result:
            self.has_parsed_initial_state = True
            return result

    def apply_rule_results_to_state(self, state, results):
        current = ['.'] * len(state['current_state'])
        #current = state['current_state']
        # print(f'results: {results}')
        for result in results:
            current[result['index']] = result['value']

        state['current_state'] = current

    def get_rules_results_for_all_indices(self, state, rules):
        return [result for index in range(0, len(state['current_state'])) for result in self.get_rules_results(state, index, rules)]

    def get_rules_results(self, state, state_index, rules):
        return [result for result in [self.get_rule_result(state, state_index, rule) for rule in rules] if result is not None]

    def get_rule_result(self, state, state_index, rule):
        if 'current_state' not in state:
            print('no current state found')
            return None
        if 'pattern' not in rule:
            print('no rule pattern found')
            return None
        
        for i in range(0, len(rule['pattern'])):
            index = state_index + i - 2 # this assumes that rules are 5 spaces long
            if index < 0 or index >= len(state['current_state']):
                value = '.'
            else:
                value = state['current_state'][index]

            if rule['pattern'][i] == value:
                # print(f'index={index} value={value}')
                continue
            else:
                # print(f'value={value} doesnt match pattern')
                return None

        # print(f'apply rule to state_index={state_index}')
        if 'id' not in rule:
            print(f'no id in rule {rule}')
            return None

        # print(f"Matched rule {rule['id']} with pattern {rule['pattern']}")

        return {
            'rule_id': rule['id'],
            'index': state_index,
            'value': rule['result']
        }

    def load_input(self, input):
        entries = map(self.parse, input.strip().splitlines())

        result = {'rules': [], 'initial_state': None}
        for entry in entries:
            if entry is None: continue
            elif entry['category'] == 'initial_state':
                result['initial_state'] = entry
            else:
                result['rules'].append(entry)

        return result

# It's not clear what these plants are for, but you're sure it's important, so
# you'd like to make sure the current configuration of plants is sustainable by
# determining what will happen after 20 generations.
# 
# For example, given the following input:
# 
# initial state: #..#.#..##......###...###
# 
# ```
# ...## => #
# ..#.. => #
# .#... => #
# .#.#. => #
# .#.## => #
# .##.. => #
# .#### => #
# #.#.# => #
# #.### => #
# ##.#. => #
# ##.## => #
# ###.. => #
# ###.# => #
# ####. => #
# ```
# 
# For brevity, in this example, only the combinations which do produce a plant
# are listed. (Your input includes all possible combinations.) Then, the next
# 20 generations will look like this:
#
# ``` 
#                  1         2         3     
#        0         0         0         0     
#  0: ...#..#.#..##......###...###...........
#  1: ...#...#....#.....#..#..#..#...........
#  2: ...##..##...##....#..#..#..##..........
#  3: ..#.#...#..#.#....#..#..#...#..........
#  4: ...#.#..#...#.#...#..#..##..##.........
#  5: ....#...##...#.#..#..#...#...#.........
#  6: ....##.#.#....#...#..##..##..##........
#  7: ...#..###.#...##..#...#...#...#........
#  8: ...#....##.#.#.#..##..##..##..##.......
#  9: ...##..#..#####....#...#...#...#.......
# 10: ..#.#..#...#.##....##..##..##..##......
# 11: ...#...##...#.#...#.#...#...#...#......
# 12: ...##.#.#....#.#...#.#..##..##..##.....
# 13: ..#..###.#....#.#...#....#...#...#.....
# 14: ..#....##.#....#.#..##...##..##..##....
# 15: ..##..#..#.#....#....#..#.#...#...#....
# 16: .#.#..#...#.#...##...#...#.#..##..##...
# 17: ..#...##...#.#.#.#...##...#....#...#...
# 18: ..##.#.#....#####.#.#.#...##...##..##..
# 19: .#..###.#..#.#.#######.#.#.#..#.#...#..
# 20: .#....##....#####...#######....#.#..##.
# ``` 
#
# The generation is shown along the left, where 0 is the initial state. The pot
# numbers are shown along the top, where 0 labels the center pot,
# negative-numbered pots extend to the left, and positive pots extend toward
# the right. Remember, the initial state begins at pot 0, which is not the
# leftmost pot used in this example.
# 
# After one generation, only seven plants remain. The one in pot 0 matched the
# rule looking for ..#.., the one in pot 4 matched the rule looking for .#.#.,
# pot 9 matched .##.., and so on.
# 
# In this example, after 20 generations, the pots shown as # contain plants,
# the furthest left of which is pot -2, and the furthest right of which is pot
# 34. Adding up all the numbers of plant-containing pots after the 20th
# generation produces 325.
# 
# After 20 generations, what is the sum of the numbers of all pots which
# contain a plant?
#
    def init_state(self, initial_state):
        state_len = len(initial_state)
        pad_factor = 7
        new_len = state_len * pad_factor
        padding = ['.' for i in range(state_len)]
        return {
            # 0
            'origin_index': len(padding),
            'first_index': -len(padding),
            'length': new_len,
            'state': padding + initial_state + (padding * (pad_factor - 2))
        }

    def rule_matches(self, rule, pattern):
        return rule['pattern'] == pattern

    def pattern_at(self, state, index):
        lower = index - 2
        upper = index + 3
        if index - 2 < 0: return None
        if index + 3 > len(state): return None

        return self.state['state'][lower:upper]


    def run_a(self, input):
        return self.run_with_generations(input, 20)

    def run_with_generations(self, input, generations):
        initial = self.load_input(input)
        # self.print_rules(initial['rules'])
        initial_state = initial['initial_state']['state']
        rules = initial['rules']
        state = self.init_state(initial_state)
        state['generation'] = 0
        state['current_state'] = state['state']

        cache = {}

        # print(f'run_a with {generations} generations')
        # self.print_state(state)
        exit_generation = None
        last_stats = []
        for i in range(0, generations):
            rule_results = self.get_rules_results_for_all_indices(state, rules)
            self.apply_rule_results_to_state(state, rule_results)
            self.print_state(state)
            state_str = "".join(state['current_state']).strip(".")
            if state_str in cache:
                print(f'i={i} already seen in generation {cache[state_str]}')
                stats = self.get_stats(state)
                stats['generation'] = i
                last_stats.append(stats)
                print(stats)
                if exit_generation is None:
                    exit_generation = i + 3
            else:
                cache[state_str] = i

            if exit_generation and exit_generation == i:
                break
            state['generation'] = i + 1

        stats = self.get_stats(state)
        stats['generation'] = i
        stats['history'] = last_stats
        print(f'Stats: {stats}.')

        return stats

    def compute_sum_of_numbers(self, state):
        return self.get_stats(state)['sum_of_pot_numbers']

    def get_stats(self, state):
        first_index_of_plant = None
        sum = 0
        numbers = []
        for i in range(0, len(state['current_state'])):
            index = i + state['first_index']
            if state['current_state'][i] != '#': continue
            if not first_index_of_plant: first_index_of_plant = i
            sum += index
            numbers.append(i)

        return {
            'first_plant_index': first_index_of_plant, 
            'sum_of_pot_numbers': sum,
            'count_of_pots': len(numbers),
            'pot_numbers': numbers
            }


    def print_state(self, state):
        print(f'{state["generation"]}: {"".join(state["current_state"])}')

    def print_rules(self, rules):
        for rule in rules:
            print(f'{rule["id"]}: {rule["pattern"]} => {rule["result"]}')

    def run_b(self, input):
        max_generation = 1000
        stats = self.run_with_generations(input, max_generation)
        first_plant_index = stats['first_plant_index']
        generation = stats['generation']
        count = stats['count_of_pots']
        delta = first_plant_index - generation

        history = stats['history']
        delta_sum_history = None
        target_generation = 50000000000
        other_sum = None
        if len(history) >= 2:
            history_a = stats['history'][0]
            history_b = stats['history'][1]
            last_history = history[len(history) - 1]
            last_generation = last_history['generation']
            last_sum = last_history['sum_of_pot_numbers']

            delta_sum_history = abs(history_a['sum_of_pot_numbers'] - history_b['sum_of_pot_numbers'])
            generation_delta = target_generation - last_generation - 1
            other_sum = last_sum + generation_delta * delta_sum_history
        
        plant_number = target_generation + delta
        numbers = []
        for i in range(0, count):
            numbers.append(plant_number)
            plant_number += 2

        # answer = sum(numbers)
        answer = other_sum
        print({
            'delta': delta,
            'sum': answer,
            'numbers': numbers,
            'history_count': len(history),
            'other_sum': other_sum,
            'last_sum': last_sum,
            'last_generation': last_generation,
            'delta_sum_history': delta_sum_history
        })

        return answer

    # bad answers:
    # * 4350000009657 too high
    # * 4350000001044 too high
    # * 4350000000957 right answer (off by one error)
    

class State:
    def __init__(self, state):
        self.state = state

    def pattern_at(self, normal_index):
        index = normal_index + self.state['origin_index']
        return self.state['state'][index - 2:index + 3]

    def apply_rule(self):
        pass

if __name__ == "__main__":
    import common
    common.main(Day12(), 'day12.input')

