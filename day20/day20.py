class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def __str__(self) -> str:
        return str(self.val)

    def create_doubly_linked_list(data):
        for i in range(1,len(data)-1):
            data[i].left = data[i-1]
            data[i].right = data[i+1]

        data[0].left = data[-1]
        data[0].right = data[1]
        data[-1].left = data[-2]
        data[-1].right = data[0]
        return data

def print_list(head):
    print(str(head), end=",")
    cur = head.right
    while cur != head:
        print(str(cur), end=",")
        cur = cur.right
    print()

DECRYPTION_KEY = 811589153

#with open("test.txt") as file:
with open("day20.txt") as file:
    nums = [int(x.strip()) for x in file.readlines()]
    data_p1 = [Node(x) for x in nums]
    data_p2 = [Node(x*DECRYPTION_KEY) for x in nums]
    p1 = 0
    p2 = 0

    # Create a doubly linked list from the data in the list. We keep two arrays because
    # data maintains both a reference inside the doubly linked list to the node we want move
    # as well as the original order to move in.
    data_p1 = Node.create_doubly_linked_list(data_p1)
    data_p2 = Node.create_doubly_linked_list(data_p2)

    def mix(data, times=1):
        for _ in range(times):
            for node_to_move in data:
                # Nothing to do if 0
                if node_to_move.val == 0:                    
                    continue

                # # For printing conveninece
                # if head == node_to_move:
                #     head = node_to_move.right

                #print(node_to_move.val, ": (",node_to_move,")", end="")
                #print_list(head)

                # remove node_to_move
                node_to_move.left.right = node_to_move.right
                node_to_move.right.left = node_to_move.left
                #print_list(head)

                offset = -1 if node_to_move.val < 0 else 1
                # Start to the left or right of the node we removed, and subtract off one from the # of times we'll go left/right.
                # also MOD the total distance by the # of node - 1 to reduce the number of cycles we perform for part 2.
                # The offset of +1 if going left is because the insertion code below always adds it after the node_dest
                node_dest = node_to_move.left if node_to_move.val < 0 else node_to_move.right
                for _ in range((abs(node_to_move.val)-1+(1 if offset == -1 else 0))%(len(data)-1)):
                    if offset == -1:
                        node_dest = node_dest.left
                    else:                
                        node_dest = node_dest.right
                # re-insert
                node_to_move.right = node_dest.right
                node_to_move.left = node_dest
                node_dest.right.left = node_to_move
                node_dest.right = node_to_move 
                #print_list(head)
    #    print_list(head)
        return data

    def score(data):
        ans = 0
        zero = next(filter(lambda x: x.val == 0, data))
        i = 0
        while i < 3001:
            if i == 1000 or i == 2000 or i == 3000:
                #print(zero.val)
                ans += zero.val
            zero = zero.right
            i += 1
        return ans
    
    print("Part 1 =", score(mix(data_p1, 1)))    
    print("Part 2 =", score(mix(data_p2, 10)))

#12433 too low!
#12574 to low!

# p2
# 1623178306 too low (yeah, oops I was submitting the test answer :( )
# 1623178306
# 1623178306
# 4869534918 too low
# Ans: 4789999181006