import heapq

DIRS = [(1,0),(-1,0),(0,1),(0,-1)]

def get_reachable(board, cur):
    w = len(board[0])
    h = len(board)

    reachable = []
    for dx,dy in DIRS:
        nx = cur[0] + dx
        ny = cur[1] + dy
        if 0 <= ny < h and 0 <= nx < w:
            if board[ny][nx]-board[cur[1]][cur[0]] <= 1:
                reachable.append((nx,ny))
    return reachable

def bfs(board, start, end):
    w = len(board[0])
    h = len(board)

    visited = set()
    nodes = [(0, *start)]

    while nodes:
        path_len, x, y = nodes.pop(0)

        if (x,y) in visited:
            continue
        visited.add((x,y))

        for r in get_reachable(board, (x,y)):
            nx,ny = r
            if (nx,ny) == end:
                return path_len + 1
            nodes.append((path_len + 1, nx,ny))

    return 0

#with open("test.txt") as file:
with open("day12.txt") as file:
    data = [x.strip() for x in file.readlines()]

    board = []
    for line in data:
        board.append([ord(x) for x in line])

    W = len(board[0])
    H = len(board)
    start = (0,0)
    end = (0,0)
    for j in range(H):
        for i in range(W):
            if board[j][i] == ord("S"):
                start = (i,j)
                board[j][i] = ord("a")
            if board[j][i] == ord("E"):
                end = (i,j)
                board[j][i] = ord("z")

    print(start,end)
    print("Part 1 =", bfs(board, start, end))     

    # Brute force.. Find all the 'a's and check them.
    dists = []
    for j in range(H):
        for i in range(W):
            if board[j][i] == ord("a"):
                #print("checking",(i,j))
                path_length = bfs(board, (i,j), end)
                if path_length:
                    dists.append(path_length)
    print("Part 2 =", min(dists))