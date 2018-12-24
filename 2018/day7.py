# --- Day 7: The Sum of Its Parts ---
# 
# You find yourself standing on a snow-covered coastline; apparently, you
# landed a little off course. The region is too hilly to see the North Pole
# from here, but you do spot some Elves that seem to be trying to unpack
# something that washed ashore. It's quite cold out, so you decide to risk
# creating a paradox by asking them for directions.
# 
# "Oh, are you the search party?" Somehow, you can understand whatever Elves
# from the year 1018 speak; you assume it's Ancient Nordic Elvish. Could the
# device on your wrist also be a translator? "Those clothes don't look very
# warm; take this." They hand you a heavy coat.
# 
# "We do need to find our way back to the North Pole, but we have higher
# priorities at the moment. You see, believe it or not, this box contains
# something that will solve all of Santa's transportation problems - at least,
# that's what it looks like from the pictures in the instructions." It doesn't
# seem like they can read whatever language it's in, but you can: "Sleigh kit.
# Some assembly required."
# 
# "'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at
# once!" They start excitedly pulling more parts out of the box.
# 
# The instructions specify a series of steps and requirements about which steps
# must be finished before others can begin (your puzzle input). Each step is
# designated by a single letter. For example, suppose you have the following
# instructions:
# 
# Step C must be finished before step A can begin.
# Step C must be finished before step F can begin.
# Step A must be finished before step B can begin.
# Step A must be finished before step D can begin.
# Step B must be finished before step E can begin.
# Step D must be finished before step E can begin.
# Step F must be finished before step E can begin.
# 
# Visually, these requirements look like this:
# 
# 
#   -->A--->B--
#  /    \      \
# C      -->D----->E
#  \           /
#   ---->F-----
# 
# Your first goal is to determine the order in which the steps should be
# completed. If more than one step is ready, choose the step which is first
# alphabetically. In this example, the steps would be completed as follows:
# 
#  * Only C is available, and so it is done first.
#  * Next, both A and F are available. A is first alphabetically, so it is done next.
#  * Then, even though F was available earlier, steps B and D are now also
#    available, and B is the first alphabetically of the three.
#  * After that, only D and F are available. E is not available because only
#    some of its prerequisites are complete. Therefore, D is completed next.
#  * F is the only choice, so it is done next.
#  * Finally, E is completed.
# 
# So, in this example, the correct order is CABDFE.
# 
# In what order should the steps in your instructions be completed?
#
# answer for my input: JDEKPFABTUHOQSXVYMLZCNIGRW

import re
class Day7():
    def __init__(self, time_for_each_task=60, workers=5):
        self.time_for_each_task = time_for_each_task
        self.workers = workers

    def parse(self, line):
        m = re.search("Step (?P<dependency>\w+) must be finished before step (?P<step>\w+) can begin.", line)
        if not m: return None
        return {'step': m.group('step'), 'dependency': m.group('dependency') }

    def merge_entries(self, entries):
        steps = {}
        for entry in entries:
            step = entry['step']
            dependency = entry['dependency']
            if step not in steps:
                steps[step] = set()
            if dependency not in steps:
                steps[dependency] = set()
            steps[step].add(dependency)
        return steps

    def get_order(self, entries):
        # we want to merge the entries together into a dictionary
        steps = self.merge_entries(entries)
        step_list = []

        steps_remaining = set(steps.keys())
        counter = 0
        max_counter = 10000
        while len(steps_remaining) > 0 and counter < max_counter:
            next_steps = set()

            for step in steps_remaining:
                dependencies = steps[step]
                if len(dependencies) == 0:
                    next_steps.add(step)

            next_step = sorted(next_steps)[0]
            step_list.append(next_step)
            
            # then we remove all the next steps from the dependencies
            for step in steps_remaining:
                steps[step] -= {next_step}

            steps_remaining.remove(next_step)
            counter += 1

        if counter >= max_counter:
            print('max iterations {max_counter} exceeded')

        return "".join(step_list)

    def run_a(self, input):
        entries = [day.parse(line) for line in input.splitlines()]
        result = day.get_order(entries)
        print(f'order of entries:\n{result}')

