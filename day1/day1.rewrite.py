from collections import defaultdict

with open("day1.txt") as file:

    elves = []
    cur_sum = 0
    for line in file.readlines():
        line = line.strip()
        if not line:
            elves.append(cur_sum)            
            cur_sum = 0
            continue

        cur_sum += int(line.strip())

    elves = list(sorted(elves, reverse=True))
    print("Part 1 = ", elves[0])
    print("Part 2 = ", sum(elves[:3]))