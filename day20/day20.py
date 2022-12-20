import copy

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def __str__(self) -> str:
        return str(self.val)

def index(i, offset, limit):
    if offset > 0:
        return (i + offset) % limit
    else:
        for i in range(offset, 0):
            i += offset
            if i < 0:
                i = limit-1
        return i

#with open("test.txt") as file:
with open("day20.txt") as file:
    nums = [int(x.strip()) for x in file.readlines()]
    data = [Node(x) for x in nums]

    assert len(data) == len(nums)   
    p1 = 0
    p2 = 0

    # create list
    for i in range(1,len(data)-1):
        data[i].left = data[i-1]
        data[i].right = data[i+1]

    data[0].left = data[-1]
    data[0].right = data[1]
    data[-1].left = data[-2]
    data[-1].right = data[0]

    head = data[0]
    def print_list(head):
        print(str(head), end=",")
        cur = head.right
        while cur != head:
            print(str(cur), end=",")
            cur = cur.right
        print()

    # def find_list(head, n):
    #     cur = head
    #     while cur.val != n:
    #         cur = cur.right
    #     return cur

    for node_to_move in data:
        if node_to_move.val == 0:
            print("not moving zero")
            continue
        #node_to_move = find_list(head, n)
        if head == node_to_move:
            head = node_to_move.right

        #print(node_to_move.val, ": (",node_to_move,")", end="")
        #print_list(head)
        
        #find node to insert
        offset = -1 if node_to_move.val < 0 else 1
        node_dest = node_to_move
        for _ in range(abs(node_to_move.val)+(1 if offset == -1 else 0)):
            if offset == -1:
                # skip the node still in the list
                if node_dest.left == node_to_move:
                    node_dest = node_dest.left
                node_dest = node_dest.left
            else:                
                # skip the node still in the list
                if node_dest.right == node_to_move:
                    node_dest = node_dest.right
                node_dest = node_dest.right
        
        # remove node_to_move
        node_to_move.left.right = node_to_move.right
        node_to_move.right.left = node_to_move.left
        #print_list(head)
        
        # re-insert
        node_to_move.right = node_dest.right
        node_to_move.left = node_dest
        node_dest.right.left = node_to_move
        node_dest.right = node_to_move 
        #print_list(head)


        # n_index = answer.index(n)
        # dest_index = index(n_index, n, len(answer))

        # offset = 1 if n > 0 else -1
        # for i in range(abs(n)):
        #     next_index = index(n_index, offset, len(answer))
        #     temp = answer[n_index]
        #     answer[n_index] = answer[next_index]
        #     answer[next_index] = temp
        #     n_index = next_index
        # print(" => " , answer)
    print_list(head)

    zero = next(filter(lambda x: x.val == 0, data))

    i = 0
    while i < 3001:
        if i == 1000 or i == 2000 or i == 3000:
            print(zero.val)
            p1 += zero.val
        zero = zero.right
        i += 1
    
    # answer = [1, 2, -3, 4, 0, 3, -2]
    # print(answer)

    # zero_index = answer.index(0)    
    # print(answer[index(zero_index, 1000, len(answer))])
    # print(answer[index(zero_index, 2000, len(answer))])
    # print(answer[index(zero_index, 3000, len(answer))])
    print("Part 1 =", p1)    
    print("Part 2 =", p2)

#12433 too low!
#12574 to low!