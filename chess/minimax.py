from copy import deepcopy

# had to copy chess.py's move piece function to prevent circular import
def move_piece(board, start, end, current_player):
    piece = board.get_piece(start)
    if piece and piece.is_valid_move(board, start, end) and piece.color == current_player[0]:
        board.set_piece(end, piece)
        board.set_piece(start, None)
        return True
    return False

# include heuristic here
def heuristic():
    pass

# minimax algorithm (reference https://blog.devgenius.io/simple-min-max-chess-ai-in-python-2910a3602641)
def minimaxN(board, current_player, N):
    # get all possible moves
    possible_moves = set()
    # iterate over chess board
    for j in range(len(board.grid[0])):
        for i in range(len(board.grid)):
            piece = board.grid[i][j]
            # first check to see if square is empty
            if piece == None:
                continue
            # then check to see if it is not the current player's color
            elif piece.color != current_player[0]:
                continue
            # if the piece is the current players piece, continue
            else:
                position = piece.indices_to_position(i, j)
                # get all possible squares the piece could move to
                possible_destinations = piece.possible_destinations(board, position)
                for destination in possible_destinations:
                    # add to possible moves
                    possible_moves.add(f"{position} {piece.indices_to_position(destination[0], destination[1])}")
    
    # heuristic scores and list of possible moves
    scores = []
    moves = list(possible_moves)

    # iterate over all possible moves
    for move in moves:
        # create a copy of the current board and take move
        newboard = deepcopy(board)
        start, end = move.split()
        move_piece(newboard, start, end, current_player)

        # recursive step
        if N>1:
            temp_best_move = minimaxN(newboard, current_player, N-1)
            s, e = temp_best_move.split()
            move_piece(newboard, s, e, current_player)
        
        # find heuristic value of current state of the board and add to scores
        scores.append(heuristic(board, current_player))
    
    # assuming that White is the max player and Black is the min player
    if current_player == 'White':
        best_move = moves[scores.index(max(scores))]
    else:
        best_move = moves[scores.index(min(scores))]
    
    # return best possible move 
    return best_move

# minimax algorithm wrapper function
def minimax(board, current_player):
    # start with N=1 for testing purposes
    N = 1
    return minimaxN(board, current_player, N)