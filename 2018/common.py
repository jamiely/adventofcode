
def main(day, input_path):
    import sys, getopt
    opts, _ = getopt.getopt(sys.argv[1:], "ab", [])
    should_run_b = False
    for o, a in opts:
        if o == "-a":
            pass
        elif o == "-b":
            should_run_b = True
        else:
            assert False, "unhandled option"
    input = ""
    with open(input_path) as f:
        input = f.read()

    if should_run_b:
        day.runB(input)
    else:
        day.runA(input)