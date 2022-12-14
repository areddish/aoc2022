import imageio
from PIL import Image, ImageDraw
import copy

MOVES = [ (0,1), (-1, 1), (1 ,1)]

COLORS = {
    "o": "brown",
    "#": "green",
    ".": "lightblue"
}

def render_board_to_image(board,xmin,ymin,xmax,ymax,multiplier=12):
    image = Image.new("RGB", ((xmax-xmin)*multiplier, (ymax-ymin)*multiplier))
    img = ImageDraw.Draw(image)
    for j in range(ymin-1,ymax+1):
        for i in range(xmin-1,xmax+1):
            img_x = (i-xmin) * multiplier
            img_y = (j-ymin) * multiplier
            color = COLORS[board.get((i,j), ".")]
            img.rectangle([img_x,img_y,img_x+multiplier, img_y+multiplier], fill=color)
    image.show()
    image.save("test"+str(xmin)+".png")
    return img

def draw_board(board,xmin,ymin,xmax,ymax):
    for j in range(ymin-1,ymax+1):
        for i in range(xmin-1,xmax+1):
            print(board.get((i,j), "."), end="")
        print()

def draw_horiz(board, x1, x2, y):
    if x1 > x2:
        x1,x2 = x2,x1

    for x in range(x1,x2+1):
        board[(x,y)] = "#"

def draw_vert(board, x, y1, y2):
    if y1 > y2:
        y1,y2 = y2,y1

    for y in range(y1,y2+1):
        board[(x,y)] = "#"

#with open("test.txt") as file:
with open("day14.txt") as file:
    data = [x.strip() for x in file.readlines()]
    p1 = 0
    p2 = 0

    xmin = 1e6
    ymin = 1e6
    xmax = 0
    ymax = 0
    board = {}
    for line in data:
        lines = []
        for pairs in line.split("->"):
            coords = pairs.strip().split(",")
            x = int(coords[0].strip())
            y = int(coords[1].strip())
            xmin = min(xmin, x)
            xmax = max(xmax, x)
            ymin = min(ymin, y)
            ymax = max(ymax, y)
            lines.append((x,y))
        print(lines)

        cur = lines.pop()
        while lines:
            next = lines.pop()
            if cur[1] == next[1]:
                draw_horiz(board, cur[0], next[0], cur[1])
            else:
                assert cur[0] == next[0]
                draw_vert(board, cur[0], cur[1], next[1])
            cur = next

    #render_board_to_image(board, xmin, ymin, xmax, ymax)

    def drop_sand(board, sand_pt, void_y):
        cur = sand_pt
        moved = True
        while moved:
            moved = False
            for dx,dy in MOVES:                
                x,y = cur
                nx = x + dx
                ny = y + dy
                if (void_y >= 0 and ny > void_y):
                    return False
                if (nx,ny) not in board:
                    moved = True
                    cur = (nx,ny)
                    break
        board[cur] = "o"        
        #draw_board(board, xmin, ymin, xmax, ymax+3)        
        if cur == (500,0):
            return False
        return True

    p2_board = board.copy()
    sand_entry = (500,0)
    while drop_sand(board, sand_entry, ymax):
        p1 += 1
    print("Part 1 =", p1) 
    render_board_to_image(board, xmin, 0, xmax, ymax)

    xmin = 336
    xmax= 664
    # Could probably compute the xmin/max via pythagorean theorem: a^2+b^2=c^2, but doubling works ;)
    # draw_horiz(p2_board,-xmin*2,2*xmax,ymax+2)
    draw_horiz(p2_board,xmin,xmax,ymax+2)
    while drop_sand(p2_board, sand_entry, -1):
        p2 += 1

    # xmin = 1e6
    # xmax = 0
    # for k in p2_board:
    #     if p2_board[k] == "o":
    #         xmin = min(xmin,k[0])
    #         xmax = max(xmax,k[0])
    # print(xmin,xmax)
    render_board_to_image(p2_board, xmin, 0, xmax,2+ ymax)
    # +1 because we don't count the last sand but it was placed.
    print("Part 2 =", p2+1)