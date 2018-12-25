# --- Day 13: Mine Cart Madness ---

# 
# A crop of this size requires significant logistics to transport produce,
# soil, fertilizer, and so on. The Elves are very busy pushing things around in
# carts on some kind of rudimentary system of tracks they've come up with.
# 
# Seeing as how cart-and-track systems don't appear in recorded history for
# another 1000 years, the Elves seem to be making this up as they go along.
# They haven't even figured out how to avoid collisions yet.
# 
# You map out the tracks (your puzzle input) and see where you can help.
# 
# Tracks consist of straight paths (| and -), curves (/ and \), and
# intersections (+). Curves connect exactly two perpendicular pieces of track;
# for example, this is a closed loop:
# 
# /----\
# |    |
# |    |
# \----/
class TrackType:
    Empty = '.'
    UpDown = '|'
    LeftRight = '-'
    RightTurn = 'R'
    LeftTurn = 'L'
    Intersection = '+'

class Dir:
    Up = (-1, 0)
    Down = (1, 0)
    Left = (0, -1)
    Right = (0, 1)

class Day13:
    CHAR_DIR_MAPPINGS = {
        '|': TrackType.UpDown,
        '-': TrackType.LeftRight,
        '\\': TrackType.RightTurn,
        '/': TrackType.LeftTurn,
        '+': TrackType.Intersection
    }

    DIR_CHAR_MAPPINGS = {
        TrackType.Empty: ' ',
        TrackType.UpDown: '|',
        TrackType.LeftRight: '-',
        TrackType.RightTurn: '\\',
        TrackType.LeftTurn: '/',
        TrackType.Intersection: '+'
    }

    def __init__(self):
        self.track_counter = 0

    def parse_char(self, char):
        return Day13.CHAR_DIR_MAPPINGS[char] if char in Day13.CHAR_DIR_MAPPINGS else TrackType.Empty

    def parse_line(self, line):
        return [self.parse_char(c) for c in line]

    def parse_input(self, input):
        "loads the input into a two-dimensional array and translates strings to types of pieces"
        return [self.parse_line(line) for line in input.strip().splitlines()]

    def load_tracks(self, parsed):
        "Loads all the tracks in the input"
        # we go through each column, then each row, fniding new tracks. if we
        # find one, we follow it to the end
        track_index = [[None for col in row] for row in parsed]
        tracks = []
        state = {
            'track_index': track_index,
            'tracks': tracks
        }
        for row in range(0, len(parsed)):
            for col in range(0, len(parsed[row])):
                if parsed[row][col] == TrackType.Empty: continue
                if state['track_index'][row][col] is not None: continue
                track = self.load_track(parsed, state, (row, col))
                if track: tracks.append(track)
                if state['track_index'][row][col] is None:
                    state['track_index'][row][col] = []

        return state

    FOLLOW_TRACK_INITIAL_DIR = {
        TrackType.LeftRight: Dir.Right,
        TrackType.UpDown: Dir.Down
    }

    DIR_STR = {
        Dir.Down: 'D',
        Dir.Up: 'U',
        Dir.Left: 'L',
        Dir.Right: 'R'
    }

    NEXT_DIR = {
        Dir.Down: {
            TrackType.UpDown: Dir.Down,
            TrackType.Intersection: Dir.Down,
            TrackType.RightTurn: Dir.Right,
            TrackType.LeftTurn: Dir.Left
        },
        Dir.Up: {
            TrackType.UpDown: Dir.Up,
            TrackType.RightTurn: Dir.Left,
            TrackType.LeftTurn: Dir.Right,
            TrackType.Intersection: Dir.Up
        },
        Dir.Left: {
            TrackType.LeftRight: Dir.Left,
            TrackType.Intersection: Dir.Left,
            TrackType.LeftTurn: Dir.Down,
            TrackType.RightTurn: Dir.Up
        },
        Dir.Right: {
            TrackType.LeftRight: Dir.Right,
            TrackType.Intersection: Dir.Right,
            TrackType.LeftTurn: Dir.Up,
            TrackType.RightTurn: Dir.Down
        }
    }

    def add_indices(self, a, b):
        r1, c1 = a
        r2, c2 = b
        return (r1 + r2, c1+ c2)

    def out_of_bounds(self, parsed, index):
        row, col = index
        if row >= len(parsed): return True
        if col >= len(parsed[row]): return True
        return False

    def load_track(self, parsed, state, index, last_dir = None):
        # follow the track until we reach the original position
        original_index = index
        track_indices = []

        while True:
            if self.out_of_bounds(parsed, index):
                print(f'out of bounds!! index={index}')
                break

            row, col = index
            track_type = parsed[row][col]
            if last_dir is None and (track_type == TrackType.LeftTurn or track_type == TrackType.RightTurn):
                print('Cannot process turn as first track')
                return None

            if last_dir is None:
                track_id = self.track_counter
                self.track_counter += 1
                last_dir = Day13.FOLLOW_TRACK_INITIAL_DIR[track_type]
                print(f'last_dir empty so initialized to {Day13.DIR_STR[last_dir]} using track_type={track_type}')

            if last_dir not in Day13.NEXT_DIR:
                print(f'bad last_dir={last_dir}')
            elif track_type not in Day13.NEXT_DIR[last_dir]:
                print(f'bad track_Type={track_type} from last_dir={Day13.DIR_STR[last_dir]}')
            else:
                next_dir = Day13.NEXT_DIR[last_dir][track_type]

            track_indices.append(index)

            if not state['track_index'][row][col]:
                state['track_index'][row][col] = []

            state['track_index'][row][col].append(track_id)

            next_index = self.add_indices(index, next_dir)
            print(f'id={track_id} index={index} next_index={next_index} track_type={track_type} last_dir={Day13.DIR_STR[last_dir]} next_dir={Day13.DIR_STR[next_dir]}')
            if next_index == original_index:
                # we reached the original index
                print('Reached first track piece')
                break
            index = next_index
            last_dir = next_dir
        
        return {
            'starting_index': index,
            'indicies': track_indices,
            'id': track_id
        }


    def render_raw(self, raw):
        return "\n".join(["".join([Day13.DIR_CHAR_MAPPINGS[char] for char in row]) for row in raw])

