def manhattan_dist(p1,p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def parse(tok):
    if tok[-1] in [",",":"]:
        tok = tok [:-1]
    return int(tok.split("=")[1])

#with open("test.txt") as file:
with open("day15.txt") as file:
    data = [x.strip() for x in file.readlines()]
    p1 = 0
    p2 = 0

    sensors = {}
    
    for line in data:
        parts = line.split(" ")
        sx,sy = parse(parts[2]), parse(parts[3])
        bx,by = parse(parts[8]), parse(parts[9])
        sensors[(sx,sy)] = manhattan_dist((sx,sy), (bx,by))
        # print(sx,sy,bx,by)

    def scanline(start_x,stop_x,start_y,stop_y,sensors):
        ans = 0
        y = start_y
        while y < stop_y+1:
            x = start_x
            while x < stop_x+1:
                unseen = True
                for s in sensors:
                    radius = sensors[s]
                    if manhattan_dist((x,y), s) <= radius:
                        # x + y = radius is the diagonal
                        # x = radius - y (from the center, need to offset then add one to account for center pt)
                        ans += s[0]-x + (radius - abs(s[1] - y)) + 1
                        x = s[0] + (radius - abs(s[1] - y)) + 1
                        unseen = False
                        break
                if unseen:
                    print("Part 2 = ",y+x*4000000)
                    exit(1)
            y += 1
        return ans

    min_x = min([s[0]-sensors[s] for s in sensors])
    max_x = max([s[0]+sensors[s] for s in sensors])
    #print("Part 2 =", scanline(0,20,0,20,sensors, part=2))
    print("Part 2 =", scanline(0,4000000,0,4000000,sensors))