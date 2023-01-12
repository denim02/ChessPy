from pieces import Piece, Pawn, Rook, Knight, Bishop, King, Queen

class ChessGame:
    def __init__(self):
        self.board = self.populate_board()

    def populate_board(self):
        # Place the chess pieces on their starting positions based on the FEN notation
        return ChessGame.parse_FEN("./game_states/init_position.fen")

    @staticmethod
    def parse_FEN(file_path):
        # Parse the FEN notation and return a 2D array of pieces
        with open(file_path) as file:
            string_FEN = file.read()
            ranks = string_FEN.split("/")
            
            board = []

            for i in range(8):
                if ranks[i] == "8":
                    board.append([None] * 8)
                else:
                    board.append([])
                    for j in ranks[i]:
                        if j.isdigit():
                            board[i].extend([None] * int(j))
                        else:
                            board[i].append(Piece.from_notation(j, (i, len(board[i]))))
            
            return board     

    def get_piece(self, position):
        return self.board[position[0]][position[1]]

    def move_piece(self, piece, position):
        piece.position = position