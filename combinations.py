def generate():  # generates all permutations of boards
    f = open('combins', 'w')
    queue = []
    currBoard = [0 for i in range(9)]
    queue.extend(permute(currBoard, 0))
    for i in range(1,9):
        nodesToAdd = []
        while len(queue) > 0:
            currBoard = queue.pop()
            nodesToAdd.extend(permute(currBoard, i))
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

generate()