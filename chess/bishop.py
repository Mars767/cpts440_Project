from piece import Piece

class Bishop(Piece):
    def is_valid_move(self, board, start, end):
        start_row, start_col = board.parse_position(start)
        end_row, end_col = board.parse_position(end)
        
        # Bishops must move diagonally, so the absolute differences must be equal
        if abs(end_row - start_row) != abs(end_col - start_col):
            return False
        
        # Determine the direction of movement
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1

        # Check each square along the diagonal path until just before the end square
        current_row = start_row + row_step
        current_col = start_col + col_step
        while current_row != end_row:
            if not board.is_empty((current_row, current_col)):
                return False
            current_row += row_step
            current_col += col_step

        # The end square can be either empty or contain an opponent's piece to capture
        target_piece = board.get_piece(end)
        if target_piece is None or target_piece.color != self.color:
            return True

        return False
