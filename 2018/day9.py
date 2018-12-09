# --- Day 9: Marble Mania ---
# 
# You talk to the Elves while you wait for your navigation system to
# initialize. To pass the time, they introduce you to their favorite marble
# game.
# 
# The Elves play this game by taking turns arranging the marbles in a circle
# according to very particular rules. The marbles are numbered starting with 0
# and increasing by 1 until every marble has a number.
# 
# First, the marble numbered 0 is placed in the circle. At this point, while it
# contains only a single marble, it is still a circle: the marble is both
# clockwise from itself and counter-clockwise from itself. This marble is
# designated the current marble.
# 
# Then, each Elf takes a turn placing the lowest-numbered remaining marble into
# the circle between the marbles that are 1 and 2 marbles clockwise of the
# current marble. (When the circle is large enough, this means that there is
# one marble between the marble that was just placed and the current marble.)
# The marble that was just placed then becomes the current marble.
# 
# However, if the marble that is about to be placed has a number which is a
# multiple of 23, something entirely different happens. First, the current
# player keeps the marble they would have placed, adding it to their score. In
# addition, the marble 7 marbles counter-clockwise from the current marble is
# removed from the circle and also added to the current player's score. The
# marble located immediately clockwise of the marble that was removed becomes
# the new current marble.
# 
# For example, suppose there are 9 players. After the marble with value 0 is
# placed in the middle, each player (shown in square brackets) takes a turn.
# The result of each of those turns would produce circles of marbles like this,
# where clockwise is to the right and the resulting current marble is in
# parentheses:
# 
# [-] (0)
# [1]  0 (1)
# [2]  0 (2) 1 
# [3]  0  2  1 (3)
# [4]  0 (4) 2  1  3 
# [5]  0  4  2 (5) 1  3 
# [6]  0  4  2  5  1 (6) 3 
# [7]  0  4  2  5  1  6  3 (7)
# [8]  0 (8) 4  2  5  1  6  3  7 
# [9]  0  8  4 (9) 2  5  1  6  3  7 
# [1]  0  8  4  9  2(10) 5  1  6  3  7 
# [2]  0  8  4  9  2 10  5(11) 1  6  3  7 
# [3]  0  8  4  9  2 10  5 11  1(12) 6  3  7 
# [4]  0  8  4  9  2 10  5 11  1 12  6(13) 3  7 
# [5]  0  8  4  9  2 10  5 11  1 12  6 13  3(14) 7 
# [6]  0  8  4  9  2 10  5 11  1 12  6 13  3 14  7(15)
# [7]  0(16) 8  4  9  2 10  5 11  1 12  6 13  3 14  7 15 
# [8]  0 16  8(17) 4  9  2 10  5 11  1 12  6 13  3 14  7 15 
# [9]  0 16  8 17  4(18) 9  2 10  5 11  1 12  6 13  3 14  7 15 
# [1]  0 16  8 17  4 18  9(19) 2 10  5 11  1 12  6 13  3 14  7 15 
# [2]  0 16  8 17  4 18  9 19  2(20)10  5 11  1 12  6 13  3 14  7 15 
# [3]  0 16  8 17  4 18  9 19  2 20 10(21) 5 11  1 12  6 13  3 14  7 15 
# [4]  0 16  8 17  4 18  9 19  2 20 10 21  5(22)11  1 12  6 13  3 14  7 15 
# [5]  0 16  8 17  4 18(19) 2 20 10 21  5 22 11  1 12  6 13  3 14  7 15 
# [6]  0 16  8 17  4 18 19  2(24)20 10 21  5 22 11  1 12  6 13  3 14  7 15 
# [7]  0 16  8 17  4 18 19  2 24 20(25)10 21  5 22 11  1 12  6 13  3 14  7 15
# 
# The goal is to be the player with the highest score after the last marble is
# used up. Assuming the example above ends after the marble numbered 25, the
# winning score is 23+9=32 (because player 5 kept marble 23 and removed marble
# 9, while no other player got any points in this very short example game).
# 
# Here are a few more examples:
# 
#     10 players; last marble is worth 1618 points: high score is 8317
#     13 players; last marble is worth 7999 points: high score is 146373
#     17 players; last marble is worth 1104 points: high score is 2764
#     21 players; last marble is worth 6111 points: high score is 54718
#     30 players; last marble is worth 5807 points: high score is 37305
# 
# What is the winning Elf's score?
# 
# 478 players; last marble is worth 71240 points: high score is 375465

