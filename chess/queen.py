from piece import Piece

class Queen(Piece):
    def is_valid_move(self, board, start, end):
        start_row, start_col = board.parse_position(start)
        end_row, end_col = board.parse_position(end)

        # Check if the end position contains a piece of the same color
        if board.get_piece(end) is not None and board.get_piece(end).color == self.color:
            return False

        # Queen pieces can move horizontally, vertically, or diagonally
        if start_row == end_row or start_col == end_col or abs(end_row - start_row) == abs(end_col - start_col):
            # Checking if any pieces are blocking the path
            row_step = 1 if end_row > start_row else -1 if end_row < start_row else 0
            col_step = 1 if end_col > start_col else -1 if end_col < start_col else 0
            row, col = start_row + row_step, start_col + col_step
            while row != end_row or col != end_col:
                if not board.is_empty(self.indices_to_position(row, col)):
                    return False
                row += row_step
                col += col_step
            return True
        return False

    # Queen pieces can move to any square along a horizontal, vertical, or diagonal line
    def possible_destinations(self, board, start):
        start_row, start_col = board.parse_position(start)
        destinations = []
        for row in range(8):
            for col in range(8):
                if row != start_row or col != start_col:
                    end = self.indices_to_position(row, col)
                    if self.is_valid_move(board, start, end):
                        destinations.append((row, col))
        return destinations