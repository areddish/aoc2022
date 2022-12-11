from copy import deepcopy

def build_op(str):
    parts = str.split(" ")

    if parts[5] == "old":
        if parts[4] == "*":
            return lambda x: x * x
        elif parts[4] == "+":
            return lambda x: x + x
    else:
        val = int(parts[5])
        if parts[4] == "*":
            return lambda x: x * val
        elif parts[4] == "+":
            return lambda x: x + val

    assert False

def simulate(monkeys, worry_reducer, num_rounds):   
    round = 0
    while round < num_rounds:
        for monkey_index in range(len(monkeys)):
            # each turn
            current_monkey = monkeys[monkey_index]
            if not current_monkey["items"]:
                continue

            for worry_level in current_monkey["items"]:
                # inspect
                worry_level = worry_reducer(current_monkey["op"](worry_level))
                if worry_level % current_monkey["test_divisor"] == 0:
                    assert current_monkey["true"] != monkey_index
                    monkeys[current_monkey["true"]]["items"].append(worry_level)
                else:
                    assert current_monkey["false"] != monkey_index
                    monkeys[current_monkey["false"]]["items"].append(worry_level)
            # ASSUMPTION: monkeys never throw to themselves, asserts above will fire if so. Otherwise
            # need to copy this list first and clear it.
            current_monkey["inspections"] += len(current_monkey["items"])
            current_monkey["items"] = []                    
        round += 1   

        # if round in [1, 20, 50, 100] + list(range(1000,10001,1000))
        #     print("Round ", round)
        #     for i in range(len(monkeys)):
        #         print(f"Monkey {i} inspected {monkeys[i]['inspections']} items")

    return monkeys

def get_score(monkeys):
    a = 0
    b = 0
    for i in range(0,len(monkeys)):
        if monkeys[i]["inspections"] > a:
            b = a
            a = monkeys[i]["inspections"]
        elif monkeys[i]["inspections"] > b:
            b = monkeys[i]["inspections"]
    return a*b

#with open("test.txt") as file:
with open("day11.txt") as file:
    data = [x.strip() for x in file.readlines()]

    monkeys = []
    monkey_i = 0
    for i in range(0,len(data),7):
        #monkey_i = int(data[i].split(" ")[1].split(":")[0])
        #print("parsing monkey", monkey_i)
        monkeys.append({
            #"name": "monkey "+ str(monkey_i),
            "items": [int(x.strip()) for x in data[i+1].split("items:")[1].split(",")],
            "op": build_op(data[i+2]),
            "test_divisor": int(data[i+3].split("by")[1]),
            "true":  int(data[i+4].split("throw to monkey")[1]),
            "false": int(data[i+5].split("throw to monkey")[1]),
            "inspections": 0
        })

    # compute a scaling divisor which is the product of all of the test conditions.
    divisor = 1
    for monkey in monkeys:
        divisor *= monkey["test_divisor"]

    p1 = get_score(simulate(deepcopy(monkeys), lambda x: x // 3, 20))
    p2 = get_score(simulate(monkeys, lambda x: x % divisor, 10000))

    print("Part 1 =", p1)    
    print("Part 2 =", p2)