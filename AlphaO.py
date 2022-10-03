from ast import main
from json.encoder import INFINITY
from multiprocessing.connection import wait
from os.path import exists
from copy import deepcopy

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


    #while the game isn't over keep playing.
    while not exists('end_game'):

        #if its our turn start playing
        if exists('AlphaO.go'):
            #perform minimax
            a = 4

            #write outcome of minimax to move file




        #if its not our turn wait.


def evaluatePosition(position,currentBoard):
    eval = 0
    mainBd = []
    evalMultiplier = [1.4,1,1.4,1,1.75,1,1.4,1,1.4]
    for x in range(9):
        eval += evaluateSquare(position[x])*1.5*evalMultiplier[x]
        if x == currentBoard:
            eval += evaluateSquare(position[x])*evalMultiplier[x]
        tmpEval = checkWinCondition(position[x])
        eval -= tmpEval*evalMultiplier[x]
        mainBd.append(tmpEval)
    eval -= checkWinCondition(mainBd)*5000
    eval += evaluateSquare(mainBd)*150

    return eval





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
    a = 1
    if (square[0] + square[1] + square[2] == a * 3 or square[3] + square[4] + square[5] == a * 3 or square[6] + square[7] + square[8] == a * 3 or square[0] + square[3] + square[6] == a * 3 or square[1] + square[4] + square[7] == a * 3 or
        square[2] + square[5] + square[8] == a * 3 or square[0] + square[4] + square[8] == a * 3 or square[2] + square[4] + square[6] == a * 3):
        return a
    
    a = -1
    if (square[0] + square[1] + square[2] == a * 3 or square[3] + square[4] + square[5] == a * 3 or square[6] + square[7] + square[8] == a * 3 or square[0] + square[3] + square[6] == a * 3 or square[1] + square[4] + square[7] == a * 3 or
        square[2] + square[5] + square[8] == a * 3 or square[0] + square[4] + square[8] == a * 3 or square[2] + square[4] + square[6] == a * 3):
        return a
    
    return 0

class Move:
    def __init__(self,position,move):
        self.position = position.deepcopy()
        self.move = move
        self.cost = evaluatePosition(self.position,move[0])



def getPossibleMoves(position, boardToPlay, maximizingPlayer):
    player = -1
    if(maximizingPlayer):
        player = 1
    nextPossibleMoves = []

    if checkWinCondition(position[boardToPlay]) == 0 and 0 in position[boardToPlay]:
        for x in range(9):
            if position[boardToPlay][x] == 0:
                tmp = position.deepcopy()
                tmp[boardToPlay][x] = player
                move = Move(tmp,[boardToPlay,x])
                nextPossibleMoves.append(move)
    else:
        for x in range(9):
            if(checkWinCondition(position[x]) == 0):
                for y in range(9):
                    if position[x][y] == 0:
                        tmp = position.deepcopy()
                        tmp[x][y] = player
                        move = Move(tmp,[x,y])
                        nextPossibleMoves.append(move)
    nextPossibleMoves = sorted(nextPossibleMoves, key=lambda m: m.cost, reverse = True)
    return nextPossibleMoves                    







def miniMax(position,boardToPlay, depth, alpha, beta, maximizingPlayer):
    if depth == 0:
        tmpMove = Move(position,[-1,-1])
        return tmpMove
    if maximizingPlayer == False:
        maxEval = Move(position,[0,0])
        maxEval.cost = -INFINITY
        nextMovePossibilities = getPossibleMoves(position,boardToPlay,False)
        for child in nextMovePossibilities:
            eval = miniMax(child.position,child.move[1], depth -1, alpha,beta, True)
            if eval.cost > maxEval.cost:
                maxEval = eval
                maxEval.move = child.move
            alpha = max(alpha, eval.cost)
            if beta <= alpha:
                break
        return maxEval

    if maximizingPlayer == True:
        minEval = Move(position,[0,0])
        minEval.cost = INFINITY
        nextMovePossibilities = getPossibleMoves(position,boardToPlay,True)
        for child in nextMovePossibilities:
            eval = miniMax(child.position,child.move[1],depth-1,alpha,beta,False)
            if eval.cost < minEval.cost:
                minEval = eval
                minEval.move = child.move
            beta = min(beta,eval.cost)
            if beta <= alpha:
                break
        return minEval


def test():
    board = [[0 for i in range(9)] for i in range(9)]
    print(board)
    move = miniMax(board,4,10,-INFINITY,INFINITY, False)
    print(move.move)
    print(board)

test()


