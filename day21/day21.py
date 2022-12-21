from collections import defaultdict

#with open("test.txt") as file:
with open("day21.txt") as file:
    monkeys = {}
    monkey_dependencies = defaultdict(list)
    monkey_eq = {}
    for line in file.readlines():
        line = line.strip()
        parts = line.split(": ")
        monkey_name = parts[0]
        eq = None
        for op in ["*","+","/","-"]:
            if op in parts[1]:
                eq = parts[1].split(" ")                
                #print(eq)
                monkey_dependencies[monkey_name].append(eq[0])
                monkey_dependencies[monkey_name].append(eq[2])
                if eq[1] == "*":
                    monkey_eq[monkey_name] = lambda x,y: x*y
                elif eq[1] == "+":
                    monkey_eq[monkey_name] = lambda x,y: x+y
                elif eq[1] == "-":
                    monkey_eq[monkey_name] = lambda x,y: x-y
                else:
                    assert eq[1] == "/", eq[1]
                    monkey_eq[monkey_name] = lambda x,y: x/y

        if not eq:
            monkeys[monkey_name] = int(parts[1])

def sim(monkeys, monkey_dependencies, monkey_eq):
    monkey_has_dependency = True
    while monkey_has_dependency:
        monkey_has_dependency = False
        for m_name in monkey_dependencies:
            # already processed?
            if m_name in monkeys:
                continue
            # see if we have 'heard' the dependent monkey's yell
            dependencies = monkey_dependencies[m_name]
            if dependencies[0] in monkeys and dependencies[1] in monkeys:
                # if so, just evaluate
                monkeys[m_name] = monkey_eq[m_name](monkeys[dependencies[0]], monkeys[dependencies[1]])
            else:
                # nope, stil need to keep doing eval passes
                monkey_has_dependency = True
    #print(monkeys)
    return monkeys
    
# Part 1
print("Part 1 =", int(sim(dict(monkeys), monkey_dependencies, monkey_eq)["root"]))

# Part 2
# 236694194201630.0==94625185243550.0
# Now just return a tuple of the values so we can compare easy. We do one sim to make sure we are returning
# the first value which will initially be greater, so the logic below works by increasing humn until we create
# a value below the other.
monkey_eq["root"] = lambda x,y: (x,y)
x, y = sim(dict(monkeys), monkey_dependencies, monkey_eq)["root"]
if x < y:
    monkey_eq["root"] = lambda x,y: (y,x)
    x,y = y,x

# Starting at the current value, find a begin and end that we can reasonably bisect to
# find the final value. 
n = monkeys["humn"]
n_prev = 0
while x > y:
    n_prev = n
    n *= 10
    monkeys_copy = dict(monkeys)
    monkeys_copy["humn"] = n
    x,y = sim(monkeys_copy, monkey_dependencies, monkey_eq)["root"]
    #print("Part 2 =", n, x,y)

# Now bisect/binary search using the range [n_prev ----- n_mid ----- n]
n_mid = 0
while x != y and n_prev < n:
    n_mid = (n+n_prev) // 2
    monkeys_copy = dict(monkeys)
    monkeys_copy["humn"] = n_mid
    x,y = sim(monkeys_copy, monkey_dependencies, monkey_eq)["root"]
    #print("Part 2 =", n_mid, x,y, x-y)
    if x < y:
        # Solution is in the left/smaller half
        n = n_mid
    else:
        # Solution is in the right/larger half
        n_prev = n_mid

print("Part 2 = ", n_mid)