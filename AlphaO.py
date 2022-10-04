import json
import time
from json.encoder import INFINITY
from multiprocessing.connection import wait
from os.path import exists
from copy import deepcopy
import sys
import os
import numpy as np


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


costs = json.load(open(resource_path('costs_data.json')))

mark = 'O'

lastMove = -1

turn = False

depth = 7

emptySpaces = 77

# player 1 = x 2 = o
timelimit = 10  # seconds
timeBuffer = 0.09

position = [[0 for i in range(9)] for i in range(9)]
globalBoard = [0 for i in range(9)]

firstMove = True

count = 0
othercount = 0

start = 0


def doTurn():
    global count
    global othercount
    count = 0
    othercount = 0
    file = open('move_file', 'r')
    f = file.readline().split(" ")
    if f[0] != 'AlphaO':
        global start
        start = time.time()
        print('O Thinking')
        global depth
        global turn
        global firstMove
        global emptySpaces
        global lastMove
        if firstMove:
            firstMove = False
            empty = not f[0]
            if empty:
                print('Im player one')
                replaceXO()
            else:
                lastMove = int(f[2])
                position[int(f[1])][int(f[2])] = 1  # play
        else:
            emptySpaces -= 1
            lastMove = int(f[2])
            position[int(f[1])][int(f[2])] = 1  # play
            print(int(f[1]), int(f[2]))
        move = miniMax(position, lastMove, depth, -INFINITY, INFINITY, False)
        makeMove(move.move)
        position[move.move[0]][move.move[1]] = -1
        emptySpaces -= 1
        if emptySpaces <= 20:
            depth = 8
        print(move.move)
        print('count',count)
        print('othercount',othercount)

        # print('Eval: ',move.cost)
        print('Time: ', time.time() - start)
        # print('Last: ', lastMove)
        # print('Move: ', move.move)
        # turn = not turn
    file.close()


def replaceXO():
    for i in range(9):
        for j in range(9):
            position[i][j] *= -1


def makeMove(move):
    f = open('move_file', 'w')
    f.write(f'AlphaO {move[0]} {move[1]}')
    f.close()


def main():
    global lastMove
    global position
    while not exists("first_four_moves"):
        pass
    f = open("first_four_moves", "r")
    for line in f:
        position[int(line[2])][int(line[4])] = 1 if line[0] == 'X' else -1
        lastMove = int(line[4])
        # print(line)
    f.close()
    # print(position)
    while not exists('end_game'):
        if exists('AlphaO.go'):
            doTurn()
            # time.sleep(.1)  # so we don't make two moves in a row
    print('Game Over')


def evaluatePosition(position, currentBoard):
    eval = 0
    mainBd = []
    evalMultiplier = [1.4, 1, 1.4, 1, 1.75, 1, 1.4, 1, 1.4]
    for x in range(9):
        eval += evaluate(position[x]) * 1.5 * evalMultiplier[x]
        if x == currentBoard:
            eval += evaluate(position[x]) * evalMultiplier[x]
        tmpEval = checkWinCondition(position[x])
        eval -= tmpEval * evalMultiplier[x]
        mainBd.append(tmpEval)
    eval -= checkWinCondition(mainBd) * 5000
    eval += evaluate(mainBd) * 150

    return eval


# positions: array of array of arrays of len 9, list of positions of big board
# maximizePlayer: boolean if we are maximizing or minimizing
# returns sorted array of array of arrays
def sort(currBoard, positions, maximizePlayer):
    return sorted(positions, key=lambda pos: evaluatePosition(pos, currBoard), reverse=maximizePlayer)


def evaluate(square):
    return costs[str(square)]


