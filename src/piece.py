

class Piece():
    # F = flat, S = standing, C = capstone
    # 1 = White, 0 = Black
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color