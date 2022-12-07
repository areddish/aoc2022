from collections import defaultdict

def cwd_to_full_path(cwd):
    if not cwd:
        return "/"
    
    str = ""
    for dir in cwd:
        str += "/" + dir
    return str

TOTAL_DISK_SIZE = 70000000
NEEDED = 30000000

#with open("test.txt") as file:
with open("day7.txt") as file:
    data = [x.strip() for x in file.readlines()]
    p1 = 0
    p2 = 0
    cwd = []
    files = defaultdict(list)

    for line in data:
        cmds = line.split(" ")
        if cmds[0] == "$":
            if cmds[1] == "cd":
                if cmds[2] == "/":
                    cwd = []
                elif cmds[2] == "..":
                    cwd.pop()
                else:
                    cwd.append(cmds[2])
                #print(cwd)
            else:
                assert cmds[1] == "ls"
        else:
            if cmds[0] == "dir":
                print("Found dir", cmds[1])
            else:
                size = int(cmds[0])
                full_path = cwd_to_full_path(cwd)
                #print("found file", size, cmds[1], full_path)                
                files[full_path].append((size, cmds[1]))
            
    dir_sizes = {"/": 0}
    for dir in files:
        dir_size = sum([x[0] for x in files[dir]])
        #print(dir, dir_size)
        dir_sizes[dir] = dir_sizes.get(dir, 0) + dir_size
        if dir != "/":
            dir_sizes["/"] += dir_size

        # recusively add
        n = dir[:dir.rindex("/")]
        while n:
            dir_sizes[n] = dir_sizes.get(n, 0) + dir_size
            n = n[:n.rindex("/")]

    for x in dir_sizes:
        if dir_sizes[x] <= 100000:
            p1 += dir_sizes[x]

    print("In use: ", dir_sizes["/"], "Free: ", TOTAL_DISK_SIZE-dir_sizes["/"])
    print("Needed: ", NEEDED - (TOTAL_DISK_SIZE-dir_sizes["/"]))

    l = sorted([(x, dir_sizes[x]) for x in dir_sizes], key=lambda v:v[1])
    p2 = l[0]
    for i in range(1,len(l)):
        if l[i][1] >= NEEDED - (TOTAL_DISK_SIZE-dir_sizes["/"]):
            p2 = l[i][1]
            break

    print("Part 1 =", p1)    
    print("Part 2 =", p2)