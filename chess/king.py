from piece import Piece

class King(Piece):
    def is_valid_move(self, board, start, end):
        start_row, start_col = board.parse_postition(start)
        end_row, end_col = board.parse_position(end)

        # King pieces can move one square in any direction
        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)
        return (row_diff <= 1 and col_diff <= 1)

    # King pieces can move to any adjacent square
    def possible_destinations(self, board, start):
        start_row, start_col = board.parse_position(start)
        destinations = []

        for row in range(start_row - 1, start_row + 2):
            for col in range(start_col - 1, start_col + 2):
                if row >= 0 and row < 8 and col >= 0 and col < 8:
                    end = self.indices_to_position(row, col)
                    if self.is_valid_move(board, start, end):
                        destinations.append((row, col))

        return destinations