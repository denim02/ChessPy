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

    def move_piece(self, original_position, new_position):
        piece = self.board[original_position[0]][original_position[1]]
        piece.position = new_position
        piece.generate_valid_moves()
        self.board[original_position[0]][original_position[1]] = None
        self.board[new_position[0]][new_position[1]] = piece

    def is_valid_move(self, piece_position, new_position):
        return new_position in self.board[piece_position[0]][piece_position[1]].valid_moves
