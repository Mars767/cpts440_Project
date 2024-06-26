from pawn import Pawn
from piece import Piece
from bishop import Bishop
from knight import knight
from rook import Rook
from king import King
from queen import Queen
from minimax import minimax
import copy
import random

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()

    def setup_pieces(self):
        # Place pawns
        for i in range(8):
            self.grid[1][i] = Pawn('W')
            self.grid[6][i] = Pawn('B')
        # Place rooks
        self.grid[0][0] = Rook('W')
        self.grid[0][7] = Rook('W')
        self.grid[7][0] = Rook('B')
        self.grid[7][7] = Rook('B')

        # Place knights
        self.grid[0][1] = knight('W')
        self.grid[0][6] = knight('W')
        self.grid[7][1] = knight('B')
        self.grid[7][6] = knight('B')

        # Place bishops
        self.grid[0][2] = Bishop('W')
        self.grid[0][5] = Bishop('W')
        self.grid[7][2] = Bishop('B')
        self.grid[7][5] = Bishop('B')

        # Place queens
        self.grid[0][3] = Queen('W')
        self.grid[7][3] = Queen('B')

        # Place kings
        self.grid[0][4] = King('W')
        self.grid[7][4] = King('B')

    def print_board(self):
        # Print column labels
        print('   ' + '    '.join([chr(c) for c in range(ord('a'), ord('h')+1)]))
        print('  +' + '-----'*8 + '+')
        # Print rows
        for i, row in enumerate(self.grid):
            # Row number
            print(f'{8-i} |', end='')
            for piece in row:
                print(f"{str(piece) if piece else ' .. ':3}", end=' ')
            print('|')
        print('   +' + '-----'*8 + '+')
        print('   ' + '    '.join([chr(c) for c in range(ord('a'), ord('h')+1)]))
    def get_piece(self, position):
        row, col = self.parse_position(position)
        return self.grid[row][col]

    def set_piece(self, position, piece):
        row, col = self.parse_position(position)
        self.grid[row][col] = piece

    def parse_position(self, position):
        row = 8 - int(position[1])
        col = ord(position[0]) - ord('a')
        return row, col

    def is_empty(self, position):
        #print(f"is empty - position = {position}")
        if (type(position) == str):
            row, col = self.parse_position(position)
        else:
            row, col = position[0], position[1]
        return self.grid[row][col] is None

def move_piece(board, start, end, current_player):
    piece = board.get_piece(start)
    if piece and piece.is_valid_move(board, start, end) and piece.color == current_player[0]:
        board.set_piece(end, piece)
        board.set_piece(start, None)
        return True
    return False

def is_check(board, current_player):

    #check to see if king still exists, to avoid the game continuing if they do not move out of check
    kingExists = False
    for j in range(len(board.grid[0])):
        for i in range(len(board.grid)):
            piece = board.grid[i][j]
            if isinstance(piece, King):
                if piece.color == current_player[0]:
                    kingExists = True
    if kingExists == False:
        return True
    
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


def is_checkmate(board, current_player):
    # used for checkmate
    possible_moves = set()

    #check to see if king still exists, to avoid the game continuing if they do not move out of check
    kingExists = False
    for j in range(len(board.grid[0])):
        for i in range(len(board.grid)):
            piece = board.grid[i][j]
            if isinstance(piece, King):
                if piece.color == current_player[0]:
                    kingExists = True
    if kingExists == False:
        return True
    
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

def main():
    board = Board()
    board.print_board()
    coin = random.randint(0, 1)
    if coin == 0:
        user_player = 'White'
    else:
        user_player = 'Black'
    current_player = 'White'
    print(f"You are playing as the {user_player} player!")
    
    while True:
        print(f"{current_player}'s turn.")
        # check for check
        if (is_check(board, current_player)):
            # check for checkmate
            if (is_checkmate(board, current_player)):
                print(f"{current_player} is in checkmate.")
                if current_player == 'White':
                    print("Black wins! Game ended. Thanks for playing!")
                    break
                else:
                    print("White wins! Game ended. Thanks for playing!")
                    break
            else:
                print(f"{current_player} is in check.")
        # minimax's turn!
        if current_player != user_player:
            # get a move from the algorithm, move the piece, change current player, and continue
            minimax_move = minimax(board, current_player)
            s, e = minimax_move.split()
            move_piece(board, s, e, current_player)
            board.print_board()
            print(f"Minimax made move -> {minimax_move}")
            current_player = 'Black' if current_player == 'White' else 'White'
        # user's turn!
        else:
            # get a move from the user, move the piece, change current player
            command = input("Enter command (e.g., 'e2 e4' to move or 'quit' to end game): ")

            if command.strip().lower() == 'quit':
                confirm = input("Are you sure you want to quit the game? (yes/no): ")
                if confirm.lower() == 'yes':
                    print("Game ended. Thanks for playing!")
                    break

            try:
                start, end = command.split()
                if not move_piece(board, start, end, current_player):
                    print("Invalid move, please try again.")
                else:
                    board.print_board()
                    current_player = 'Black' if current_player == 'White' else 'White'
            except ValueError:
                print("Please enter a valid command (e.g., 'e2 e4').")

main()
