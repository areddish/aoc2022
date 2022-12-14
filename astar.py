data = """#######
#S# #E#
# ### #
#   # #
# # # #
# #   #
#######"""

grid = []
for line in data.split("\n"):
    grid.append(list(line))

def print_grid(grid, path=[]):
    W = len(grid[0])
    H = len(grid)

    for j in range(H):
        for i in range(W):
            print(grid[j][i] if (i,j) not in path else "*", end="")
        print()


print_grid(grid)

import heapq
from collections import defaultdict

DIRS_4 = [ (-1,0), (0,1), (1,0), (0,1)]
DIRS_8 = DIRS_4 + [ (1,1), (-1,-1), (-1,1), (1,-1)]

def neighbors(grid, loc, test_fn, dirs = DIRS_4):
    W = len(grid[0])
    H = len(grid)

    x,y = loc
        
    results = []
    for dy,dx in dirs:
        nx = x + dx
        ny = y + dy    
        if 0<=nx<W and 0<=ny<H and test_fn(grid, (nx,ny)):
            results.append((nx,ny))
    return results
def manhattan_distance(start,end):
    return (start[0]-end[0]) + abs(start[1]-end[1])

def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.append(current)
    return list(reversed(total_path))

def a_star(start, target, h, d, neighbors, test_fn):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    open_set = [start]

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    came_from = {}

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    goal_score = defaultdict(lambda: 1e10)
    goal_score[start] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how cheap a path could be from start to finish if it goes through n.
    f_score = defaultdict(int)
    f_score[start] = h(start)

    while open_set:
        # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
        current = heapq.heappop(open_set)
        if current == target:
            return reconstruct_path(came_from, current)

        # openSet.Remove(current)
        for neighbor in neighbors(grid, current, test_fn):
            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            tentative_gScore = goal_score[current] + d(current, neighbor)
            if tentative_gScore < goal_score[neighbor]:
                # This path to neighbor is better than any previous one. Record it!
                came_from[neighbor] = current
                goal_score[neighbor] = tentative_gScore
                f_score[neighbor] = tentative_gScore + h(neighbor)
                if neighbor not in open_set:
                    heapq.heappush(open_set, neighbor)

    # Open set is empty but goal was never reached
    return []


"""

# A* finds a path from start to goal.
# h is the heuristic function. h(n) estimates the cost to reach goal from node n.
function A_Star(start, g    oal, h)
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    openSet := {start}

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    cameFrom := an empty map

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    gScore := map with default value of Infinity
    gScore[start] := 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how cheap a path could be from start to finish if it goes through n.
    fScore := map with default value of Infinity
    fScore[start] := h(start)

    while openSet is not empty
        # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
        current := the node in openSet having the lowest fScore[] value
        if current = goal
            return reconstruct_path(cameFrom, current)

        openSet.Remove(current)
        for each neighbor of current
            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            tentative_gScore := gScore[current] + d(current, neighbor)
            if tentative_gScore < gScore[neighbor]
                # This path to neighbor is better than any previous one. Record it!
                cameFrom[neighbor] := current
                gScore[neighbor] := tentative_gScore
                fScore[neighbor] := tentative_gScore + h(neighbor)
                if neighbor not in openSet
                    openSet.add(neighbor)

    # Open set is empty but goal was never reached
    return failure
"""

path = a_star((1,1), (5,1), lambda x:0, manhattan_distance, neighbors, lambda grid,x: grid[x[1]][x[0]] != "#")
print(path)
print_grid(grid, path)
