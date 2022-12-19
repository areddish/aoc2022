import sys
from collections import defaultdict

#with open("test.txt") as file:
with open("day19.txt" if len(sys.argv[1]) < 1 else sys.argv[1]) as file:
#with open("day19.txt") as file:
    data = [x.strip() for x in file.readlines()]
    p1 = 0
    p2 = 0

    global state_memo
    state_memo = defaultdict(list)
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

    ORE, CLAY, OBSIDIAN, GEODE, ORE_ROBOT, CLAY_ROBOT, OBSIDIAN_ROBOT, GEODE_ROBOT = list(range(8))    

    def collect(state, max_spend):
        if state[ORE] < max_spend[ORE] * 2:
            state[ORE] += state[ORE_ROBOT]
        if state[CLAY] < max_spend[CLAY] * 2:            
            state[CLAY] += state[CLAY_ROBOT]
        if state[OBSIDIAN] < max_spend[OBSIDIAN] * 2:
            state[OBSIDIAN] += state[OBSIDIAN_ROBOT]
        state[GEODE] += state[GEODE_ROBOT]
        return state
        
    def sim(blueprint, minutes):
        global state_memo        

        max_spend = (max([blueprint[x][0] for x in range(1,5)])+1, max([blueprint[x][1] for x in range(1,5)])+1, max([blueprint[x][2] for x in range(1,5)])+1, max([blueprint[x][3] for x in range(1,5)])+1)
        states = { (0,0,0,0,1,0,0,0): 1 }

        # ore, clay, obsidian geode
        minute = 0
        while minute < minutes:
            #print("Minute ", minute + 1, ": ", end="")
            next_state = {}
            for ss in states:
                s = list(ss)
                # if ss in state_memo:
                #     for x in state_memo:
                #         next_state[x] = 1
                #     continue

                #this_minute_robot = outcome["robots"].copy()
                # buy
                if s[ORE] >= blueprint[4][ORE] and s[OBSIDIAN] >= blueprint[4][OBSIDIAN]:
                    # Always build a geode robot if we can
                    s_new = collect(list(s), max_spend)
                    s_new[GEODE_ROBOT] += 1
                    s_new[ORE] -= blueprint[4][ORE]
                    s_new[OBSIDIAN] -= blueprint[4][OBSIDIAN]
                    next_state[tuple(s_new)] = 1
                    # state_memo[ss].append(tuple(s_new))
                if s[OBSIDIAN_ROBOT] < max_spend[OBSIDIAN] and s[ORE] >= blueprint[3][ORE] and s[CLAY] >= blueprint[3][CLAY]:
                #if s[ORE] >= blueprint[3][ORE] and s[CLAY] >= blueprint[3][CLAY]:
                    #print("Build obsidian robot")
                    s_new = collect(list(s), max_spend)
                    s_new[OBSIDIAN_ROBOT] += 1
                    s_new[ORE] -= blueprint[3][ORE]
                    s_new[CLAY] -= blueprint[3][CLAY]
                    next_state[tuple(s_new)] = 1
                    # state_memo[ss].append(tuple(s_new))
                if s[CLAY_ROBOT] < max_spend[CLAY] and s[ORE] >= blueprint[2][0]:
                #if s[ORE] >= blueprint[2][ORE]:
                    #print("Build clay robot")
                    s_new = collect(list(s), max_spend)
                    s_new[CLAY_ROBOT] += 1
                    s_new[ORE] -= blueprint[2][ORE]
                    next_state[tuple(s_new)] = 1
                    # state_memo[ss].append(tuple(s_new))
                if s[ORE_ROBOT] < max_spend[ORE] and s[ORE] >= blueprint[1][0]:
                #if s[ORE] >= blueprint[1][ORE]:                    
                    s_new = collect(list(s), max_spend)
                    s_new[ORE_ROBOT] += 1
                    s_new[ORE] -= blueprint[1][ORE]
                    next_state[tuple(s_new)] = 1
                    # state_memo[ss].append(tuple(s_new))
                next_state[tuple(collect(s, max_spend))] = 1
                #print(tuple(collect(s, max_spend)), max_spend)
                # state_memo[ss].append(tuple(collect(s)))
            #minutes -= 1  
            states = next_state
            print(len(states))

            # Only keep top 2000 states
            # Score is sum of states
            #states = sorted(states.keys(), key=lambda x:sum(x), reverse=True)[:10000]

            # do we have any geode_robots? if so those solutions are preferable
            # preferred_states = {}
            # for s in states:
            #     if s[GEODE_ROBOT] > 0 or s[OBSIDIAN] > 0:
            #         preferred_states[s] = 1
            # if preferred_states:
            #     states = preferred_states

            minute += 1

        max_geodes = 0
        best = (0,0,0,0, 0,0,0,0)
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
    print("Part 2 =", p2)


    # 2275 - too low
