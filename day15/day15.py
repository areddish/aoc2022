import math

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

    sensors = {}
    beacons = {}
    
    for line in data:
        parts = line.split(" ")
        sx,sy = parse(parts[2]), parse(parts[3])
        bx,by = parse(parts[8]), parse(parts[9])
        sensors[(sx,sy)] = manhattan_dist((sx,sy), (bx,by))
        beacons[(bx,by)] = 1
        print(sx,sy,bx,by)

    # y = 10
    y = 2000000
    locs = []
    for b in beacons:
        if b[1] == y:
            locs.append(b)

    start_x = min([l[0] for l in locs])

    # go left until not in scanner:
    cur = (start_x-1, y)
    stop = False
    while not stop:
        stop = True
        for s in sensors:
            radius = sensors[s]
            if manhattan_dist(cur, s) <= radius:
                stop = False
                p1 += 1
                break
        cur = (cur[0]-1, y)
    # print(p1)

    # go right until not in scanner
    cur = (start_x+1, y)
    stop = False
    while not stop:
        stop = True
        for s in sensors:
            radius = sensors[s]
            if manhattan_dist(cur, s) <= radius:
                stop = False
                assert cur not in beacons
                p1 += 1
                break
        cur = (cur[0]+1, y)

    print("Part 1 =", p1)