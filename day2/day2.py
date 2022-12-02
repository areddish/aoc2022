score = {
    "A": 1, # Rock
    "X": 1,
    "B": 2, # Paper
    "Y": 2,
    "A": 3, # Scissor
    "Z": 3,
}

score_result = {
    "win": 6,
    "draw": 3,
    "lose": 0
}

game_result = {
    "AX": "draw",
    "AY": "win",
    "AZ": "lose",
    "BX": "lose",
    "BY": "draw",
    "BZ": "win",
    "CX": "win",
    "CY": "lose",
    "CZ": "draw",
}

desired = {
    "X": "lose",
    "Y": "draw",
    "Z": "win"
}

map_desired_to_move = {
    "lose": {
        "A": "Z",
        "B": "X",
        "C": "Y"
    },
    "win":{
        "A": "Y",
        "B": "Z",
        "C": "X"
    },
    "draw":{
        "A":"X",
        "B":"Y",
        "C":"Z"
    }
}

#with open("test.txt") as file:
with open("day2.txt") as file:
    data = [x.strip() for x in file.readlines()]
    p1 = 0
    p2 = 0
    for line in data:
        moves = line.split()
        p1 += score[moves[1]] + score_result[game_result[moves[0]+moves[1]]]
        desired_outcome = desired[moves[1]]
        p2 += score[map_desired_to_move[desired_outcome][moves[0]]] + score_result[desired_outcome]

    print("Part 1 =", p1)    
    print("Part 2 =", p2)