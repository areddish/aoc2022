import sys
from collections import defaultdict

#with open("test.txt") as file:
#with open("day19.txt" if len(sys.argv[1]) < 1 else sys.argv[1]) as file:
with open("day19.txt") as file:
    data = [x.strip() for x in file.readlines()]
    p1 = 0
    p2 = 0

    blueprints = []
    for line in data:
        parts = line.split()
        num = int(parts[1][:-1])
        ore_cost = (int(parts[6]), 0, 0, 0)
        clay_cost = (int(parts[12]), 0, 0, 0)
        obsidian_cost = (int(parts[18]), int(parts[21]), 0, 0)
        geode_cost= (int(parts[27]), 0, int(parts[30]), 0)
        print(num, ore_cost, clay_cost, obsidian_cost, geode_cost)
        blueprints.append((num, ore_cost, clay_cost, obsidian_cost, geode_cost))

    # Make some constants to help my sanity of using tuples with many parts
    ORE, CLAY, OBSIDIAN, GEODE, ORE_ROBOT, CLAY_ROBOT, OBSIDIAN_ROBOT, GEODE_ROBOT = list(range(8))    

    # Collects ore based on the number of robots.
    # OPTIMIZATION: Limit the growth of resources (and states) by 2x the max we can spend in a minute. 2* is a guess and based on the fact we can
    #               only make one robot per minute/turn.
    def collect(state, max_spend):
        if state[ORE] < max_spend[ORE] * 2:
            state[ORE] += state[ORE_ROBOT]
        if state[CLAY] < max_spend[CLAY] * 2:
            state[CLAY] += state[CLAY_ROBOT]
        if state[OBSIDIAN] < max_spend[OBSIDIAN] * 2:
            state[OBSIDIAN] += state[OBSIDIAN_ROBOT]
        state[GEODE] += state[GEODE_ROBOT]
        return state
        
    # Simulate a blueprint for x minutes. Compute all states we can reach by doing all actions and keep going...
    def sim(blueprint, minutes):
        # Determine how much we can spent for a given minute
        max_spend = (max([blueprint[x][0] for x in range(1,5)])+1, max([blueprint[x][1] for x in range(1,5)])+1, max([blueprint[x][2] for x in range(1,5)])+1, max([blueprint[x][3] for x in range(1,5)])+1)

        # Resources then Robots
        states = { (0,0,0,0,1,0,0,0): 1 }

        minute = 0
        while minute < minutes:
            #print("Minute ", minute + 1, ": ", end="")

            # Clear the next state, we'll fill this in and swap it with our current state.
            next_state = {}
            for s in states:
                # ASSUMPTION: We are greedy with geode opening robots, always buy/build one if possible.
                if s[ORE] >= blueprint[4][ORE] and s[OBSIDIAN] >= blueprint[4][OBSIDIAN]:
                    s_new = collect(list(s), max_spend)
                    s_new[GEODE_ROBOT] += 1
                    s_new[ORE] -= blueprint[4][ORE]
                    s_new[OBSIDIAN] -= blueprint[4][OBSIDIAN]
                    next_state[tuple(s_new)] = 1
                else:
                    # If we can't build a geode opening robot, then we simulate the potential purchases of any of the
                    # other robots + the state of not buying anyting.

                    if s[OBSIDIAN_ROBOT] < max_spend[OBSIDIAN] and s[ORE] >= blueprint[3][ORE] and s[CLAY] >= blueprint[3][CLAY]:
                        #print("Build obsidian robot")
                        s_new = collect(list(s), max_spend)
                        s_new[OBSIDIAN_ROBOT] += 1
                        s_new[ORE] -= blueprint[3][ORE]
                        s_new[CLAY] -= blueprint[3][CLAY]
                        next_state[tuple(s_new)] = 1
                    if s[CLAY_ROBOT] < max_spend[CLAY] and s[ORE] >= blueprint[2][ORE]:
                        #print("Build clay robot")
                        s_new = collect(list(s), max_spend)
                        s_new[CLAY_ROBOT] += 1
                        s_new[ORE] -= blueprint[2][ORE]
                        next_state[tuple(s_new)] = 1
                    if s[ORE_ROBOT] < max_spend[ORE] and s[ORE] >= blueprint[1][ORE]:
                        s_new = collect(list(s), max_spend)
                        s_new[ORE_ROBOT] += 1
                        s_new[ORE] -= blueprint[1][ORE]
                        next_state[tuple(s_new)] = 1
                    next_state[tuple(collect(list(s), max_spend))] = 1
            states = next_state
            #print(len(states))

            # Attempted optimization: Only keep top 2000 states, score is sum of states. - Didn't help much, grew this to 500000
            #states = sorted(states.keys(), key=lambda x:sum(x), reverse=True)[:500000]

            # Attempted optimization: Do we have any geode_robots? if so those solutions are preferable and we can cull anything else
            # This got really close to a solution but was missing some states, i.e. 2275 vs the 2301 real answer. Probably needs some
            # more tweaking as it seems promising.
            # preferred_states = {}
            # for s in states:
            #     if s[GEODE_ROBOT] > 0:
            #         preferred_states[s] = 1
            # if preferred_states:
            #     states = preferred_states

            minute += 1

        # Find the best of the states w.r.t to the # of geodes opened
        max_geodes = 0
        best = (0,0,0,0, 0,0,0,0)   # Default case where we didn't open any, this happens in part 1 alot.
        for s in states:
            if s[GEODE] > max_geodes:
                max_geodes = s[GEODE]
                best = s    
        return best 

    p1 = []
    for blueprint in blueprints:
        (o,c,o,g,ore_r,cr,obs_r,gr) = sim(blueprint, 24)
        print("Quality: ", blueprint[0], g)
        p1.append(blueprint[0]*g)
    print("Part 1 =", sum(p1))

    p2 = 1
    for blueprint in blueprints[:3]:
        (o,c,o,g,ore_r,cr,obs_r,gr) = sim(blueprint, 32)
        print("Geodes opened: ", blueprint[0], g)
        p2 *= g
    print("Part 2 =", p2)