# 
# Intersections occur when two perpendicular paths cross. At an intersection, a
# cart is capable of turning left, turning right, or continuing straight. Here
# are two loops connected by two intersections:
# 
# /-----\
# |     |
# |  /--+--\
# |  |  |  |
# \--+--/  |
#    |     |
#    \-----/
# 
# Several carts are also on the tracks. Carts always face either up (^), down
# (v), left (<), or right (>). (On your initial map, the track under each cart
# is a straight path matching the direction the cart is facing.)
# 
# Each time a cart has the option to turn (by arriving at any intersection), it
# turns left the first time, goes straight the second time, turns right the
# third time, and then repeats those directions starting again with left the
# fourth time, straight the fifth time, and so on. This process is independent
# of the particular intersection at which the cart has arrived - that is, the
# cart has no per-intersection memory.
# 
# Carts all move at the same speed; they take turns moving a single step at a
# time. They do this based on their current location: carts on the top row move
# first (acting from left to right), then carts on the second row move (again
# from left to right), then carts on the third row, and so on. Once each cart
# has moved one step, the process repeats; each of these loops is called a
# tick.
# 
# For example, suppose there are two carts on a straight track:
# 
# |  |  |  |  |
# v  |  |  |  |
# |  v  v  |  |
# |  |  |  v  X
# |  |  ^  ^  |
# ^  ^  |  |  |
# |  |  |  |  |
# 
# First, the top cart moves. It is facing down (v), so it moves down one
# square. Second, the bottom cart moves. It is facing up (^), so it moves up
# one square. Because all carts have moved, the first tick ends. Then, the
# process repeats, starting with the first cart. The first cart moves down,
# then the second cart moves up - right into the first cart, colliding with it!
# (The location of the crash is marked with an X.) This ends the second and
# last tick.
# 
# Here is a longer example:
# 
# /->-\        
# |   |  /----\
# | /-+--+-\  |
# | | |  | v  |
# \-+-/  \-+--/
#   \------/   
# 
# /-->\        
# |   |  /----\
# | /-+--+-\  |
# | | |  | |  |
# \-+-/  \->--/
#   \------/   
# 
# /---v        
# |   |  /----\
# | /-+--+-\  |
# | | |  | |  |
# \-+-/  \-+>-/
#   \------/   
# 
# /---\        
# |   v  /----\
# | /-+--+-\  |
# | | |  | |  |
# \-+-/  \-+->/
#   \------/   
# 
# /---\        
# |   |  /----\
# | /->--+-\  |
# | | |  | |  |
# \-+-/  \-+--^
#   \------/   
# 
# /---\        
# |   |  /----\
# | /-+>-+-\  |
# | | |  | |  ^
# \-+-/  \-+--/
#   \------/   
# 
# /---\        
# |   |  /----\
# | /-+->+-\  ^
# | | |  | |  |
# \-+-/  \-+--/
#   \------/   
# 
# /---\        
# |   |  /----<
# | /-+-->-\  |
# | | |  | |  |
# \-+-/  \-+--/
#   \------/   
# 
# /---\        
# |   |  /---<\
# | /-+--+>\  |
# | | |  | |  |
# \-+-/  \-+--/
#   \------/   
# 
# /---\        
# |   |  /--<-\
# | /-+--+-v  |
# | | |  | |  |
# \-+-/  \-+--/
#   \------/   
# 
# /---\        
# |   |  /-<--\
# | /-+--+-\  |
# | | |  | v  |
# \-+-/  \-+--/
#   \------/   
# 
# /---\        
# |   |  /<---\
# | /-+--+-\  |
# | | |  | |  |
# \-+-/  \-<--/
#   \------/   
# 
# /---\        
# |   |  v----\
# | /-+--+-\  |
# | | |  | |  |
# \-+-/  \<+--/
#   \------/   
# 
# /---\        
# |   |  /----\
# | /-+--v-\  |
# | | |  | |  |
# \-+-/  ^-+--/
#   \------/   
# 
# /---\        
# |   |  /----\
# | /-+--+-\  |
# | | |  X |  |
# \-+-/  \-+--/
#   \------/   
# 
# After following their respective paths for a while, the carts eventually
# crash. To help prevent crashes, you'd like to know the location of the first
# crash. Locations are given in X,Y coordinates, where the furthest left column
# is X=0 and the furthest top row is Y=0:
# 
#            111
#  0123456789012
# 0/---\        
# 1|   |  /----\
# 2| /-+--+-\  |
# 3| | |  X |  |
# 4\-+-/  \-+--/
# 5  \------/   
# 
# In this example, the location of the first crash is 7,3.
# 

if __name__ == "__main__":
    import common
    day = Day13()
    common.main(day, 'day13.input')