from os.path import exists
import json

data = json.load(open('data.json'))

mark = 'O'

# player 1 = x 2 = o
timelimit = 10  # seconds

localBoards = [[0 for i in range(9)] for i in range(9)]
globalBoard = [0 for i in range(9)]

f = open("first_four_moves", "r")

for line in f:
    localBoards[int(line[2])][int(line[4])] = line[0]
    print(line)
f.close()


# for localBoard in localBoards:
#     ret = ''
#     for x in localBoard:
#         if x == 'X':
#             ret += '1'
#         if x == 'O':
#             ret += '-1'
#         if x == 0:
#             ret += '0'
#     print(data[ret])
# print(localBoards)


def readMove():
    f = open('move_file', 'r')
    empty = not f.read(1)
    if empty:
        global mark
        mark = 'X'
    else:
        localBoards[int(int(f[2]) / 3) * 3 + int(int(f[4]) / 3)][int(f[4]) % 3 + int(f[2]) % 3 * 3] = f[0]  # player o
    move = choseMove()  # player X
    makeMove(move[0], move[1])


def choseMove():
    return (0, 0)


def makeMove(i, j):
    f = open('move_file', 'w')
    f.write(f'AlphaO {i} {j}')
    f.close()


def waitForTurn():
    while not exists('AlphaO.go'):
        print('waiting for turn')
    if exists('end_game'):
        print('game over, did I win?')
    else:
        readMove()

# waitForTurn()
