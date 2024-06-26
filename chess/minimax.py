import copy
import math
from copy import deepcopy
from pawn import Pawn
from piece import Piece
from bishop import Bishop
from knight import knight
from rook import Rook
from king import King
from queen import Queen

# had to copy chess.py's move piece function to prevent circular import
def move_piece(board, start, end, current_player):
    piece = board.get_piece(start)
    if piece and piece.is_valid_move(board, start, end) and piece.color == current_player[0]:
        board.set_piece(end, piece)
        board.set_piece(start, None)
        return True
    return False

# functions for check and checkmate are also copied for same reason
def is_checkmate(board, current_player):
    # used for checkmate
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
    
    # failsafe
    if (len(possible_moves) == 0):
        return False

    # create multiple instances of board where each possible move is taken
    possible_boards = []
    for move in possible_moves:
        newboard = copy.deepcopy(board)
        start, end = move.split()
        move_piece(newboard, start, end, current_player)
        possible_boards.append(newboard)
    
    # iterate through all possibilities and if any are not in check, return false
    for pboard in possible_boards:
        if (is_check(pboard, current_player)):
            continue
        else:
            return False
    
    # if all possibilities are in check, return true
    return True

def is_check(board, current_player):
    # iterate over chess board
    for j in range(len(board.grid[0])):
        for i in range(len(board.grid)):
            piece = board.grid[i][j]
            # first check to see if square is empty
            if piece == None:
                continue
            # then check to see if it is the current player's color
            elif piece.color == current_player[0]:
                continue
            # if the piece is the other player's piece, continue
            else:
                position = piece.indices_to_position(i, j)
                # get all possible squares the piece could move to
                possible_destinations = piece.possible_destinations(board, position)
                for destination in possible_destinations:
                    # if the current player's king is reachable, return true
                    if type(board.grid[destination[0]][destination[1]]) == King and board.grid[destination[0]][destination[1]].color == current_player[0]:
                        return True
    # otherwise, return false
    return False

# include heuristic here
def heuristic(board, color):
    #evaluate pieces for general value
    value = 0
    for i in range(8):
        for j in range(8):
        #check each square to see its state
            if not(board.grid[i][j] is None):
                #check which kind of piece it is: if it is white, add, if it is black, subtract If it is the other color subtract
                #add 1 to each of the pieces values for each square it has advanced beyond its starting position
                if isinstance(board.grid[i][j], Pawn):
                    if board.grid[i][j].color == color[0]:
                        if color == 'White':
                            value += i-1
                        else:
                            value -= 6-i
                    if board.grid[i][j].color == 'W':
                        value += 1
                    else:
                        value -= 1
                if isinstance(board.grid[i][j], Bishop):
                    if board.grid[i][j].color == color[0]:
                        if color == 'White':
                            value += i
                        else:
                            value -= 7-i
                    if board.grid[i][j].color == 'W':
                        value += 3
                    else:
                        value -= 3
                if isinstance(board.grid[i][j], knight):
                    if board.grid[i][j].color == color[0]:
                        if color == 'White':
                            value += i
                        else:
                            value -= 7-i
                    if board.grid[i][j].color == 'W':
                        value += 3
                    else:
                        value -= 3
                if isinstance(board.grid[i][j], Rook):
                    if board.grid[i][j].color == color[0]:
                        if color == 'White':
                            value += i
                        else:
                            value -= 7-i
                    if board.grid[i][j].color == 'W':
                        value += 5
                    else:
                        value -= 5
                if isinstance(board.grid[i][j], Queen):
                    if board.grid[i][j].color == color[0]:
                        if color == 'White':
                            value += i
                        else:
                            value -= 7-i
                    if board.grid[i][j].color == 'W':
                        value += 9
                    else:
                        value -= 9
                if isinstance(board.grid[i][j], King):
                    if board.grid[i][j].color == 'W':
                        value += 1000
                    else:
                        value -= 1000


    #check for checkmate: use function developed in the other main program to determine if checkmate is possible for either, these should always be prioritized
    if is_checkmate(board, 'B'):
        value += 500

    if is_checkmate(board, 'W'):
        value -= 500

    #do the same for check
    if is_check(board, 'B'):
        value += 200
        

    if(is_check(board, 'W')):
        value -= 200

    return value

# minimax algorithm (reference https://blog.devgenius.io/simple-min-max-chess-ai-in-python-2910a3602641)
def minimaxN(board, current_player, N, alpha, beta):
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

    maxVal = -math.inf
    minVal = math.inf

    # iterate over all possible moves
    for move in moves:
        # create a copy of the current board and take move
        newboard = deepcopy(board)
        start, end = move.split()
        move_piece(newboard, start, end, current_player)
        # recursive step
        if N>1:
            if current_player == 'White':
                temp_best_move = minimaxN(newboard, 'Black', N-1, alpha, beta)
                if len(scores) > 0:
                    maxVal = max(maxVal, max(scores))
                alpha = max(alpha, maxVal)
                s, e = temp_best_move.split()
                move_piece(newboard, s, e, 'Black')
            else:
                temp_best_move = minimaxN(newboard, 'White', N-1, alpha, beta)
                s, e = temp_best_move.split()
                if len(scores) > 0:
                    minVal = min(minVal, min(scores))
                beta = min(beta, minVal)
                move_piece(newboard, s, e, 'White')
        
        # find heuristic value of current state of the board and add to scores
        scores.append(heuristic(newboard, current_player))

        if  beta <= alpha:
            print("broken")
            break
    
    # assuming that White is the max player and Black is the min player
    if current_player == 'White':
        best_move = moves[scores.index(max(scores))]
    else:
        best_move = moves[scores.index(min(scores))]
    
    # return best possible move 
    return best_move

# minimax algorithm wrapper function
def minimax(board, current_player):
    # start with N=1 for testing purposes.
    # if we change to N=2, the alg takes a little while to compute
    N = 2
    alpha = -math.inf
    beta = math.inf
    return minimaxN(board, current_player, N, alpha, beta)