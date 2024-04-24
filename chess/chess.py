from pawn import Pawn
from piece import Piece
from bishop import Bishop
from rook import Rook

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
        self.grid[0][1] = Knight('W')
        self.grid[0][6] = Knight('W')
        self.grid[7][1] = Knight('B')
        self.grid[7][6] = Knight('B')

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
            # if so, continue
            else:
                position = piece.indices_to_position(i, j)
                # get all possible squares the piece could move to
                possible_destinations = piece.possible_destinations(board, position)
                for destination in possible_destinations:
                    # if the other player's king is reachable, return true
                    #print(f"Position {piece.indices_to_position(destination[0], destination[1])}, type {type(board.grid[destination[0]][destination[1]])}" )
                    if type(board.grid[destination[0]][destination[1]]) == King and board.grid[destination[0]][destination[1]].color == current_player[0]:
                        return True
    # otherwise, return false
    return False


def is_checkmate(board):
    # to be implemented
    # IDEA: FIND ALL POSSIBLE BOARD CONFIGURATIONS WITH THE MOVES YOU CAN CURRENTLY TAKE.
    # THEN RUN IS_CHECK ON ALL OF THEM. IF ALL CONFIGURATIONS ARE IN CHECK, RETURN TRUE, IF NOT, FALSE
    pass

class Queen(Piece):
    def is_valid_move(self, board, start, end):
       pass
class King(Piece):
    def is_valid_move(self, board, start, end):
       pass
class Knight(Piece):
    def is_valid_move(self, board, start, end):
       pass

def main():
    board = Board()
    board.print_board()
    current_player = 'White'
    
    while True:
        print(f"{current_player}'s turn.")
        if (is_check(board, current_player)):
            # check for checkmate here
            if (False):
                print(f"{current_player} is in checkmate.")
                if current_player == 'White':
                    print("Black wins! Game ended. Thanks for playing!")
                    break
                else:
                    print("White wins! Game ended. Thanks for playing!")
                    break
            else:
                print(f"{current_player} is in check.")
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
