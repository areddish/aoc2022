from collections import defaultdict
NORTH = (0,-1)
SOUTH = (0,1)
EAST = (1,0)
WEST = (-1,0)
NW = (-1,-1)
NE = (1,-1)
SE = (1,1)
SW = (-1,1)

DIRS = {
    "N": lambda x,y: (x,y-1),
    "NE": lambda x,y: (x+1,y-1),
    "NW": lambda x,y: (x-1,y-1),
    "E": lambda x,y: (x+1,y),
    "W": lambda x,y: (x-1,y),
    "S": lambda x,y: (x,y+1),
    "SE": lambda x,y: (x+1,y+1),
    "SW": lambda x,y: (x-1,y+1)    
}

def print_elves(elves):
    maxx = 0
    minx = 1e6
    maxy = 0
    miny = 1e6
    for elf in elves:
        x,y = elf
        maxx = max(maxx, x)
        minx = min(minx, x)
        maxy = max(maxy, y)
        miny = min(miny, y)

    for y in range(miny,maxy+1):
        for x in range(minx,maxx+1):
            if (x,y) in elves:
                print("#", end="")
            else:
                print(".", end="")
        print()

#with open("test2.txt") as file:
#with open("test.txt") as file:
with open("day23.txt") as file:
    data = [x.strip() for x in file.readlines()]
    p1 = 0
    p2 = 0

    elves = set()
    y = 0
    for line in data:
        for i,ch in enumerate(line):
            if ch == "#":
                print("elf at", (i,y))
                elves.add((i,y))
        y += 1

    print_elves(elves)
    #moves = [NORTH, SOUTH, WEST, EAST]
    
    moves = ["N", "S", "W", "E"]
    test_moves = {
        "N": ["N", "NE", "NW"],
        "S": ["S", "SE", "SW"],
        "W": ["W", "SW", "NW"],
        "E": ["E", "NE", "SE"],
    }

    round = 0
    while True:
        #first half
        possible_moves = {}
        not_moving = set()
        for elf in elves:
            ex,ey = elf

            # see if we don't moves..
            adj = 0
            for dir in DIRS:
                if DIRS[dir](ex,ey) in elves:
                    adj += 1
            if adj == 0:
                not_moving.add(elf)
            else:
                for try_dir in moves:               
                    elves_adj = 0 
                    for dir in test_moves[try_dir]:
                        if DIRS[dir](ex,ey) in elves:
                            #print(f"{elf} found neighbor at {DIRS[dir](ex,ey)} while going {try_dir}")
                            elves_adj += 1
                            break
                    if elves_adj == 0:
                        assert elf not in possible_moves
                        possible_moves[elf] = try_dir
                        break
                if elf not in possible_moves:
                    not_moving.add(elf)

        if len(not_moving) == len(elves):
            print("Part 2 =", round + 1)
            break
        
        new_elves = defaultdict(list)
        # try to make moves
        for move in possible_moves:
            ex,ey = move
            new_elves[DIRS[possible_moves[move]](ex,ey)].append((ex,ey))

        elves = set(not_moving)
        for elf in new_elves:
            if len(new_elves[elf]) > 1:
                for old_elf in new_elves[elf]:
                    assert old_elf not in elves
                    elves.add(old_elf)
        for elf in new_elves:
            if len(new_elves[elf]) == 1:
                assert elf not in elves
                elves.add(elf)

        #print_elves(elves)
        temp = moves.pop(0)
        moves.append(temp)
        round += 1

        if round == 10:
            maxx = 0
            minx = 1e6
            maxy = 0
            miny = 1e6
            for elf in elves:
                x,y = elf
                maxx = max(maxx, x)
                minx = min(minx, x)
                maxy = max(maxy, y)
                miny = min(miny, y)
            print(maxx,minx,maxy,miny, len(elves))
            print("Part 1 =", ((maxx-minx+1) * (maxy-miny+1) - len(elves)))