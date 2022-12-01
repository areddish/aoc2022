from collections import defaultdict

with open("day1.txt") as file:

    elves = defaultdict(list)
    index = 1
    for line in file.readlines():
        line = line.strip()
        if not line:
            index += 1
            continue

        elves[index].append(int(line.strip()))

    # part 1
    # largest = -1
    # for x in elves:
    #     if sum(elves[x]) > largest:
    #         largest = sum(elves[x])

    maxes = [0,0,0]
    for x in elves:
        s = sum(elves[x])
        if s > maxes[0]:
            maxes = [s, maxes[0], maxes[1]]
        elif s > maxes[1]:
            maxes = [maxes[0], s, maxes[1]]
        elif s > maxes[2]:
            maxes[2] = s

    print("Part 1 =", maxes[0])
    print("Part 2 =", sum(maxes))