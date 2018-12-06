# --- Day 5: Alchemical Reduction ---
# 
# You've managed to sneak in to the prototype suit manufacturing lab. The Elves
# are making decent progress, but are still struggling with the suit's size
# reduction capabilities.
# 
# While the very latest in 1518 alchemical technology might have solved their
# problem eventually, you can do better. You scan the chemical composition of
# the suit's material and discover that it is formed by extremely long polymers
# (one of which is available as your puzzle input).
# 
# The polymer is formed by smaller units which, when triggered, react with each
# other such that two adjacent units of the same type and opposite polarity are
# destroyed. Units' types are represented by letters; units' polarity is
# represented by capitalization. For instance, r and R are units with the same
# type but opposite polarity, whereas r and s are entirely different types and
# do not react.
# 
# For example:
# 
#     In aA, a and A react, leaving nothing behind.
#     In abBA, bB destroys itself, leaving aA. As above, this then destroys itself, leaving nothing.
#     In abAB, no two adjacent units are of the same type, and so nothing happens.
#     In aabAAB, even though aa and AA are of the same type, their polarities match, and so nothing happens.
# 
# Now, consider a larger example, dabAcCaCBAcCcaDA:
# 
# dabAcCaCBAcCcaDA  The first 'cC' is removed.
# dabAaCBAcCcaDA    This creates 'Aa', which is removed.
# dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
# dabCBAcaDA        No further actions can be taken.
# 
# After all possible reactions, the resulting polymer contains 10 units.
# 
# How many units remain after fully reacting the polymer you scanned? (Note: in
# this puzzle and others, the input is large; if you copy/paste your input,
# make sure you get the whole thing.)
# 
import re
import string


class Day5:
    def __init__(self, input):
        self.input = input

    def trial_strip(self):
        smallest = {'strip_polymer': None, 'length': 10**20}
        for char in string.ascii_lowercase:
            input = self.strip_polymer(self.input, char)
            output = self.collapse_input(input)
            length = len(output)
            if smallest['length'] > length:
                smallest = {'strip_polymer': char, 'length': length}
            print(f'Stripped polymer {char} to {length} length')
        return smallest

    def collapse(self):
        return self.collapse_input(self.input)

    def strip_polymer(self, input, polymer):
        return re.sub(polymer, '', input, flags=re.IGNORECASE)

    def collapse_input(self, input):
        result = None
        iterations = 0
        while True:
            result = self._collapse(input)
            if not result['has_collapsed']: break
            # print(f'prev input="{input}" next_input="{ result["output"] }"')
            input = result['output']
            if len(input) <= 1: break
            iterations += 1

        output = result['output']

        print(f'Got result of length {len(output)} in {iterations} iterations starting with polymer of length {len(self.input)}')
            
        return output

    def _collapse(self, input):
        lower_chars = list(input.lower())
        chars = list(input)
        collapsed = [chars[0]]
        has_collapsed = False

        i = 1
        while i < len(input):
            if lower_chars[i] == lower_chars[i - 1] and chars[i] != chars[i - 1]:
                # do nothing
                collapsed.pop()
                has_collapsed = True
                if i + 1 < len(input):
                    collapsed.append(chars[i + 1])
                i += 1 # do an extra skip because we don't want to evaluaste things next to each other
            else:
                collapsed.append(chars[i])
            i += 1

        return {
            'output': "".join(collapsed),
            'has_collapsed': has_collapsed
        }


if __name__ == '__main__':
    with open('day5.input') as f:
        day5 = Day5(f.read())
        result = day5.collapse()
        # print(f'Got result {result}')
        print(f'Unit count: {len(result)}')
        print(day5.trial_strip())

# Answers:
# a: 10972
# b: 5278

