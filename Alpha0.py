localBoards = [[0 for i in range(9)] for i in range(9)]
globalBoard = [[0 for i in range(3) ] for i in range(3)]

f = open("first_four_moves","r")

for line in f:
    localBoards[int(line[2])][int(line[4])] = line[0]
    print(line)

print(localBoards)