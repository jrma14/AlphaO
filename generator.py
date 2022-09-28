import numpy as np
import json

globalBoard = [0 for i in range(9)]
allBoards = []

g = open('combinations_orig', 'w')


# board class that has cost included
class board():

    def __init__(self, board=[0 for i in range(9)]):
        self.board = board
        self.cost = 0

    def __str__(self):
        return f'Board: {self.board} Cost:{self.cost}\n'

    def __cmp__(self, other):
        if self.cost < other.cost:
            return 1
        elif self.cost == other.cost:
            return 0
        else:
            return -1

    def __hash__(self):
        return hash(((x for x in self.board), self.cost))

    def __eq__(self, other):
        for i, e in enumerate(other.board):
            if e != self.board[i]:
                return False
        return True

    def bToStr(self):
        ret = ''
        for x in self.board:
            ret += str(x)
        return ret

    def bToInvStr(self):
        ret = ''
        for x in self.board:
            ret += str(-1 * x)
        return ret


# node class for tree
class node:
    def __init__(self, board=board()):
        self.b = board
        self.children = []

    def __str__(self):
        return f'{str(self.b)}\nChildren:{str(self.children)}'


def maketree():  # recursive helper for, not checked if working
    tree = node()
    addToTree(tree, 1)
    print(tree)


def addToTree(tree, lvl):  # creates the tree of permutations of board objects
    queue = []
    while lvl < 9:
        children = permuteBoard(tree.b, lvl)
        childrenNodes = list(map(lambda child: node(board(child.board)), children))
        queue.extend(childrenNodes)
        tree.children = childrenNodes
        while (len(queue) > 0):
            addToTree(queue.pop(), lvl + 1)


def cost():
    b = board()
    cost = calculateCost(b, 1)
    print(cost)
    print(allBoards)
    f = open('costs', 'w')
    f.write(str(allBoards))
    f.close()


def calculateCost(b: board, move):
    queue = []
    queue.extend(permuteBoard(b, move))
    currBoard = b
    while move < 8:
        nodesToAdd = []
        while len(queue) > 0:
            currBoard = queue.pop()
            allBoards.append(currBoard)
            nodesToAdd.extend(permuteBoard(currBoard, move))
            for i in nodesToAdd:
                cost = calculateCost(i, move + 1)
                print(cost)
                currBoard.cost += cost
        queue = nodesToAdd
    return checkWin(currBoard.board)


def permuteBoard(b: board, move):  # permutes a board object
    try:
        ret = []
        players = [-1, 0, 1]
        for player in players:
            temp = b.board.copy()
            temp[move] = player
            retB = board()
            retB.board = temp
            ret.append(retB)
        return ret
    except Exception as e:
        print(move)
        print(e)


def generate():  # generates all permutations of boards
    f = open('combins', 'w')
    queue = []
    currBoard = [0 for i in range(9)]
    queue.extend(permute(currBoard, 0))
    move = 0
    while len(queue) > 0 and move < 8:
        move += 1
        nodesToAdd = []
        while len(queue) > 0:
            currBoard = queue.pop()
            nodesToAdd.extend(permute(currBoard, move))
        queue = nodesToAdd
    print(len(queue))
    f.write(str(queue))


def permute(board, move):  # places 3 different players in the given spot on the array board
    ret = []
    players = [-1, 0, 1]
    for player in players:
        temp = board.copy()
        temp[move] = player
        ret.append(temp)
    return ret


def makeMove(board, move, player):  # makes move on board and returns that board as array, not the object
    temp = board.copy()
    temp[move] = player
    return temp


def allCombs():  # 300,000
    queue = []
    player = 1
    for move in getNextPossibleMoves(globalBoard):
        queue.insert(0, makeMove(globalBoard, move, player))
    while len(queue) > 0:
        player *= -1
        currBoard = queue.pop()
        allBoards.append(currBoard)
        for move in getNextPossibleMoves(currBoard):
            queue.insert(0, makeMove(currBoard, move, player))
    print(len(allBoards))
    g.write(str(allBoards))


allCosts = []


def idkanymore(board, player):  # generates all possible permutations of boards and calculates the utility cost
    queue = []
    moves = getNextPossibleMoves(board.board)
    if len(moves) == 0:
        return checkWin(board.board)
    for move in moves:
        queue.insert(0, performMove(board.board, move, player))
    nextBoards = []
    while len(queue) > 0:
        nextBoard = queue.pop()
        nextBoards.append(nextBoard)
        nextBoard.cost += idkanymore(nextBoard, player * -1)
        allCosts.append(nextBoard)
    for nextBoard in nextBoards:
        # print(nextBoard)
        board.cost += nextBoard.cost
    # print(board)
    allCosts.append(board)
    return board.cost


def performMove(b, move, player):  # makes a move on a board and returns board object
    temp = b.copy()
    temp[move] = player
    return board(temp)


def getNextPossibleMoves(board):  # returns array of next possible moves of board given as array
    moves = []
    if (checkWin(board)):
        return moves
    for i in range(len(board)):
        if board[i] == 0:
            moves.append(i)
    return moves


def checkWin(board):  # single array
    if board[0] != 0 and board[0] == board[4] == board[8]:
        return board[0]
    if board[2] != 0 and board[2] == board[4] == board[6]:
        return board[2]
    for i in range(0, 3):
        if board[i] != 0 and board[i] == board[3 + i] == board[6 + i]:
            return board[i]
        if board[3 * i] != 0 and board[3 * i] == board[3 * i + 1] == board[3 * i + 2]:
            return board[3 * i]
    return 0


generate()
# cost()
# maketree()
# allCombs()

# b = board()
# idkanymore(b, 1)
# res = []

# print('Num combinations:', len(allCosts))
# res = list(set(allCosts))
#
# f = open('testingcost.txt', 'w')
# sort = sorted(res, key=lambda b: b.cost)
# for b in sort:
#     f.write(str(b))
#
# resMap = {}
# for b in sort:
#     resMap[b.bToStr()] = b.cost
#     resMap[b.bToInvStr()] = -1 * b.cost
# json_object = json.dumps(resMap, indent=4)
# with open("data.json", "w") as outfile:
#     outfile.write(json_object)
