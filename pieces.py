class Piece:
    def __init__(self, name, value, color, position):
        self.name = name
        self.value = value
        self.color = color
        self.image_path = f"./assets/{color}-{name}.png"
        self.position = position
        self.valid_moves = []
        
class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(name="Pawn", value=1, position=position, color=color)
        
    def get_valid_moves(self):
        if self.color == "white":
            self.valid_moves.append((self.position[0] - 1, self.position[1]))
            if self.position[0] == 6:
                self.valid_moves.append((self.position[0] - 2, self.position[1]))
        else:
            self.valid_moves.append((self.position[0] + 1, self.position[1]))
            if self.position[0] == 1:
                self.valid_moves.append((self.position[0] + 2, self.position[1]))
        return self.valid_moves

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(name="Rook", value=5, position=position, color=color)
        
    def get_valid_moves(self):
        for i in range(8):
            self.valid_moves.append((self.position[0], i))
            self.valid_moves.append((i, self.position[1]))
        return self.valid_moves

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(name="Rook", value=3, position=position, color=color)

    def get_valid_moves(self):
        self.valid_moves.append((self.position[0] - 2, self.position[1] - 1))
        self.valid_moves.append((self.position[0] - 2, self.position[1] + 1))
        self.valid_moves.append((self.position[0] - 1, self.position[1] - 2))
        self.valid_moves.append((self.position[0] - 1, self.position[1] + 2))
        self.valid_moves.append((self.position[0] + 1, self.position[1] - 2))
        self.valid_moves.append((self.position[0] + 1, self.position[1] + 2))
        self.valid_moves.append((self.position[0] + 2, self.position[1] - 1))
        self.valid_moves.append((self.position[0] + 2, self.position[1] + 1))
        return self.valid_moves

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(name="Bishop", value=3, position=position, color=color)
        
    def get_valid_moves(self):
        for i in range(8):
            self.valid_moves.append((self.position[0] - i, self.position[1] - i))
            self.valid_moves.append((self.position[0] + i, self.position[1] - i))
            self.valid_moves.append((self.position[0] - i, self.position[1] + i))
            self.valid_moves.append((self.position[0] + i, self.position[1] + i))
        return self.valid_moves

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(name="Queen", value=9, position=position, color=color)
        
    def get_valid_moves(self):
        for i in range(8):
            self.valid_moves.append((self.position[0], i))
            self.valid_moves.append((i, self.position[1]))
            self.valid_moves.append((self.position[0] - i, self.position[1] - i))
            self.valid_moves.append((self.position[0] + i, self.position[1] - i))
            self.valid_moves.append((self.position[0] - i, self.position[1] + i))
            self.valid_moves.append((self.position[0] + i, self.position[1] + i))
        return self.valid_moves

class King(Piece):
    def __init__(self, color, position):
        super().__init__(name="King", value=100, position=position, color=color)
        
    def get_valid_moves(self):
        self.valid_moves.append((self.position[0] - 1, self.position[1]))
        self.valid_moves.append((self.position[0] + 1, self.position[1]))
        self.valid_moves.append((self.position[0], self.position[1] - 1))
        self.valid_moves.append((self.position[0], self.position[1] + 1))
        self.valid_moves.append((self.position[0] - 1, self.position[1] - 1))
        self.valid_moves.append((self.position[0] + 1, self.position[1] - 1))
        self.valid_moves.append((self.position[0] - 1, self.position[1] + 1))
        self.valid_moves.append((self.position[0] + 1, self.position[1] + 1))
        return self.valid_moves