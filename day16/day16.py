from collections import defaultdict

global memo
memo = {}

def advance_time(pressures, opened):
    s = 0
    for x in opened:
        s += pressures[x]
    return s

#with open("test.txt") as file:
with open("day16.txt") as file:
    data = [x.strip() for x in file.readlines()]
    p1 = 0

    pressures = {}
    state = defaultdict(list)
    for line in data:
        parts = line.split()
        valve = parts[1]
        flow = int(parts[4].split("=")[1][:-1])
        pressures[valve] = flow
        for dest in parts[9:]:
            if "," in dest:
                dest = dest[:-1]
            state[valve].append(dest)
        if flow > 0:
            state[valve].append("open "+valve)

    num_openable = sum([1 if pressures[x] > 0 else 0 for x in pressures])
    print("Can open", num_openable)

    def solver(pressures, state, num_openable, cur, minutes_left, opened):
        global memo

        k = "".join(sorted(opened.keys()))
        if (cur, minutes_left, k) in memo:
            return memo[(cur, minutes_left, k)]

        # out of time, end condition
        assert minutes_left >= 0
        if minutes_left == 0:
            memo[(cur, 0, k)] = 0
            return 0

        # nothing else to open, just return the rest of the sim.
        if len(opened) == num_openable:
            memo[(cur, minutes_left, k)] = advance_time(pressures, opened) * minutes_left
            return advance_time(pressures, opened) * minutes_left

        choices = [0]
        # Try the options from here
        for dest in state[cur]:
            next_opened = dict(opened)
            if "open" in dest:
                id = dest.split(" ")[1]
                next_opened[id] = 1
                choices.append(solver(pressures, state, num_openable, cur, minutes_left-1, next_opened))
            else:
                choices.append(solver(pressures, state, num_openable, dest, minutes_left-1, next_opened))
        s = advance_time(pressures, opened) + max(choices)
        memo[(cur, minutes_left, k)] = s
        return s

    print ("part 1 = ", solver(pressures,state, num_openable, "AA", 30, {}))

