from collections import defaultdict

def move(buckets, q, src, dest):
    for i in range(q):
        buckets[dest].insert(0, buckets[src].pop(0))

def move_stack(buckets,q,src,dest):
    stack = []
    for i in range(q):
        stack.append(buckets[src].pop(0))

    while len(stack) > 0:
        buckets[dest].insert(0, stack.pop())

#with open("test.txt") as file:
with open("day5.txt") as file:
    data = file.readlines()

    parse_board = True
    buckets_part1 = defaultdict(list)
    buckets_part2 = defaultdict(list)
    for line in data:
        if parse_board:
            #print(line,len(line))
            i = 1
            cur = 0
            while cur < len(line):
                tok = line[cur:cur+3]
                if "[" in tok:
                    buckets_part1[i].append(tok[1])
                    buckets_part2[i].append(tok[1])
                cur += 4
                i += 1
            if not line.strip():
                parse_board = False
                continue
        else:
            parts = line.split(" ")
            q = int(parts[1])
            src = int(parts[3])
            dest = int(parts[5])
            
            move(buckets_part1,q,src,dest)
            move_stack(buckets_part2,q,src,dest)

    i=1
    p1 = ""
    p2 = ""
    while True:
        if i in buckets_part1:
            p1+=buckets_part1[i][0]
            p2+=buckets_part2[i][0]
            i+=1
        else:
            break

    print("Part 1 =", p1)    
    print("Part 2 =", p2)