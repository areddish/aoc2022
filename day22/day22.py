LEFT = (-1,0)
RIGHT = (1, 0)
UP = (0,-1)
DOWN = (0,1)
DIRS = [RIGHT, DOWN, LEFT, UP]

def top_most(board, x):
    v = 0
    while board[v][x] == " ":
        v += 1
    return v

def left_most(board, y):
    v = 0
    while board[y][v] == " ":
        v += 1
    return v

def right_most(board, y, w):
    v = w - 1
    while board[y][v] == " ":
        v -= 1
    return v

def bottom_most(board, x, h):
    v = h - 1
    while board[v][x] == " ":
        v -= 1
    return v

def right(dir):
    i = DIRS.index(dir)
    i += 1
    i %= len(DIRS)
    return DIRS[i]

def left(dir):
    i = DIRS.index(dir)
    i -= 1
    i = i if i >=0 else len(DIRS)-1
    return DIRS[i]

def forward(c, r, dir, n, board, wrap_fn):
    nc,nr = c, r
    for i in range(n):
        prev_c = nc
        prev_r = nr
        prev_dir = dir  # !! Hours wasted as I didn't restore this and L62 was changing dir.
        nc = nc + dir[0]
        nr = nr + dir[1]
        nr, nc, dir = wrap_fn(nr, nc, dir)
        if board[nr][nc] == ".":
            continue
        elif board[nr][nc] == "#":
            return prev_c, prev_r, prev_dir
    return nc, nr, dir

def print_board(board, start=None):
    w = len(board[0])
    h = len(board)

    for y in range(h):
        for x in range(w):
            if start and start == (x,y):
                print("*", end="")
            else:
                print(board[y][x], end="")
        print()

