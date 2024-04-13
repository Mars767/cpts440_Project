class Piece:
    def __init__(self, color):
        self.color = color
    
    def __str__(self):
        return f"{self.__class__.__name__[0]}({self.color})"

    def is_valid_move(self, board, start, end):
        raise NotImplementedError("Each piece must implement this method.")