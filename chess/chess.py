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
        row, col = self.parse_position(position)
        return self.grid[row][col] is None

def move_piece(board, start, end):
    piece = board.get_piece(start)
    if piece and piece.is_valid_move(board, start, end):
        board.set_piece(end, piece)
        board.set_piece(start, None)
        return True
    return False


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
        command = input("Enter command (e.g., 'e2 e4' to move or 'quit' to end game): ")

        if command.strip().lower() == 'quit':
            confirm = input("Are you sure you want to quit the game? (yes/no): ")
            if confirm.lower() == 'yes':
                print("Game ended. Thanks for playing!")
                break

        try:
            start, end = command.split()
            if not move_piece(board, start, end):
                print("Invalid move, please try again.")
            else:
                board.print_board()
                current_player = 'Black' if current_player == 'White' else 'White'
        except ValueError:
            print("Please enter a valid command (e.g., 'e2 e4').")

main()
