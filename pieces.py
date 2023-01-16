import chess_logic

# No negative indices permitted for positions in generate_possible_moves() methods

class Piece:
    def __init__(self, name, value, color, position):
        self.name = name
        self.value = value
        self.color = color
        self.image = None
        self.position = position
        self.legal_moves = []

    def generate_possible_moves(self, board):
        pass

    def refresh_legal_moves(self, board):
        self.legal_moves = self.generate_legal_moves(board)

    def generate_legal_moves(self, board):
        possible_moves = self.generate_possible_moves(board)
        legal_moves = [move for move in possible_moves if move != self.position and chess_logic.is_legal_move(board, self, move)]
        return legal_moves

    # Define a constructor to create piece from algebraic notation
    @staticmethod
    def from_algebraic_notation(algebraic_notation, position):
        name = algebraic_notation.lower()
        color = "black" if name == algebraic_notation else "white"

        if name == "p":
            return Pawn(color, position)
        elif name == "r":
            return Rook(color, position)
        elif name == "n":
            return Knight(color, position)
        elif name == "b":
            return Bishop(color, position)
        elif name == "q":
            return Queen(color, position)
        elif name == "k":
            return King(color, position)
        else:
            raise ValueError("Impossible algebraic notation")
    
    def to_algebraic_notation(self):
        if self.name == "Knight":
            return "n" if self.color == "black" else "N"
        else:
            return self.name[0].lower() if self.color == "black" else self.name[0].upper()

    def __repr__(self):
        return f"{self.color.title()} {self.name}"
        


class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(name="Pawn", value=1, position=position, color=color)
        
    def generate_possible_moves(self, board):
        possible_moves = []
        if self.color == "white":
            possible_moves.append((self.position[0] - 1, self.position[1]))
            if self.position[0] == 6:
                possible_moves.append((self.position[0] - 2, self.position[1]))
            if self.position[0] + 1 < 8 and self.position[1] - 1 >= 0 and self.position[0] - 1 >= 0 and self.position[1] + 1 < 8:
                if board.is_square_occupied((self.position[0] - 1, self.position[1] - 1)):
                    possible_moves.append((self.position[0] - 1, self.position[1] - 1))
                if board.is_square_occupied((self.position[0] - 1, self.position[1] + 1)):
                    possible_moves.append((self.position[0] - 1, self.position[1] + 1))
            
        else:
            possible_moves.append((self.position[0] + 1, self.position[1]))
            if self.position[0] == 1:
                possible_moves.append((self.position[0] + 2, self.position[1]))
            if self.position[0] + 1 < 8 and self.position[1] - 1 >= 0 and self.position[0] - 1 >= 0 and self.position[1] + 1 < 8:
                if board.is_square_occupied((self.position[0] + 1, self.position[1] - 1)):
                    possible_moves.append((self.position[0] + 1, self.position[1] - 1))
                if board.is_square_occupied((self.position[0] + 1, self.position[1] + 1)):
                    possible_moves.append((self.position[0] + 1, self.position[1] + 1))
        return possible_moves

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(name="Rook", value=5, position=position, color=color)
        
    def generate_possible_moves(self, board):
        possible_moves = []
        x,y = self.position  # unpack the current position of the rook

        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x_, y_ = x + i, y + j
            while 0 <= x_ < 8 and 0 <= y_ < 8:
                possible_moves.append((x_, y_))
                x_ += i
                y_ += j
        return possible_moves

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(name="Knight", value=3, position=position, color=color)

    def generate_possible_moves(self, board):
        possible_moves = []
        for i in range(8):
            for j in range(8):
                if abs(i - self.position[0]) + abs(j - self.position[1]) == 3 and i != self.position[0] and j != self.position[1]:
                    possible_moves.append((i, j))
        return possible_moves

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(name="Bishop", value=3, position=position, color=color)
        
    def generate_possible_moves(self, board):
        possible_moves = []
        x, y = self.position  # unpack the current position of the bishop
        for i, j in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x_, y_ = x+i, y+j
            while 0 <= x_ < 8 and 0 <= y_ < 8:
                possible_moves.append((x_, y_))
                x_ += i
                y_ += j
        return possible_moves

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(name="Queen", value=9, position=position, color=color)
        
    def generate_possible_moves(self, board):
        possible_moves = []
        x, y = self.position  # unpack the current position of the queen
        # Diagonal moves
        for i, j in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x_, y_ = x+i, y+j
            while 0 <= x_ < 8 and 0 <= y_ < 8:
                possible_moves.append((x_, y_))
                x_ += i
                y_ += j

        # Horizontal and vertical moves
        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x_, y_ = x+i, y+j
            while 0 <= x_ < 8 and 0 <= y_ < 8:
                possible_moves.append((x_, y_))
                x_ += i
                y_ += j
        return possible_moves

class King(Piece):
    def __init__(self, color, position):
        super().__init__(name="King", value=100, position=position, color=color)
        
    def generate_possible_moves(self, board):
        possible_moves = []
        for i in range(8):
            for j in range(8):
                if abs(i - self.position[0]) + abs(j - self.position[1]) == 1 and i != self.position[0] and j != self.position[1]:
                    possible_moves.append((i, j))

        return possible_moves