# --- Part Two ---
# 
# As you're about to begin construction, four of the Elves offer to help. "The
# sun will set soon; it'll go faster if we work together." Now, you need to
# account for multiple people working on steps simultaneously. If multiple
# steps are available, workers should still begin them in alphabetical order.
# 
# Each step takes 60 seconds plus an amount corresponding to its letter: A=1,
# B=2, C=3, and so on. So, step A takes 60+1=61 seconds, while step Z takes
# 60+26=86 seconds. No time is required between steps.
# 
# To simplify things for the example, however, suppose you only have help from
# one Elf (a total of two workers) and that each step takes 60 fewer seconds
# (so that step A takes 1 second and step Z takes 26 seconds). Then, using the
# same instructions as above, this is how each second would be spent:
# 
# Second   Worker 1   Worker 2   Done
#    0        C          .        
#    1        C          .        
#    2        C          .        
#    3        A          F       C
#    4        B          F       CA
#    5        B          F       CA
#    6        D          F       CAB
#    7        D          F       CAB
#    8        D          F       CAB
#    9        D          .       CABF
#   10        E          .       CABFD
#   11        E          .       CABFD
#   12        E          .       CABFD
#   13        E          .       CABFD
#   14        E          .       CABFD
#   15        .          .       CABFDE
# 
# Each row represents one second of time. The Second column identifies how many
# seconds have passed as of the beginning of that second. Each worker column
# shows the step that worker is currently doing (or . if they are idle). The
# Done column shows completed steps.
# 
# Note that the order of the steps has changed; this is because steps now take
# time to finish and multiple workers can begin multiple steps simultaneously.
# 
# In this example, it would take 15 seconds for two workers to complete these steps.
# 
# With 5 workers and the 60+ second step durations described above, how long
# will it take to complete all of the steps?
#
# answer: 1048
    def remove_from_work(self, steps, finished_step):
        for dependencies in steps.values():
            dependencies -= {finished_step}
        steps.pop(finished_step)
        return steps

    def get_next_steps(self, steps):
        """These are the things we can work on next"""
        step_list = []

        steps_remaining = set(steps.keys())
        counter = 0
        max_counter = 10000
        next_steps = set()

        for step in steps_remaining:
            dependencies = steps[step]
            if len(dependencies) == 0:
                next_steps.add(step)

        # this is the list of things that can be take for work now
        return sorted(next_steps)

    def get_task_completion(self, current_clock, task):
        return current_clock + self.time_for_each_task + (ord(task) - 64)

    def run_work(self, steps, reporter=lambda report: None, tick_max=100000):
        import sys
        clock = 0
        workers = [{'is_working': False, 'id': i + 1} for i in range(self.workers)]
        done = []
        print(f"Steps: {steps}")
        available_work = self.get_next_steps(steps)
        print(f"Available work: {available_work}")
        pending_work = set()

        while len(steps) > 0:
            for w in workers:
                # complete work
                if w['is_working'] and clock == w['clock_completion']:
                    w['is_working'] = False
                    done.append(w['task'])
                    steps = self.remove_from_work(steps, w['task'])
                    available_work = [task for task in self.get_next_steps(steps) if task not in pending_work]
                    print(f"Available work: {available_work} after completing {w['task']}. steps: {steps}")
                    w.pop('task')
                    w.pop('clock_completion')
                    w.pop('duration')

            for w in workers:
                # assign new work
                if not w['is_working'] and len(available_work) > 0:
                    task = available_work.pop(0)
                    pending_work.add(task)
                    w['is_working'] = True
                    w['task'] = task
                    w['clock_completion'] = self.get_task_completion(clock, task)
                    w['duration'] = w['clock_completion'] - clock

            # logging
            reporter({
                'clock': clock,
                'workers': workers,
                'done': done
            })

            clock += 1

            if clock > tick_max:
                print('Reached MAX TICK. ABORTING')
                return None

        return clock - 1

    def print_run_b_entry(self, entry):
        parts = [str(entry['clock'])]
        for worker in entry['workers']:
            if worker['is_working']:
                parts.append(f"{worker['task']}({worker['duration']}/{worker['clock_completion']})")
            else:
                parts.append('.')
        parts.append("".join(entry['done']))
        print(" | ".join(parts))

    def run_b(self, input):
        entries = [day.parse(line) for line in input.splitlines()]
        merged = day.merge_entries(entries)
        clock = day.run_work(merged, lambda report: self.print_run_b_entry(report))
        print(f'completed in: {clock} ticks')

if __name__ == "__main__":
    import getopt, sys
    day = Day7()
    opts, args = getopt.getopt(sys.argv[1:], "ab", [])

    should_run_b = False
    for o, a in opts:
        if o == "-a":
            pass
        elif o == "-b":
            should_run_b = True
        else:
            assert False, "unhandled option"
    input = ""
    with open('day7.input') as f:
        input = f.read()

    if should_run_b:
        day.run_b(input)
    else:
        day.run_a(input)
