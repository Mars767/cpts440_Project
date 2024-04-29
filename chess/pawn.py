from piece import Piece

class Pawn(Piece):
    def is_valid_move(self, board, start, end):
        start_row, start_col = board.parse_position(start)
        end_row, end_col = board.parse_position(end)
        direction = 1 if self.color == 'W' else -1
        
        # Diagonal capture
        if abs(start_col - end_col) == 1 and abs(start_row - end_row) == 1:
            #print("attempt diagonal capture")
            if (self.color == 'W' and end_row > start_row or self.color == 'B' and end_row < start_row):
                target_piece = board.get_piece(end)
                return target_piece is not None and target_piece.color != self.color
        # Move forward one space
        if start_col == end_col and abs(start_row - end_row) == 1:
            if self.color == 'W' and end_row > start_row or self.color == 'B' and end_row < start_row:
                return board.is_empty(end)

        # Move forward two spaces from the initial position
        if start_col == end_col and abs(start_row - end_row) == 2:
            if (self.color == 'W' and start_row == 1 and end_row == 3) or (self.color == 'B' and start_row == 6 and end_row == 4):
                # Check that both the square directly in front and the destination square are empty
                intermediate_pos = chr(start_col + ord('a')) + str(8 - (start_row + direction))
                return board.is_empty(intermediate_pos) and board.is_empty(end)

      

        return False
