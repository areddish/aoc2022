#with open("test.txt") as file:
with open("day4.txt") as file:
    data = [x.strip() for x in file.readlines()]
    p1 = 0
    p2 = 0

    for line in data:
        pairs = line.split(",")
        seg1 = [int(x) for x in pairs[0].split('-')]
        seg2 = [int(x) for x in pairs[1].split('-')]

        # full containment
        if seg1[0]<=seg2[0]<=seg1[1] and seg1[0]<=seg2[1]<=seg1[1]:
            p1 += 1
        elif seg2[0]<=seg1[0]<=seg2[1] and seg2[0]<=seg1[1]<=seg2[1]:
            p1 += 1

        # partial/any containment
        if seg1[0]<=seg2[0]<=seg1[1] or seg1[0]<=seg2[1]<=seg1[1] or seg2[0]<=seg1[0]<=seg2[1] or seg2[0]<=seg1[1]<=seg2[1]:
            p2 += 1

    print("Part 1 =", p1)    
    print("Part 2 =", p2)