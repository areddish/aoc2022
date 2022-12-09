DIRECTION_OFFSETS = {
    "U": (0,-1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1,0)
}

def simulate_rope(moves, tail_size=1):
    head_loc = [0,0]
    tail_locs = []
    for _ in range(tail_size):
        tail_locs.append([0,0])

    x_range = [0, 0]
    y_range = [0, 0]

    tail_visits = {}
    tail_visits[tuple(tail_locs[tail_size-1])] = 1

    print_board(tail_visits, x_range, y_range, head_loc, tail_locs)

    for line in moves:
        parts = line.split()
        size = int(parts[1])

        for _ in range(size):
            head_loc[0] += DIRECTION_OFFSETS[parts[0]][0]
            head_loc[1] += DIRECTION_OFFSETS[parts[0]][1]

            # update ranges for rendering
            x_range[0] = min(x_range[0], head_loc[0])
            x_range[1] = max(x_range[1], head_loc[0])
            y_range[0] = min(y_range[0], head_loc[1])
            y_range[1] = max(y_range[1], head_loc[1])

            for i in range(tail_size):
                if i == 0:
                    dx = head_loc[0] - tail_locs[0][0]
                    dy = head_loc[1] - tail_locs[0][1]
                else:
                    dx = tail_locs[i-1][0] - tail_locs[i][0]
                    dy = tail_locs[i-1][1] - tail_locs[i][1]
                
                if abs(dx) > 1 and abs(dy) == 0:
                    tail_locs[i][0] += 1 if dx > 0 else -1
                if abs(dx) == 0 and abs(dy) > 1:
                    tail_locs[i][1] += 1 if dy > 0 else -1
                if (abs(dx) >= 2 and abs(dy)) >= 1 or (abs(dx) == 1 and  abs(dy) >= 2):
                    tail_locs[i][0] += 1 if dx > 0 else -1
                    tail_locs[i][1] += 1 if dy > 0 else -1
                tail_visits[tuple(tail_locs[tail_size-1])] = 1

        #print_board(tail_visits, x_range, y_range, head_loc, tail_locs)
        #time.sleep(1)

    #print_board(tail_visits, x_range, y_range, head_loc, [])
    #print(tail_visits)
    return tail_visits

def print_board(tail_visits, x_range, y_range, head_loc, tail_locs):
    for y in range(y_range[0]-1, y_range[1]+1):
        for x in range(x_range[0]-1, x_range[1]+1):
            if [x,y] == head_loc:
                print("H", end="")
            elif [x,y] in tail_locs:
                for i in range(len(tail_locs)):
                    if [x,y] == tail_locs[i]:
                        print(i+1,end="")
                        break
#                print("T", end="")                
            elif (x,y) == (0,0):
                print("s", end="")
            elif (x,y) in tail_visits:
                print("#", end="")
            else:
                print(".", end="")
        print()

#with open("test.txt") as file:
#with open("test2.txt") as file:
with open("day9.txt") as file:
    data = [x.strip() for x in file.readlines()]
    print("Part 1 =", len(simulate_rope(data, 1)))
    print("Part 2 =", len(simulate_rope(data, 9)))