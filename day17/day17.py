from collections import defaultdict

#with open("test.txt") as file:
with open("day17.txt") as file:
    data = file.read().strip()
    p1 = 0
    p2 = 0

pieces = [
    { 
        "data" : [list("####")],
        "w": 4,
        "h": 1
    },
    { 
        "data" : [list(".#."), list("###"), list(".#.")],
        "w": 3,
        "h": 3
    },    
    { 
        "data" : [list("..#"), list("..#"), list("###")],
        "w": 3,
        "h": 3
    },    
    {
        "data": ["#","#","#","#"],
        "w": 1,
        "h": 4
    },
    { 
        "data" : [list("##"), list("##")],
        "w": 2,
        "h": 2
    }
]

def print_board(board):
    assert len(board[0]) == 7
    for y in range(len(board)):
        for x in range(7):
            print(board[y][x], end="")
        print()

def stop(board, loc, piece):
    for y in range(piece["h"]):
        for x in range(piece["w"]):
            if piece["data"][y][x] == "#":
                board[loc[1] + y][loc[0]+x] = "#"

def collision(board, loc, piece):
    for y in range(piece["h"]):
        for x in range(piece["w"]):
            if piece["data"][y][x] == "#":
                if loc[1]+y >= len(board) or loc[0]+x >= 7:
                    return True
                if board[loc[1] + y][loc[0]+x] != ".":
                    return True
    return False

board = [["-"] * 7]
for _ in range(pieces[0]["h"] + 3):
    board.insert(0, ["."]*7)

wind_i = 0
piece_i = 0
rocks_stopped = 0
cur = (2,0)
moves_per_piece = defaultdict(list)
state = {}
cycles = []
rocks_left = 1000000000000
found_cycle = False
cycle_height = 0
while rocks_left:
    next_piece = pieces[piece_i]
    
    # First move L/R
    ch = data[wind_i]
    if ch == "<":
        if cur[0] - 1 >= 0 and not collision(board, (cur[0]-1, cur[1]), next_piece):
            cur = (cur[0]-1, cur[1])
    elif ch == ">":
        if cur[0] + next_piece["w"] < 8 and not collision(board, (cur[0]+1, cur[1]), next_piece):
            cur = (cur[0]+1, cur[1])
    else:
        assert False, ch

    # Now try down
    if collision(board, (cur[0], cur[1] + 1), next_piece):
        stop(board, cur, next_piece)
        
        rocks_stopped += 1
        rocks_left -= 1

        # if rocks_stopped % 1000 == 0:
        #     print("rocks:", rocks_stopped)

        y = len(board)-1 # skip base
        while y >= 0 and board[y] != ["."]*7:
            y -= 1

        key = (piece_i, wind_i)
        piece_i += 1
        piece_i = piece_i % len(pieces)

        if rocks_stopped == 2022:
            print("Part 1 =", len(board)-2-y)
        elif rocks_stopped >= 2022 and not found_cycle and key in state:
            found_cycle = True
            print("cycle", piece_i-1, wind_i, rocks_stopped, y, state[key])
            #print_board(board)

            # Found the cycle, compute how many rocks we drop in a cycle as well as
            # how tall the tower increases each cycle

            rocks_in_cycle = rocks_stopped - state[key][0]
            height_per_cycle = len(board)-2-y - state[key][1]

            # Start by gathering the current height + all of the height we will generating with all of
            # the cycles executing
            p2 = len(board)-2-y + (rocks_left // rocks_in_cycle) * height_per_cycle

            # Make sure to correcly update the the pieces by the number of rocks drops
            piece_i += ((rocks_left // rocks_in_cycle) * rocks_in_cycle)
            piece_i = piece_i % len(pieces)

            # Compute left over rocks not covered by cycles and update the tracking
            rocks_left %= rocks_in_cycle
            rocks_stopped += (rocks_left // rocks_in_cycle) * rocks_in_cycle
            cycle_height = len(board)-2-y

        state[key] = (rocks_stopped, len(board)-2-y)

        empty_lines = 0
        while board[empty_lines] == ["."]*7:
            empty_lines += 1
        for _ in range(empty_lines,3+pieces[piece_i]["h"]):
            board.insert(0, ["."]*7)
        if empty_lines >= 3+pieces[piece_i]["h"]:
            while empty_lines > 3+pieces[piece_i]["h"]:
                board.pop(0)
                empty_lines -= 1
        cur = (2,0)
    else:
        cur = (cur[0], cur[1] + 1)
    wind_i = (wind_i + 1) % len(data)

#print_board(board)
y = len(board)-1 # skip base
while y >= 0 and board[y] != ["."]*7:
        y -= 1
# 3128
# 3127 - someone else's input
# 3129 
# 3220

print("Part 2 =", p2 + (len(board)-2-y) - cycle_height)


# Tried 1558501440110
# tried 1558501437179+2930+4 = 1558501440113, too low
# tried 1558501440932, too low
# tried 1559654178680
# tried 1564265129668
1565517241382