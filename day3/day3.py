# Original implementation using bit flags to mark commonality, until I realized 
# I was building set difference and could just use set & set...
#
# def common(s1,s2,s3=""):
#     x = {ch:1 for ch in s1}
#     for ch in s2:
#         if ch in x:
#             x[ch] = x[ch] | 0x2

#     if not s3:
#         for ch in x:
#             if x[ch] == 3:
#                 return ch

#     for ch in s3:
#         if ch in x:
#             x[ch] = x[ch] | 0x4

#     for ch in x:
#             if x[ch] == 7: # 0x1|0x2|0x4
#                 return ch

#     return None

# ord('a') - 96 = 1 to map into 1...26
# ord('A') - 64 = 1 + 26 to map into range 27...52
def score(ch):
    orig = ch
    if ch.lower() == orig:
        return ord(orig) - 96

    return ord(orig)-64 + 26

#with open("test.txt") as file:
with open("day3.txt") as file:
    data = [x.strip() for x in file.readlines()]
    p1 = 0
    p2 = 0

    for i in range(len(data)):        
        n = len(data[i])//2
        p1 += score(list(set(data[i][:n]) & set(data[i][n:]))[0]) # common(data[i][:n], data[i][n:]))
        if i % 3 == 0:
            first = data[i]
            second = data[i+1]
            third = data[i+2]
            c = list(set(first) & set(second) & set(third))[0] # common(first,second,third)
            p2 += score(c)
    print("Part 1 =", p1)    
    print("Part 2 =", p2)