def evaluateSquare(square):
    eval = 0
    evalMultiplier = [0.2, 0.17, 0.2, 0.17, 0.22, 0.17, 0.2, 0.17, 0.2]
    for x in range(9):
        eval -= square[x] * evalMultiplier[x]
    a = 2
    if square[0] + square[1] + square[2] == a or square[3] + square[4] + square[5] == a or square[6] + square[7] + \
            square[8] == a:
        eval -= 6
    if square[0] + square[3] + square[6] == a or square[1] + square[4] + square[7] == a or square[2] + square[5] + \
            square[8] == a:
        eval -= 6

    if square[0] + square[4] + square[8] == a or square[2] + square[4] + square[6] == a:
        eval -= 7

    a = -1
    if ((square[0] + square[1] == 2 * a and square[2] == -a) or (
            square[1] + square[2] == 2 * a and square[0] == -a) or (square[0] + square[2] == 2 * a and square[1] == -a)
            or (square[3] + square[4] == 2 * a and square[5] == -a) or (
                    square[3] + square[5] == 2 * a and square[4] == -a) or (
                    square[5] + square[4] == 2 * a and square[3] == -a)
            or (square[6] + square[7] == 2 * a and square[8] == -a) or (
                    square[6] + square[8] == 2 * a and square[7] == -a) or (
                    square[7] + square[8] == 2 * a and square[6] == -a)
            or (square[0] + square[3] == 2 * a and square[6] == -a) or (
                    square[0] + square[6] == 2 * a and square[3] == -a) or (
                    square[3] + square[6] == 2 * a and square[0] == -a)
            or (square[1] + square[4] == 2 * a and square[7] == -a) or (
                    square[1] + square[7] == 2 * a and square[4] == -a) or (
                    square[4] + square[7] == 2 * a and square[1] == -a)
            or (square[2] + square[5] == 2 * a and square[8] == -a) or (
                    square[2] + square[8] == 2 * a and square[5] == -a) or (
                    square[5] + square[8] == 2 * a and square[2] == -a)
            or (square[0] + square[4] == 2 * a and square[8] == -a) or (
                    square[0] + square[8] == 2 * a and square[4] == -a) or (
                    square[4] + square[8] == 2 * a and square[0] == -a)
            or (square[2] + square[4] == 2 * a and square[6] == -a) or (
                    square[2] + square[6] == 2 * a and square[4] == -a) or (
                    square[4] + square[6] == 2 * a and square[2] == -a)):
        eval -= 9

    a = -2
    if (square[0] + square[1] + square[2] == a or square[3] + square[4] + square[5] == a or square[6] + square[7] +
            square[8] == a):
        eval += 6

    if (square[0] + square[3] + square[6] == a or square[1] + square[4] + square[7] == a or square[2] + square[5] +
            square[8] == a):
        eval += 6

    if (square[0] + square[4] + square[8] == a or square[2] + square[4] + square[6] == a):
        eval += 7

    a = 1
    if ((square[0] + square[1] == 2 * a and square[2] == -a) or (
            square[1] + square[2] == 2 * a and square[0] == -a) or (square[0] + square[2] == 2 * a and square[1] == -a)
            or (square[3] + square[4] == 2 * a and square[5] == -a) or (
                    square[3] + square[5] == 2 * a and square[4] == -a) or (
                    square[5] + square[4] == 2 * a and square[3] == -a)
            or (square[6] + square[7] == 2 * a and square[8] == -a) or (
                    square[6] + square[8] == 2 * a and square[7] == -a) or (
                    square[7] + square[8] == 2 * a and square[6] == -a)
            or (square[0] + square[3] == 2 * a and square[6] == -a) or (
                    square[0] + square[6] == 2 * a and square[3] == -a) or (
                    square[3] + square[6] == 2 * a and square[0] == -a)
            or (square[1] + square[4] == 2 * a and square[7] == -a) or (
                    square[1] + square[7] == 2 * a and square[4] == -a) or (
                    square[4] + square[7] == 2 * a and square[1] == -a)
            or (square[2] + square[5] == 2 * a and square[8] == -a) or (
                    square[2] + square[8] == 2 * a and square[5] == -a) or (
                    square[5] + square[8] == 2 * a and square[2] == -a)
            or (square[0] + square[4] == 2 * a and square[8] == -a) or (
                    square[0] + square[8] == 2 * a and square[4] == -a) or (
                    square[4] + square[8] == 2 * a and square[0] == -a)
            or (square[2] + square[4] == 2 * a and square[6] == -a) or (
                    square[2] + square[6] == 2 * a and square[4] == -a) or (
                    square[4] + square[6] == 2 * a and square[2] == -a)):
        eval += 9

    eval -= checkWinCondition(square) * 12

    return eval


def checkWinCondition(square):
    a = 1
    if (square[0] + square[1] + square[2] == a * 3 or square[3] + square[4] + square[5] == a * 3 or square[6] + square[
        7] + square[8] == a * 3 or square[0] + square[3] + square[6] == a * 3 or square[1] + square[4] + square[
        7] == a * 3 or
            square[2] + square[5] + square[8] == a * 3 or square[0] + square[4] + square[8] == a * 3 or square[2] +
            square[4] + square[6] == a * 3):
        return a

    a = -1
    if (square[0] + square[1] + square[2] == a * 3 or square[3] + square[4] + square[5] == a * 3 or square[6] + square[
        7] + square[8] == a * 3 or square[0] + square[3] + square[6] == a * 3 or square[1] + square[4] + square[
        7] == a * 3 or
            square[2] + square[5] + square[8] == a * 3 or square[0] + square[4] + square[8] == a * 3 or square[2] +
            square[4] + square[6] == a * 3):
        return a

    return 0


