with open("test.txt") as file:
#with open("day19.txt") as file:
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
        geode_cost= (int(parts[27]), 0, 0, int(parts[30]), )
        print(num, ore_cost, clay_cost, obsidian_cost, geode_cost)
        blueprints.append((num, ore_cost, clay_cost, obsidian_cost, geode_cost))
    
    def sim(blueprint, minutes, robots=[1, 0, 0, 0], resources=[0, 0, 0, 0]):
        # ore, clay, obsidian geode
        minute = 0
        while minute < minutes:
            print("Minute ", minute + 1, ": ", end="")

            this_minute_robot = robots.copy()
            # buy
            if resources[0] >= blueprint[4][0] and resources[3] >= blueprint[4][3]:
                print("Build geode robot")
                robots[3] += 1
                resources[0] -= blueprint[4][0]
                resources[3] -= blueprint[4][3]
            elif resources[0] >= blueprint[3][0] and resources[1] >= blueprint[3][1]:
                print("Build obsidian robot")
                robots[2] += 1
                resources[0] -= blueprint[3][0]
                resources[1] -= blueprint[3][0]
            elif resources[0] >= blueprint[2][0]:
                print("Build clay robot")
                robots[1] += 1
                #resources[0] -= blueprint[4][0]
                resources[0] -= blueprint[2][0]
            elif resources[0] >= blueprint[1][0]:
                print("Build ore robot")
                robots[0] += 1
                resources[0] -= blueprint[1][0]
                #resources[1] -= blueprint[0][1]

            # collect
            for type in range(4):                
                resources[type] += this_minute_robot[type]
            print("Resources: ", resources)
            #minutes -= 1  
            minute += 1
        return resources          

    p1 = []
    for blueprint in blueprints:
        (o,c,o,g) = sim(blueprint, 26)
        print("Quality: ", blueprint[0], g)
        p1.append(blueprint[0]*g)

    print("Part 1 =", sum(p1))
    print("Part 2 =", p2)