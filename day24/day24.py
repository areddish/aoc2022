from collections import defaultdict, deque

BLIZZ_DIRS = {
    "^": (0,-1),
    "v": (0,1),
    ">": (1,0),
    "<": (-1,0)
}

BLIZ_CHARS = {
    (0,-1): "^",
    (0,1): "v",
    (1,0): ">",
    (-1,0): "<"
}

def print_board(board, blizzards, W, H, cur):
    for y in range(H):
        for x in range(W):
            if (x,y) == cur:
                print("E", end="")
            elif (x,y) in blizzards:
                print(BLIZ_CHARS[blizzards[(x,y)][0]] if len(blizzards[(x,y)]) == 1 else len(blizzards[x,y]), end="")
            else:
                if (x,y) in board:
                    print("#", end="")
                else:
                    print(".", end="")
        print()

#with open("test.txt") as file:
#with open("test2.txt") as file:
with open("day24.txt") as file:
    data = [x.strip() for x in file.readlines()]

    start = (0,0)
    end = (0,0)
    blizzards = defaultdict(list)
    grid = set()
    y = 0
    W = 0
    for line in data:
        row = []
        W = len(line)
        for x, ch in enumerate(line):
            if y == 0 and ch == ".":
                start = (x,y)
            if ch in [">","<","v","^"]:
                blizzards[(x,y)].append(BLIZZ_DIRS[ch])
                row.append(".")
            else:
                if ch == "#":
                    grid.add((x,y))
                elif ch == ".":
                    end = (x,y)
        y += 1
    H = y

    print_board(grid, blizzards, W, H, start)
    print(start, end)

    def nav(start, end, grid, blizzards, W, H):
        print(f"Navigating from {start} to {end}")
        seen = set()
        Q = deque([(start[0], start[1], blizzards, 0)])
        while True:
            cx, cy, blizzards, minute = Q.popleft()
            
            if (cx,cy) == end:
                return (minute, blizzards)

            if (cx,cy, minute) in seen:
                continue  
            seen.add((cx,cy,minute))

            # if minute % 200 == 0:
            #     print("Minute: ", minute, "@ (",cx,",",cy,"): Q", len(Q), "Seen", len(seen))

            # move blizzards:
            next_blizzards = defaultdict(list)
            for coord in blizzards:
                for b in blizzards[coord]:
                    bx,by = coord
                    dx,dy = b
                    nx = bx + dx
                    ny = by + dy
                    if nx < 1:
                        nx = W-2
                    elif nx >= W-1:
                        nx = 1                    
                    if ny < 1:
                        ny = H-2
                    elif ny >= H-1:
                        ny = 1
                    next_blizzards[(nx,ny)].append((dx,dy))
            blizzards = next_blizzards

            # find moves
            for dx,dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx = cx + dx
                ny = cy + dy

                # Hack to deal with part 2
                if (nx,ny) == end:
                    Q.append((nx,ny, blizzards, minute+1))

                if not (1 <= nx <= W-2 and 1 <= ny <= H):
                    continue
                if (nx,ny) in blizzards or (nx, ny) in grid:
                    continue  

                # try the move
                Q.append((nx,ny, blizzards, minute+1))

            if (cx,cy) not in blizzards:
                Q.append((cx,cy,blizzards,minute+1))            

    minutes, blizzards = nav(start, end, grid, blizzards, W, H)
    print("Part 1 =", minutes)
    print()

    minutes_back_to_start, blizzards = nav(end, start, grid, blizzards, W, H)
    minutes += minutes_back_to_start
    print(f"Part 2 (back to start) = {minutes}     delta = +{minutes_back_to_start}")
    minutes_again_to_end, _ = nav(start, end, grid, blizzards, W, H)
    minutes += minutes_again_to_end
    print(f"Part 2 (again to end)  = {minutes}     delta = +{minutes_again_to_end}")