#with open("test.txt") as file:
with open("day22.txt") as file:
    p1 = 0
    p2 = 0

    start = (0,0) # To be filled in with upper first
    w = 0
    h = 0

    data = file.read().split("\n\n")
    board = []
    for i, line in enumerate(data[0].split("\n")):
        if i == 0:
            # ASSUMPTION: May not work for all cases, works for test and my input as both start with '.'
            start = (line.index("."), start[1])
        w = max(w, len(line))
        board.append(list(line))    
    h = len(board)

    # Fix up any row missing trailing whitespace
    for y in range(h):
        while len(board[y]) != w:
            board[y].append(" ")

    moves = [("", int(data[1][:2]))]
    i = 2    
    while i < len(data[1]):
        # Get the orientation
        turn = data[1][i]
        i += 1
        # Get the amount to move in that updated orientation
        num = data[1][i]
        i += 1
        while i < len(data[1]) and data[1][i] not in ["L", "R"]:
            num = num + data[1][i]
            i += 1
        moves.append((turn, int(num)))

    #print_board(board, start)
    #print(moves)
        
    dir = RIGHT
    c,r = start
    w = len(board[0])
    h = len(board)
    
    def wrap(nr, nc, dir):
        global w
        global h
        if nc < 0:
            nc = right_most(board, nr, w)
        elif nc >= w:
            nc = left_most(board, nr)
        if nr < 0:
            nr = bottom_most(board, nc, h)
        elif nr >= h:
            nr = top_most(board, nc)

        if board[nr][nc] == " " and dir == LEFT:
            nc = right_most(board, nr, w)
        elif board[nr][nc] == " " and dir == RIGHT:
            nc = left_most(board, nr)
        if board[nr][nc] == " " and dir == UP:
            nr = bottom_most(board, nc, h)
        elif board[nr][nc] == " " and dir == DOWN:
            nr = top_most(board, nc)
        return nr, nc, dir

    def sim(c, r, board, moves, wrap_fn):
        dir = RIGHT
        for turn,n in moves:
            #print(turn,n)
            if turn == "L":
                dir = left(dir)
            elif turn == "R":
                dir = right(dir)
            c, r, dir = forward(c, r, dir, n, board, wrap_fn)
        facing = DIRS.index(dir) 
        return c,r,facing

    p1_c, p1_r, p1_facing = sim(c, r, board, moves, wrap)
    print("Part 1 =", 1000*(p1_r+1)+4*(p1_c+1)+p1_facing)

    def cube_wrap(nr, nc, dir):
        global w
        global h
        
        # Consider our folding liek this, where 3 is the front of the cube looking at it.
        # 5 will be the back, 4 the top, 6 right side, 2, left side, 1 the bottom
        #       0  50  100  150
        #      0|---|---|---|
        #       | X | 5 | 6 |
        #     50|---|---|---|
        #       | X | 4 | X |
        #    100|---|---|---|
        #       | 2 | 3 | X |
        #    150|---|---|---|
        #       | 1 | X | X |
        #    200|---|---|---|

        dw = w // 3
        dh = h // 4
        assert dw == dh
        assert dw == 50

        # wrap moving to the right
        if dir == RIGHT:
            # 6 -> 3
            if 0 <= nr < dh and nc >= w:
                dir = LEFT
                nr = 3*dh-1 - nr
                nc = 2*dw - 1
            # 4 -> 6
            elif dh <= nr < 2*dh and nc >= 2*dw:
                dir = UP
                nc = nr + dh
                nr = dw-1
            # 3 -> 6
            elif 2*dh <= nr < 3*dh and nc >= 2*dw:
                dir = LEFT
                nr = 3*dh-1-nr#(dw - 1) - (nc - 2*dw)
                nc = w - 1
            # 1 -> 3
            elif 3*dh <= nr < h and nc >= dw:
                dir = UP 
                nc = nr-3*dh+dw
                nr = 3*dh-1
        elif dir == LEFT:
            # 5 -> 2
            if 0 <= nr < dh and nc < dw:
                dir = RIGHT
                # 0 maps to 149
                # 49 maps to 100
                nr = 3*dh-1-nr
                nc = 0                
            # 4 -> 2
            elif dh <= nr < 2*dh and nc < dw:
                dir = DOWN
                nc = nr - dh
                nr = 2*dh
            # 2 -> 5
            elif 2*dh <= nr < 3*dh and nc < 0:
                dir = RIGHT
                nc = dw
                nr = 3*dh-1-nr#(dh - 1) - (nr - 2*dh)
            # 1 -> 5
            elif 3*dh <= nr < h and nc < 0:
                dir = DOWN
                nc = (nr - 3*dh) + dw
                nr = 0
        elif dir == UP:
            # 2 -> 4
            if 0 <= nc < dw and nr < 2*dh:
                dir = RIGHT
                nr = nc + dh
                nc = dw
            # 5 -> 1
            elif dw <= nc < 2*dw and nr < 0:
                dir = RIGHT
                nr = nc - dw + 3*dh
                nc = 0
            # 6 -> 1
            elif 2*dw <= nc < w and nr < 0:
                dir = UP
                nc = nc - 2*dw
                nr = h - 1
        else:
            assert dir == DOWN
            # 1 -> 6
            if 0 <= nc < dw and nr >= h:
                dir = DOWN
                nc += 2*dw
                nr = 0
            # 3 -> 1
            elif dw <= nc < 2*dw and nr >= 3*dh:
                dir = LEFT
                nr = 3*dh + nc - dw
                nc = dw-1
                
            # 6 -> 4
            elif 2*dw <= nc < w and nr >= dh:
                dir = LEFT
                nr = dh + (nc-2*dw) #(nr - 2*dh) + dw
                nc = 2*dw - 1                
        return nr, nc, dir

    ########################################
    # Tests for wrapping
    ########################################

    # # Verify all squares interior map to the same, if they aren't spaces
    # for big_r in range(w//50):
    #     for big_c in range(w//50):
    #         for r in range(big_r * 50 + 1,(big_r+1)*50-1):
    #             for c in range(big_c*50 + 1, (big_c+1)*50-1):
    #                 if board[r][c] == " ":
    #                     continue
    #                 nr, nc, dir = cube_wrap(r,c,LEFT)
    #                 assert r == nr
    #                 assert c == nc
    #                 assert dir == LEFT
    #                 nr, nc, dir = cube_wrap(r,c,RIGHT)
    #                 assert r == nr
    #                 assert c == nc
    #                 assert dir == RIGHT
    #                 nr, nc, dir = cube_wrap(r,c,UP)
    #                 assert r == nr
    #                 assert c == nc
    #                 assert dir == UP
    #                 nr, nc, dir = cube_wrap(r,c,DOWN)
    #                 assert r == nr
    #                 assert c == nc
    #                 assert dir == DOWN

    # # check wrapping from 6
    # # UP
    # for c in range(50*2,w):
    #     nr, nc, dir = cube_wrap(-1, c, UP)
    #     assert dir == UP
    #     assert nc == c - 50*2
    #     assert nr == h - 1
    # assert cube_wrap(-1, 2*50, UP) == (h-1, 0, UP)            
    # assert cube_wrap(-1, 2*50+ 4, UP) == (h-1, 4, UP)            
    # assert cube_wrap(-1, 3*50-1, UP) == (h-1, 49, UP)            
    # # RIGHT
    # for r in range(50):
    #     nr, nc, dir = cube_wrap(r, w+1, RIGHT)
    #     assert dir == LEFT
    #     assert nc == 50*2 - 1
    #     assert nr == 3*50-1-r
    # assert cube_wrap(0, w+1, RIGHT) == (3*50-1,50*2-1, LEFT)        
    # assert cube_wrap(3, w+1, RIGHT) == (3*50-1-3,50*2-1, LEFT)
    # assert cube_wrap(49, w+1, RIGHT) == (2*50,50*2-1, LEFT)        
    # # DOWN
    # for c in range(50*2,w):
    #     nr, nc, dir = cube_wrap(50, c, DOWN)
    #     assert dir == LEFT
    #     assert nc == 50*2 - 1
    #     assert nr == 50 + (c - 50*2)
    # assert cube_wrap(h, 2*50, DOWN) == (2*50-50, 2*50-1, LEFT)            
    # assert cube_wrap(h, 2*50+ 4, DOWN) == (2*50-50+4, 2*50-1, LEFT)            
    # assert cube_wrap(h, 3*50-1, DOWN) == (3*50-1-50, 2*50-1, LEFT)      

    # # check wrapping from 1
    # # LEFT
    # for r in range(3*50,h):
    #     nr, nc, dir = cube_wrap(r, -1, LEFT)
    #     assert dir == DOWN
    #     assert nc == r - 3*50 + 50
    #     assert nr == 0
    # assert cube_wrap(50*3, -1, LEFT) == (0, 50, DOWN)            
    # assert cube_wrap(50*3+4, -1, LEFT) == (0, 54, DOWN)            
    # assert cube_wrap(h-1, -1, LEFT) == (0, 99, DOWN)            
    # # RIGHT
    # for r in range(3*50,h):
    #     nr, nc, dir = cube_wrap(r, 51, RIGHT)
    #     assert dir == UP
    #     assert nc == 50+(r-3*50)
    #     assert nr == 3*50-1
    # # assert cube_wrap(0, w+1, RIGHT) == (3*50-1,50*2-1, UP)        
    # # assert cube_wrap(3, w+1, RIGHT) == (3*50-1-3,50*2-1, UP)
    # # assert cube_wrap(49, w+1, RIGHT) == (2*50,50*2-1, UP)        
    # # DOWN
    # for c in range(50):
    #     nr, nc, dir = cube_wrap(h+1, c, DOWN)
    #     assert dir == DOWN
    #     assert nc == c + 50*2
    #     assert nr == 0

    # # check wrapping from 3
    # # RIGHT
    # for r in range(2*50,3*50):
    #     nr, nc, dir = cube_wrap(r, 100, RIGHT)
    #     assert dir == LEFT
    #     assert nc == w-1
    #     assert nr == 3*50-1-r
    # # DOWN
    # for c in range(50,2*50):
    #     nr, nc, dir = cube_wrap(150, c, DOWN)
    #     assert dir == LEFT
    #     assert nc == 50-1
    #     assert nr == 3*50 + c-50
    # assert cube_wrap(150, 50, DOWN) == (3*50, 49, LEFT)            
    # assert cube_wrap(150, 50+4, DOWN) == (3*50+4, 49, LEFT)            
    # assert cube_wrap(150, 99, DOWN) == (h-1, 49, LEFT)    

    # # check wrapping from 2
    # # LEFT
    # for r in range(2*50,3*50):
    #     nr, nc, dir = cube_wrap(r, -1, LEFT)
    #     assert dir == RIGHT
    #     assert nc == 50
    #     assert nr == 3*50-1-r #(50-1) - (r - 2*50)
    # assert cube_wrap(100, -1, LEFT) == (49,50, RIGHT)        
    # assert cube_wrap(103, -1, LEFT) == (46,50, RIGHT)
    # assert cube_wrap(149, -1, LEFT) == (0,50, RIGHT)        
    # # UP
    # for c in range(50):
    #     nr, nc, dir = cube_wrap(99, c, UP)
    #     assert dir == RIGHT
    #     assert nc == 50
    #     assert nr == 50+c

    # # check wrapping from 4
    # # LEFT
    # for r in range(50,2*50):
    #     nr, nc, dir = cube_wrap(r, 49, LEFT)
    #     assert dir == DOWN
    #     assert nc == r - 50
    #     assert nr == 100
    # # RIGHT
    # for r in range(50,2*50):
    #     nr, nc, dir = cube_wrap(r, 100, RIGHT)
    #     assert dir == UP
    #     assert nc == r + 50
    #     assert nr == 49

    # # check wrapping from 5
    # # LEFT
    # for r in range(50):
    #     nr, nc, dir = cube_wrap(r, 49, LEFT)
    #     assert dir == RIGHT
    #     assert nc == 0
    #     assert nr == 3*50 - 1-r

    # #UP
    # for c in range(50,50*2):
    #     nr, nc, dir = cube_wrap(-1, c, UP)
    #     assert dir == RIGHT
    #     assert nc == 0
    #     assert nr == c + 100       

    c,r = start
    c, r, facing = sim(c, r, board, moves, cube_wrap)
    print("Part 2 =", 1000*(r+1)+4*(c+1)+facing)


# 195146 too high
# 143302 too high
# 125403 nope
# 40499
#  36573 too low
#  26502 too low
# 130068 yes..