from PIL import ImageTk, Image

class Piece:
    def __init__(self, name, value, color, position):
        self.name = name
        self.value = value
        self.color = color
        self.image = None
        self.position = position
        self.valid_moves = []
        self.generate_valid_moves()

    def generate_valid_moves(self):
        pass

    # Define a constructor to create piece from algebraic notation
    @classmethod
    def from_notation(cls, algebraic_notation, position):
        name = algebraic_notation.lower()
        color = "white" if name == algebraic_notation else "black"

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
            raise ValueError("Invalid algebraic notation")

    def __repr__(self):
        return f"{self.color.title()} {self.name}"
        


class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(name="Pawn", value=1, position=position, color=color)
        
    def generate_valid_moves(self):
        self.valid_moves.clear()
        if self.color == "white":
            self.valid_moves.append((self.position[0] - 1, self.position[1]))
            if self.position[0] == 6:
                self.valid_moves.append((self.position[0] - 2, self.position[1]))
        else:
            self.valid_moves.append((self.position[0] + 1, self.position[1]))
            if self.position[0] == 1:
                self.valid_moves.append((self.position[0] + 2, self.position[1]))

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(name="Rook", value=5, position=position, color=color)
        
    def generate_valid_moves(self):
        self.valid_moves.clear()
        for i in range(8):
            self.valid_moves.append((self.position[0], i))
            self.valid_moves.append((i, self.position[1]))

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(name="Knight", value=3, position=position, color=color)

    def generate_valid_moves(self):
        self.valid_moves.clear()
        self.valid_moves.append((self.position[0] - 2, self.position[1] - 1))
        self.valid_moves.append((self.position[0] - 2, self.position[1] + 1))
        self.valid_moves.append((self.position[0] - 1, self.position[1] - 2))
        self.valid_moves.append((self.position[0] - 1, self.position[1] + 2))
        self.valid_moves.append((self.position[0] + 1, self.position[1] - 2))
        self.valid_moves.append((self.position[0] + 1, self.position[1] + 2))
        self.valid_moves.append((self.position[0] + 2, self.position[1] - 1))
        self.valid_moves.append((self.position[0] + 2, self.position[1] + 1))

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(name="Bishop", value=3, position=position, color=color)
        
    def generate_valid_moves(self):
        self.valid_moves.clear()
        for i in range(8):
            self.valid_moves.append((self.position[0] - i, self.position[1] - i))
            self.valid_moves.append((self.position[0] + i, self.position[1] - i))
            self.valid_moves.append((self.position[0] - i, self.position[1] + i))
            self.valid_moves.append((self.position[0] + i, self.position[1] + i))

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(name="Queen", value=9, position=position, color=color)
        
    def generate_valid_moves(self):
        self.valid_moves.clear()
        for i in range(8):
            self.valid_moves.append((self.position[0], i))
            self.valid_moves.append((i, self.position[1]))
            self.valid_moves.append((self.position[0] - i, self.position[1] - i))
            self.valid_moves.append((self.position[0] + i, self.position[1] - i))
            self.valid_moves.append((self.position[0] - i, self.position[1] + i))
            self.valid_moves.append((self.position[0] + i, self.position[1] + i))

class King(Piece):
    def __init__(self, color, position):
        super().__init__(name="King", value=100, position=position, color=color)
        
    def generate_valid_moves(self):
        self.valid_moves.clear()
        self.valid_moves.append((self.position[0] - 1, self.position[1]))
        self.valid_moves.append((self.position[0] + 1, self.position[1]))
        self.valid_moves.append((self.position[0], self.position[1] - 1))
        self.valid_moves.append((self.position[0], self.position[1] + 1))
        self.valid_moves.append((self.position[0] - 1, self.position[1] - 1))
        self.valid_moves.append((self.position[0] + 1, self.position[1] - 1))
        self.valid_moves.append((self.position[0] - 1, self.position[1] + 1))
        self.valid_moves.append((self.position[0] + 1, self.position[1] + 1))