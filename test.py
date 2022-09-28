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

# board1 = [1,1,0,0,-1,-1,0,0,0]
# board2 = [1,1,0,0,-1,-1,0,0,0]
# board3 = [1,1,0,0,-1,-1,0,0,0]
# board4 = [1,1,0,0,-1,-1,0,0,0]
# board5 = [1,1,0,0,-1,-1,0,0,0]
# board6 = [1,1,0,0,-1,-1,0,0,0]
# board7 = [1,1,0,0,-1,-1,0,0,0]
# board8 = [1,1,0,0,-1,-1,0,0,0]
# board9 = [1,1,0,0,-1,-1,0,0,0]

board1 = [1,1,1,1,1,1,1,1,1]
board2 = [1,1,1,1,1,1,1,1,1]
board3 = [1,1,1,1,1,1,1,1,1]
board4 = [1,1,0,0,-1,-1,0,0,0]
board5 = [1,1,1,1,1,1,1,1,1]
board6 = [1,1,1,1,1,1,1,1,1]
board7 = [1,1,1,1,1,1,1,1,1]
board8 = [1,1,1,1,1,1,1,1,1]
board9 = [1,1,1,1,1,1,1,1,1]

board = [board1,board2,board3,board4,board5,board6,board7,board8,board9]


#if its true make -1s, meaning our turn
#pass in a big board

#make sure to return the big boards, and write down the possible moves and write new boards for those

#if wincondition returns 0, then we must play in that board
def next_possibleMoves(board, boardPosition, player):
    
    #this is the array of possible 9 x 9s (or arrays of smaller boards) 
    next_possible_moves = []

    #this is the copy of the total board that we need (9 x 9)
    new_board = board.copy()

    #list of boards if the board we must go to is a win/loss so we can pick 
    #from this list of new boards to play from
    playable_boards = []

    #setting which player it is to fill in the positions
    player = -1
    if(player):
      player = 1

    #this is a set of boards we are manipulating 
    #the position we were given for a board to play in within the 9 x 9 determined by a number 0 - 8 which is the boardPosition parameter)
    set_of_boards = []


    if(checkWinCondition(board[boardPosition])==0):
      #below is assigning the new X or O to the open spots on the given board we are playing in determined by a number 0 - 8
      for i in range(9):
        small_board = new_board[boardPosition].copy()
        if(small_board[i] == 0):
            small_board[i] = player
            set_of_boards.append(small_board)

      #below is making sets of possible 9 x 9s that we can have based on the spots we choose to fill from above 
      for j in range(len(set_of_boards)):
        new_set = []
        for i in range(9):
          if(i == boardPosition):
            new_set.append(set_of_boards[j])
          else:
            new_set.append(new_board[i])
        next_possible_moves.append(new_set)
      
    else:
      #getting a list of boards we can move too
      positions = []
      for i in range(9):
        if(checkWinCondition(board[i])==0):
          playable_boards.append(board[i])
          positions.append(i)

     #we are looping through the boards that we have deemed playable and making the 
     #possible 9 x 9s to play
      for j in range(len(playable_boards)):
        new_set_of_boards = []
        for i in range(9):
          small_board = playable_boards[j].copy()
          if(small_board[i] == 0):
              small_board[i] = player
              new_set_of_boards.append(small_board)

        for k in range(len(new_set_of_boards)):
          new_set = []
          for l in range(9):
            if(l == positions[j]):
              new_set.append(new_set_of_boards[k])
            else:
              new_set.append(new_board[l])
          next_possible_moves.append(new_set)
          
    return next_possible_moves

print(next_possibleMoves(board,4,False))










