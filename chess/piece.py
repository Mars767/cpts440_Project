class Piece:
    def __init__(self, color):
        self.color = color
    
    def __str__(self):
        return f"{self.__class__.__name__[0]}({self.color})"

    def is_valid_move(self, board, start, end):
        raise NotImplementedError("Each piece must implement this method.")
    
    # used to convert position in 2D array to spot on chess board
    def indices_to_position(self, i, j):
        # convert row index to letter (a-h)
        column_label = chr(ord('a') + j)
        # convert column index to number (1-8)
        row_number = 8 - i
        # combine the letter and number to form the position
        position = f"{column_label}{row_number}"
        
        return position
    
    # used to convert spot on chess board to position in 2D array (DOES THE SAME THING AS PARSE POSITION)
    def position_to_indices(self, position):
        # ensure the position is valid
        if len(position) != 2:
            print("Invalid position format. Expected two characters (e.g., 'a1').")
        
        column_label, row_number = position[0], position[1]
        # convert column letter to index (0-7)
        j = ord(column_label.lower()) - ord('a')
        # convert row number to index (0-7)
        i = 8 - int(row_number)
        
        return i, j
    
    # used to get indices of all possible destinations
    def possible_destinations(self, board, start):
        destinations = []
        # iterate over grid
        for n in range(len(board.grid[0])):
            for m in range(len(board.grid)):
                end = self.indices_to_position(m, n)
                # add to the destinations if it is a valid move
                if self.is_valid_move(board, start, end):
                    # convert to indices for indexing the array
                    x, y = self.position_to_indices(end)
                    destinations.append((x, y))
        
        return destinations