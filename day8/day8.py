def is_visible(board, x, y, w , h):
    kernel = [(-1,0),(1,0),(0,1),(0,-1)]
    for j in range(max(w,h)):
        for i in range(len(kernel)):
            k = kernel[i]
            if not k:
                continue

            tx = x + k[0] * (j+1)
            ty = y + k[1] * (j+1)
            if 0 <= tx < w and 0 <= ty < h:
                if board[ty][tx] >= board[y][x]:
                    kernel[i] = None 
    return sum([1 if k else 0 for k in kernel]) > 0

def is_visible2(board, x, y, w, h):
    if x == 0 or y == 0 or x == w-1 or y == h-1:
        return True

    # from left
    tx = 0
    while tx < x:
        if board[y][tx] >= board[y][x]:
            break
        tx += 1
    if tx == x:
        return True

    # from right
    tx = w-1
    while tx > x:
        if board[y][tx] >= board[y][x]:
            break
        tx -=1
    if tx == x:
        return True
    # from top
    ty = 0
    while ty < y:
        if board[ty][x] >= board[y][x]:
            break
        ty += 1
    if ty == y:
        return True

    # from left
    ty = h - 1
    while ty > y:
        if board[ty][x] >= board[y][x]:
            break
        ty -= 1
    if ty == y:
        return True
    return False

def part2(board,x,y,w,h):
    # [ LEFT, RIGHT, DOWN, UP]
    kernel = [(-1,0),(1,0),(0,1),(0,-1)]
    trees_seen = [0, 0, 0, 0]
    blocked_view_direction = [False, False, False, False]
    for j in range(max(w,h)):
        for i in range(len(kernel)):
            k = kernel[i]
            if not k:
                continue
            tx = x + k[0] * (j+1)
            ty = y + k[1] * (j+1)
            if not blocked_view_direction[i] and 0 <= tx <= w-1 and 0 <= ty <= h-1:
                trees_seen[i] += 1
                if board[ty][tx] >= board[y][x]:
                    blocked_view_direction[i] = True
                    kernel[i] = None
    return trees_seen[0] * trees_seen[1] *  trees_seen[2] * trees_seen[3]

def is_visible(board, x, y, w, h):
    # SPECIAL CASE: Edges are visible by default
    if x == 0 or y == 0 or x == w-1 or y == h-1:
        return True

    kernel = [(-1,0),(1,0),(0,1),(0,-1)]
    radius = 1
    while radius < max(w,h):
        for i in range(len(kernel)):
            k = kernel[i]
            if not k:
                continue
            tx = x + k[0]*radius
            ty = y + k[1]*radius
            # if it's a valid point, see if we've reached the edge
            if 0 <= tx < w and 0 <= ty < h and board[ty][tx] < board[y][x]:
                if tx == 0 or ty == 0 or tx == w-1 or ty == h-1:
                    return True
            else:
                kernel[i] = None
        radius += 1
    return False

#with open("test.txt") as file:
with open("day8.txt") as file:
    board = [[int(x) for x in list(line.strip())] for line in file.readlines()]
    p1 = 0

    scores = []
    vis={}
    w = len(board[0])
    h = len(board)
    for y in range(h):
        for x in range(w):
            if is_visible(board, x, y, w, h):
                vis[(x,y)] = True
                p1 += 1
            scores.append(part2(board, x, y, w, h))

    for y in range(h):
        for x in range(w):
            print(board[y][x] if (x,y) not in vis else "*", end="")
        print()

    print("Part 1 =", p1)    
    print("Part 2 =", max(scores))