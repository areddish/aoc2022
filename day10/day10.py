def is_lit(cycle, x):
    pos = cycle % 40
    return x-1 <= pos <= x+1

#with open("test.txt") as file:
with open("day10.txt") as file:
    data = [x.strip() for x in file.readlines()]

    X = 1
    cycle = 0
    results = []
    crt = ["."]*40*6

    for instr in data:
        for inc in range(1 if instr == "noop" else 2):
            cycle += 1
            if inc == 1:
                X += int(instr.split(" ")[1])

            # Part 1 - store signal strength
            if cycle in [20,60,100,140,180,220]:
                results.append(cycle * X)

            # Part 2 - render crt
            if cycle < len(crt):
                crt[cycle] = "#" if is_lit(cycle, X) else "."

    # render the crt
    for j in range(6):
        for i in range(40):
            print(crt[j*40 + i], end="")
        print()

    print("Part 1 =", sum(results))    
    print("Part 2 = read above")