from blist import blist

class Day9:
    def play(self, player_count, turns, reporter = lambda a: None):
        marbles = turns
        state = blist([0])
        players = [0 for i in range(player_count)]
        # zero indexed player
        current_player = 0
        current_index = 0
        for marble in range(1, marbles + 1):
            if marble % 10000 == 0:
                print(f"{int(marble/marbles * 100)}% complete")
            projected_insert_location = current_index + 2
            previous_len = len(state)

            marble_was_removed = False
            if marble % 23 == 0:
                players[current_player] += marble
                projected_insert_location = current_index - 7
                if projected_insert_location < 0:
                    insert_location = len(state) + projected_insert_location
                else: insert_location = projected_insert_location
                removed_marble = state.pop(insert_location)
                players[current_player] += removed_marble
                marble_was_removed = True
            elif projected_insert_location == previous_len:
                insert_location = projected_insert_location
            elif projected_insert_location == previous_len + 1:
                insert_location = 1
            elif projected_insert_location == previous_len + 2:
                insert_location = 2
            else: insert_location = projected_insert_location

            if not marble_was_removed: state.insert(insert_location, marble)
            
            last_index = current_index
            current_index = insert_location

            entry = {
                'state': state,
                'previous_len': previous_len,
                'insert_location': insert_location,
                'projected_insert_location': projected_insert_location,
                'last_index': last_index,
                'current_index': current_index,
                'marble': marble,
                'player': current_player + 1
            }
            reporter(entry)
            current_player += 1
            current_player = current_player % player_count

        return players

    def entry_formatter(self, entry):
        state = [str(i) for i in entry['state']]
        state[entry['current_index']] = f"({state[entry['current_index']]})"
        state_list = " ".join(state)
        return f"[{entry['player']}] {state_list}"


    def get_max_score(self, players):
        return max(players)
    
    def print_scores(self, player):
        updated = [entry if entry % 23 != 0 else f">{entry}" for entry in player]
        return f"{sum(player)}: {updated}"

    def entry_formatter2(self, entry):
        # print(f"Entry: {entry}")
        state = [str(i) for i in entry['state']]
        current = state[entry['index']]
        state[entry['index']] = f"({current})"

        line = f"[{entry['player'] + 1}] {' '.join(state)}"

        return line

    def runA(self, input):
        day = Day9()
        player_count = 478
        turns = 71240
        players = day.play(player_count = player_count, turns = turns)
        max_score = day.get_max_score(players)
        print(f"{player_count} players; last marble is worth {turns} points: high score is {max_score}")
        # 478 players; last marble is worth 71240 points

# --- Part Two ---
# 
# Amused by the speed of your answer, the Elves are curious:
# 
# What would the new winning Elf's score be if the number of the last marble
# were 100 times larger?
# 
# 478 players; last marble is worth 7124000 points: high score is 3037741441

    def runB(self, input):
        day = Day9()
        player_count = 478
        turns = 71240 * 100
        players = day.play(player_count = player_count, turns = turns)
        max_score = day.get_max_score(players)
        print(f"{player_count} players; last marble is worth {turns} points: high score is {max_score}")

if __name__ == "__main__":
    import sys, getopt
    opts, _ = getopt.getopt(sys.argv[1:], "ab", [])
    day = Day9()
    should_run_b = False
    for o, a in opts:
        if o == "-a":
            pass
        elif o == "-b":
            should_run_b = True
        else:
            assert False, "unhandled option"
    input = ""
    with open('day8.input') as f:
        input = f.read()

    if should_run_b:
        day.runB(input)
    else:
        day.runA(input)
