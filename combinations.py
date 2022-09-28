import json
import time
def calculateCosts():
    dict = {}
    combs = generate()
    costs = []
    for comb in combs:
        dict[str(comb)] = evaluateSquare(comb)
    json_object = json.dumps(dict, indent=4)
    with open("costs.json", "w") as outfile:
        outfile.write(json_object)


def generate():  # generates all permutations of boards
    # f = open('combins', 'w')
    queue = []
    currBoard = [0 for i in range(9)]
    queue.extend(permute(currBoard, 0))
    for i in range(1,9):
        nodesToAdd = []
        while len(queue) > 0:
            currBoard = queue.pop()
            nodesToAdd.extend(permute(currBoard, i))
        queue = nodesToAdd
    return queue
    # print(len(queue))
    # f.write(str(queue))


def permute(board, move):  # places 3 different players in the given spot on the array board
    ret = []
    players = [-1, 0, 1]
    for player in players:
        temp = board.copy()
        temp[move] = player
        ret.append(temp)
    return ret


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


def checkWinCondition(map):
    a = 1
    if (map[0] + map[1] + map[2] == a * 3 or map[3] + map[4] + map[5] == a * 3 or map[6] + map[7] + map[8] == a * 3 or
            map[0] + map[3] + map[6] == a * 3 or map[1] + map[4] + map[7] == a * 3 or
            map[2] + map[5] + map[8] == a * 3 or map[0] + map[4] + map[8] == a * 3 or map[2] + map[4] + map[
                6] == a * 3):
        return a

    a = -1
    if (map[0] + map[1] + map[2] == a * 3 or map[3] + map[4] + map[5] == a * 3 or map[6] + map[7] + map[8] == a * 3 or
            map[0] + map[3] + map[6] == a * 3 or map[1] + map[4] + map[7] == a * 3 or
            map[2] + map[5] + map[8] == a * 3 or map[0] + map[4] + map[8] == a * 3 or map[2] + map[4] + map[
                6] == a * 3):
        return a

    return 0

# calculateCosts()

arr = generate()

start = time.time()
costs = json.load(open('costs.json'))
end = time.time()
print('Load: ', int((end-start) * 1000), 'ms')


start = time.time()
for i in range(len(arr)):
    var = costs[str(arr[i])]
end = time.time()
print('Map: ', int((end-start) * 1000), 'ms')

start = time.time()
for i in range(len(arr)):
    evaluateSquare(arr[i])
end = time.time()
print('Evaluate: ', int((end-start) * 1000), 'ms')
