import numpy as np

globalBoard = [0 for i in range(9)]
allBoards = []


class board():

    def __init__(self, board = [0 for i in range(9)]):
        self.board = board
        self.cost = 0
    def __str__(self):
        return f'Board: {self.board}\nCost:{self.cost}'


class node:
    def __init__(self, board = board()):
        self.b = board
        self.children = []
    def __str__(self):
        return f'{str(self.b)}\nChildren:{str(self.children)}'


def maketree():
    tree = node()
    addToTree(tree, 1)
    print(tree)


def addToTree(tree, lvl):
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
    return checkWin(currBoard.board)  # make checkWin return 1 for player, -1 for opponet, 0 for tie


def permuteBoard(b: board, move):
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


def generate():
    f = open('combins', 'w')
    queue = []
    move = 0
    currBoard = [0 for i in range(9)]
    queue.extend(permute(currBoard, move))
    while move < 8:
        move += 1
        nodesToAdd = []
        while len(queue) > 0:
            currBoard = queue.pop()
            allBoards.append(currBoard)
            nodesToAdd.extend(permute(currBoard, move))
        queue = nodesToAdd
    print(len(allBoards))
    f.write(str(allBoards))


def permute(board, move):
    try:
        ret = []
        players = [-1, 0, 1]
        for player in players:
            temp = board.copy()
            temp[move] = player
            ret.append(temp)
        return ret
    except Exception as e:
        print(move)
        print(e)


def makeMove(board, move, player):
    temp = board.copy()
    temp[move] = player
    return temp


def getNextPossibleMoves(board):
    moves = []
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


# generate()

# cost()
maketree()
# print(checkWin([0,1,1,0,1,0,0,1,0]))
import numpy as np

globalBoard = [0 for i in range(9)]
allBoards = []


class board():

    def __init__(self, board = [0 for i in range(9)]):
        self.board = board
        self.cost = 0
    def __str__(self):
        return f'Board: {self.board}\nCost:{self.cost}'


class node:
    def __init__(self, board = board()):
        self.b = board
        self.children = []
    def __str__(self):
        return f'{str(self.b)}\nChildren:{str(self.children)}'


def maketree():
    tree = node()
    addToTree(tree, 1)
    print(tree)


def addToTree(tree, lvl):
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
    return checkWin(currBoard.board)  # make checkWin return 1 for player, -1 for opponet, 0 for tie


def permuteBoard(b: board, move):
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


def generate():
    f = open('combins', 'w')
    queue = []
    move = 0
    currBoard = [0 for i in range(9)]
    queue.extend(permute(currBoard, move))
    while move < 8:
        move += 1
        nodesToAdd = []
        while len(queue) > 0:
            currBoard = queue.pop()
            allBoards.append(currBoard)
            nodesToAdd.extend(permute(currBoard, move))
        queue = nodesToAdd
    print(len(allBoards))
    f.write(str(allBoards))


def permute(board, move):
    try:
        ret = []
        players = [-1, 0, 1]
        for player in players:
            temp = board.copy()
            temp[move] = player
            ret.append(temp)
        return ret
    except Exception as e:
        print(move)
        print(e)


def makeMove(board, move, player):
    temp = board.copy()
    temp[move] = player
    return temp


def getNextPossibleMoves(board):
    moves = []
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


# generate()

# cost()
maketree()
# print(checkWin([0,1,1,0,1,0,0,1,0]))
