from piece import Piece

class Knight(Piece):
    def is_valid_move(self, board, start, end):
        start_row, start_col = board.parse_position(start)
        end_row, end_col = board.parse_position(end)

        # Knight pieces move in an L shape: 2 squares in one direction and 1 square perpendicular
        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)
        return ((row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2))

    # Knight pieces can move to one of the 8 squares adjacent to their current position in an L shape
    def possible_destinations(self, board, start):
        start_row, start_col = board.parse_position(start)
        destinations = []
        for row_offset, col_offset in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]:
            row = start_row + row_offset
            col = start_col + col_offset
            if 0 <= row < 8 and 0 <= col < 8:
                end = self.indices_to_position(row, col)
                if self.is_valid_move(board, start, end):
                    destinations.append((row, col))
        return destinations