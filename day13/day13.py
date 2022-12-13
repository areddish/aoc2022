def compare_items(left, right):
    if isinstance(left, list) and isinstance(right, list):
        return compare_packets(left, right)
    elif isinstance(left, int) and isinstance(right, int):
        return left < right
    else:
        if isinstance(left, list):
            return compare_packets(left, [right])
        else:
            assert isinstance(right, list)
            return compare_packets([left], right)
            
    assert False

def compare_packets(p1, p2, d=0):
    for i in range(len(p1)):
        if i >= len(p2):
            return False
        if p1[i] == p2[i]:
            continue
        return compare_items(p1[i], p2[i])
    return True

#with open("test.txt") as file:
with open("day13.txt") as file:
    data = file.read().split("\n\n")
    p1 = 0
    p2 = 0

    unordered_packets = []
    index = 1
    for index, line in enumerate(data):
        packet1, packet2 = line.split("\n")
        packet1 = eval(packet1)
        packet2 = eval(packet2)
        unordered_packets.append(packet1)
        unordered_packets.append(packet2)
        if compare_packets(packet1, packet2):
            p1 += index + 1
    print("Part 1 =", p1)

    # add in the divider packets
    DIVIDER_1 = [[2]]
    DIVIDER_2 = [[6]]
    unordered_packets.append(DIVIDER_1)
    unordered_packets.append(DIVIDER_2)

    ordered_packets = [unordered_packets.pop()]
    for packet in unordered_packets:
        # Try to place as far down as possible
        index = 0
        while index < len(ordered_packets) and compare_packets(ordered_packets[index], packet):
            index += 1
        ordered_packets.insert(index, packet)

    # Find divider packets and multiply
    divider_1_index = 0
    divider_2_index = 0
    for index,packet in enumerate(ordered_packets):
        if packet == DIVIDER_1:
            divider_1_index = index + 1 
        elif packet == DIVIDER_2:
            divider_2_index = index + 1
    print("Part 2 =", divider_1_index * divider_2_index)