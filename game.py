from pieces import Pawn, Rook, Knight, Bishop, King, Queen

class ChessGame:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.populate_board()

    def populate_board(self):
        # Place the chess pieces on their starting positions
        for col in range(8):
            self.board[1][col] = Pawn("black", (1, col))
            self.board[6][col] = Pawn("white", (6, col))
        self.board[0][0] = Rook("black", (0, 0))
        self.board[0][7] = Rook("black", (0, 7))
        self.board[7][0] = Rook("white", (7, 0))
        self.board[7][7] = Rook("white", (7, 7))
        self.board[0][1] = Knight("black", (0, 1))
        self.board[0][6] = Knight("black", (0, 6))
        self.board[7][1] = Knight("white", (7, 1))
        self.board[7][6] = Knight("white", (7, 6))
        self.board[0][2] = Bishop("black", (0, 2))
        self.board[0][5] = Bishop("black", (0, 5))
        self.board[7][2] = Bishop("white", (7, 2))
        self.board[7][5] = Bishop("white", (7, 5))
        self.board[0][3] = Queen("black", (0, 3))
        self.board[7][3] = Queen("white", (7, 3))
        self.board[0][4] = King("black", (0, 4))
        self.board[7][4] = King("white", (7, 4))

    def get_piece(self, position):
        return self.board[position[0]][position[1]]
