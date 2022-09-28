from ast import main
import json
from json.encoder import INFINITY
from multiprocessing.connection import wait
from os.path import exists

costs = json.load(open('costs.json'))


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

print(localBoards)


def readMove():
    f = open('move_file', 'r')
    empty = not f.read(1)
    if empty:
        global mark
        mark = 'X'
    else:
        localBoards[int(f[2])][int(f[4])] = f[0]  # play
    move = choseMove()  # player X
    makeMove(move[0], move[1])


def choseMove():
    miniMax()
    return (0,0)


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

def main():
    #initialize game board, first 4 moves
    while not exists('AlphaO.go'):
        print('waiting for turn')
    if exists('end_game'):
        print('game over, did I win?')
    else:
        readMove()

    # #while the game isn't over keep playing.
    # while not exists('end_game'):
    #
    #     #if its our turn start playing
    #     if exists('AlphaO.go'):
    #         #perform minimax
    #
    #
    #         #write outcome of minimax to move file
    #
    #
    #
    #
    #     #if its not our turn wait.
    #     else:
            


def evaluatePosition(position,currentBoard):
    eval = 0
    mainBd = []
    evalMultiplier = [1.4,1,1.4,1,1.75,1,1.4,1,1.4]
    for x in range(9):
        eval += evaluate(position[x])*1.5*evalMultiplier[x]
        if x == currentBoard:
            eval += evaluate(position[x]*evalMultiplier[x])
        tmpEval = checkWinCondition(position[x])
        eval -= tmpEval*evalMultiplier[x]
        mainBd[x] = tmpEval
    eval -= checkWinCondition(mainBd)*5000
    eval += evaluate(mainBd)*150

    return eval


#positions: array of array of arrays of len 9, list of positions of big board
#maximizePlayer: boolean if we are maximizing or minimizing
#returns sorted array of array of arrays
def sort(currBoard, positions, maximizePlayer):
    return sorted(positions, key=lambda pos: evaluatePosition(pos, currBoard), reverse=maximizePlayer)


def evaluate(square):
    return costs[str(square)]

def evaluateSquare(square):
    eval = 0
    evalMultiplier = [0.2, 0.17, 0.2, 0.17, 0.22, 0.17, 0.2, 0.17, 0.2]
    for x in range(9):
        eval -=square[x]*evalMultiplier[x]
    a = 2
    if square[0] + square[1] + square[2] == a or square[3] + square[4] + square[5] == a or square[6] + square[7] + square[8] == a:
        eval -= 6
    if square[0] + square[3] + square[6] == a or square[1] + square[4] + square[7] == a or square[2] + square[5] + square[8] == a:
        eval -= 6
    
    if square[0] + square[4] + square[8] == a or square[2] + square[4] + square[6] == a:
        eval -= 7
    

    a = -1
    if((square[0] + square[1] == 2*a and square[2] == -a) or (square[1] + square[2] == 2*a and square[0] == -a) or (square[0] + square[2] == 2*a and square[1] == -a)
        or (square[3] + square[4] == 2*a and square[5] == -a) or (square[3] + square[5] == 2*a and square[4] == -a) or (square[5] + square[4] == 2*a and square[3] == -a)
        or (square[6] + square[7] == 2*a and square[8] == -a) or (square[6] + square[8] == 2*a and square[7] == -a) or (square[7] + square[8] == 2*a and square[6] == -a)
        or (square[0] + square[3] == 2*a and square[6] == -a) or (square[0] + square[6] == 2*a and square[3] == -a) or (square[3] + square[6] == 2*a and square[0] == -a)
        or (square[1] + square[4] == 2*a and square[7] == -a) or (square[1] + square[7] == 2*a and square[4] == -a) or (square[4] + square[7] == 2*a and square[1] == -a)
        or (square[2] + square[5] == 2*a and square[8] == -a) or (square[2] + square[8] == 2*a and square[5] == -a) or (square[5] + square[8] == 2*a and square[2] == -a)
        or (square[0] + square[4] == 2*a and square[8] == -a) or (square[0] + square[8] == 2*a and square[4] == -a) or (square[4] + square[8] == 2*a and square[0] == -a)
        or (square[2] + square[4] == 2*a and square[6] == -a) or (square[2] + square[6] == 2*a and square[4] == -a) or (square[4] + square[6] == 2*a and square[2] == -a)):
        eval-=9
    

    a = -2
    if(square[0] + square[1] + square[2] == a or square[3] + square[4] + square[5] == a or square[6] + square[7] + square[8] == a):
        eval += 6
    
    if(square[0] + square[3] + square[6] == a or square[1] + square[4] + square[7] == a or square[2] + square[5] + square[8] == a):
        eval += 6
    
    if(square[0] + square[4] + square[8] == a or square[2] + square[4] + square[6] == a):
        eval += 7
    

    a = 1
    if((square[0] + square[1] == 2*a and square[2] == -a) or (square[1] + square[2] == 2*a and square[0] == -a) or (square[0] + square[2] == 2*a and square[1] == -a)
        or (square[3] + square[4] == 2*a and square[5] == -a) or (square[3] + square[5] == 2*a and square[4] == -a) or (square[5] + square[4] == 2*a and square[3] == -a)
        or (square[6] + square[7] == 2*a and square[8] == -a) or (square[6] + square[8] == 2*a and square[7] == -a) or (square[7] + square[8] == 2*a and square[6] == -a)
        or (square[0] + square[3] == 2*a and square[6] == -a) or (square[0] + square[6] == 2*a and square[3] == -a) or (square[3] + square[6] == 2*a and square[0] == -a)
        or (square[1] + square[4] == 2*a and square[7] == -a) or (square[1] + square[7] == 2*a and square[4] == -a) or (square[4] + square[7] == 2*a and square[1] == -a)
        or (square[2] + square[5] == 2*a and square[8] == -a) or (square[2] + square[8] == 2*a and square[5] == -a) or (square[5] + square[8] == 2*a and square[2] == -a)
        or (square[0] + square[4] == 2*a and square[8] == -a) or (square[0] + square[8] == 2*a and square[4] == -a) or (square[4] + square[8] == 2*a and square[0] == -a)
        or (square[2] + square[4] == 2*a and square[6] == -a) or (square[2] + square[6] == 2*a and square[4] == -a) or (square[4] + square[6] == 2*a and square[2] == -a)):
        eval+=9
    

    eval -= checkWinCondition(square)*12

    return eval


def checkWinCondition(square):



def miniMax(position,boardToPlay, depth, alpha, beta, maximizingPlayer):
    if depth == 0:
        return position
    if maximizingPlayer == True:
        maxEval = -INFINITY
        nextMovePossibilities = getPossibleMoves(position,boardToPlay,alpha,beta,False)
        for child in nextMovePossibilities:
            eval = miniMax(child,)








