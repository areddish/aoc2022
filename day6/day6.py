tests = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz",  5),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11)
]

def find_marker(message, marker_length=4):
    start = 0
    i = marker_length
    while True:
        if len(set(message[start:i])) == marker_length:
            return i
        start += 1
        i += 1


# Tests to validate cases
for t in tests:
    assert find_marker(t[0]) == t[1], t[0]

with open("day6.txt") as file:
    day6_data = [x.strip() for x in file.readlines()][0]

    print("Part 1 = ", find_marker(day6_data, 4))
    print("Part 2 = ", find_marker(day6_data, 14))