class Move:
    def __init__(self, position, move):
        self.position = deepcopy(position)
        self.move = move
        self.cost = evaluatePosition(self.position, move[0])


def getPossibleMoves(position, boardToPlay, maximizingPlayer):
    player = -1
    if (maximizingPlayer):
        player = 1
    nextPossibleMoves = []

    if checkWinCondition(position[boardToPlay]) == 0 and 0 in position[boardToPlay]:
        for x in range(9):
            if position[boardToPlay][x] == 0:
                tmp = deepcopy(position)
                tmp[boardToPlay][x] = player
                move = Move(tmp, [boardToPlay, x])
                nextPossibleMoves.append(move)
    else:
        for x in range(9):
            if (checkWinCondition(position[x]) == 0):
                for y in range(9):
                    if position[x][y] == 0:
                        tmp = deepcopy(position)
                        tmp[x][y] = player
                        move = Move(tmp, [x, y])
                        nextPossibleMoves.append(move)
    nextPossibleMoves = sorted(nextPossibleMoves, key=lambda m: m.cost, reverse=not maximizingPlayer)
    return nextPossibleMoves


def miniMax(position, boardToPlay, depth, alpha, beta, maximizingPlayer):
    global count
    global othercount
    othercount += 1
    if depth == 0:
        count += 1
    tmpMove = Move(position, [-1, -1])
    if (time.time() - start) >= timelimit - timeBuffer or depth == 0:
        return tmpMove
    if not maximizingPlayer:
        nextMovePossibilities = getPossibleMoves(position, boardToPlay, False)
        if len(nextMovePossibilities) == 0:
            return Move(position, [-1, -1])
        maxEval = nextMovePossibilities[0]
        maxEval.cost = -INFINITY
        for child in nextMovePossibilities:
            eval = miniMax(child.position, child.move[1], depth - 1, alpha, beta, True)
            if eval.cost > maxEval.cost:
                maxEval = deepcopy(eval)
                maxEval.move = deepcopy(child.move)
            alpha = max(alpha, eval.cost)
            if beta <= alpha:
                break
        return maxEval

    if maximizingPlayer:
        nextMovePossibilities = getPossibleMoves(position, boardToPlay, True)
        if len(nextMovePossibilities) == 0:
            return Move(position, [-1, -1])
        minEval = nextMovePossibilities[0]
        minEval.cost = INFINITY
        for child in nextMovePossibilities:
            eval = miniMax(child.position, child.move[1], depth - 1, alpha, beta, False)
            if eval.cost < minEval.cost:
                minEval = deepcopy(eval)
                minEval.move = deepcopy(child.move)
            beta = min(beta, eval.cost)
            if beta <= alpha:
                break
        return minEval


def test():
    board = [[0 for i in range(9)] for i in range(9)]
    board[4][0] = 1
    board[4][6] = 1
    print(board)
    global start
    start = time.time()
    move = miniMax(board, 1, 5, -INFINITY, INFINITY, False)
    end = time.time()
    print('Minimax: ', int((end - start) * 1000), 'ms')
    print(move.move)


# test()

main()

position = [[-1,0,0,0,1,0,1,0,0],[0,0,0,0,0,0,0,0,0],[-1,0,0,0,-1,0,0,0,-1],[0,0,0,0,0,0,0,0,0],[1,1,1,0,-1,0,0,0,1],[0,0,0,0,0,0,0,0,0],[0,0,0,0,-1,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,1,0,-1,0,0,0,0]]
print(evaluatePosition(position,4))
# print(miniMax(position,6,6,-INFINITY, INFINITY,False).move)
# position = [[1,1,1,0,0,0,0,0,0],[-1,-1,-1,0,0,0,0,0,0],[1,1,1,0,0,0,0,0,0],[-1,-1,-1,0,0,0,0,0,0],[-1,-1,-1,0,0,0,0,0,0],[1,1,1,0,0,0,0,0,0],[1,-1,1,1,1,-1,0,1,0],[1,1,1,0,0,0,0,0,0],[-1,-1,-1,0,0,0,0,0,0]]
# print(miniMax(position,6,6,-INFINITY, INFINITY,False).move)
