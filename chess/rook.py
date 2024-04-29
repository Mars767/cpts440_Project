from piece import Piece
class Rook(Piece):
    def is_valid_move(self, board, start, end):
        start_row, start_col = board.parse_position(start)
        end_row, end_col = board.parse_position(end)
        
        # Rooks move either horizontally or vertically
        if start_row != end_row and start_col != end_col:
            return False

        # Determine the direction of the move
        if start_row == end_row:  # Horizontal move
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                # Convert row and column back to position notation
                if not board.is_empty(self.index_to_position(start_row, col)):
                    return False
        else:  # Vertical move
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                # Convert row and column back to position notation
                if not board.is_empty(self.index_to_position(row, start_col)):
                    return False

        # The end square can be either empty or contain an opponent's piece to capture
        target_piece = board.get_piece(end)
        if target_piece is None or target_piece.color != self.color:
            return True

        return False

    def index_to_position(self, row, col):
        # Convert row and column indices back to standard chess notation
        return chr(col + ord('a')) + str(8 - row)
