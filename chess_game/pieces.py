"""
pieces.py
This module contains the Piece, Pawn, Rook, Knight, Bishop, Queen, King classes.
These classes are used to represent pieces in a chess game. Each class has properties
like name, value, color, position, legal_moves and methods generate_possible_moves,
refresh_legal_moves and generate_legal_moves etc. They are also used to manage algebraic
notation of the chess pieces and and generate possible moves for each piece.
"""
import chess_game.chess_logic as chess_logic
from chess_game.constants import *


class Piece:
    """
    Piece:
    This is a class for representing a chess piece.
    It is initialized with properties like name, value, color and position.
    It also has properties like legal_moves and methods like generate_possible_moves,
    refresh_legal_moves and generate_legal_moves etc. It also has static methods to create
    a piece from algebraic notation and convert a piece to algebraic notation.
    """

    def __init__(self, name, value, color, position):
        """
        Initializes the piece with properties like name, value, color, position.

        Parameters:
        name (str): the name of the piece
        value (int): the value of the piece
        color (str): the color of the piece
        position (tuple): the position of the piece in (x, y) format,
        where x is the row and y is the column.
        """
        self.name = name
        self.value = value
        self.__color = color
        self.image = None
        self.__position = position
        self.__coords = ()
        self.__legal_moves = set()
        self.refresh_coords()

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        if color not in ("white", "black"):
            raise ValueError("Invalid color.")
        else:
            self.__color = color

    @property
    def coords(self):
        return self.__coords

    @coords.setter
    def coords(self, coords):
        self.__coords = coords

    def refresh_coords(self):
        """
        Determines the coordinates of the piece.
        """
        self.__coords = self.position[1] * SQUARE_SIZE, self.position[0] * SQUARE_SIZE

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        if not (0 <= position[0] <= 7 and 0 <= position[1] <= 7):
            raise ValueError("Invalid position.")
        else:
            self.__position = position
            self.refresh_coords()

    @property
    def legal_moves(self):
        return self.__legal_moves

    def generate_possible_moves(self, board):
        """
        Generates the possible moves for the piece.

        Parameters:
        board (Board): the board on which the piece is placed."""
        return set()

    def refresh_legal_moves(self, board):
        """
        Refreshes the legal moves for the piece.

        Parameters:
        board (Board): the board on which the piece is placed."""
        self.__legal_moves = self.generate_legal_moves(board)

    def generate_legal_moves(self, board):
        """
        Generates the legal moves for the piece.

        Parameters:
        board (Board): the board on which the piece is placed."""
        possible_moves = self.generate_possible_moves(board)
        legal_moves = {
            move
            for move in possible_moves
            if move != self.position and chess_logic.is_legal_move(board, self, move)
        }
        return legal_moves

    # Define a constructor to create piece from algebraic notation
    @staticmethod
    def from_algebraic_notation(algebraic_notation, position):
        """
        Creates a piece from algebraic notation.

        Parameters:
        algebraic_notation (str): the algebraic notation of the piece.
        position (tuple): the position of the piece in (x, y) format,
        where x is the row and y is the column."""
        name = algebraic_notation.lower()
        color = "black" if name == algebraic_notation else "white"

        match name:
            case "p":
                return Pawn(color, position)
            case "r":
                return Rook(color, position)
            case "n":
                return Knight(color, position)
            case "b":
                return Bishop(color, position)
            case "q":
                return Queen(color, position)
            case "k":
                return King(color, position)
            case _:
                raise ValueError("Impossible algebraic notation")

    def to_algebraic_notation(self):
        """
        Converts a piece to algebraic notation."""
        if self.name == "Knight":
            return "n" if self.color == "black" else "N"
        return self.name[0].lower() if self.color == "black" else self.name[0].upper()

    def __repr__(self):
        """
        Returns a string representation of the piece."""
        return f"{self.color.title()} {self.name}"


class Pawn(Piece):
    """
    Pawn:
    This is a class for representing a Pawn piece.
    It inherits from the Piece class and overrides the generate_possible_moves method.
    It also has properties like name, value, color and position, that are inherited
    from the Piece class.
    """

    def __init__(self, color, position):
        super().__init__(name="Pawn", value=1, position=position, color=color)

    def generate_possible_moves(self, board):
        """
        Generates the possible moves for the pawn.

        Parameters:
        board (Board): the board on which the piece is placed.
        """
        possible_moves = set()
        if self.color == "white":
            possible_moves.add((self.position[0] - 1, self.position[1]))
            if (
                self.position[0] == 6
                and board.get_piece_at_square((self.position[0] - 2, self.position[1]))
                is None
            ):
                possible_moves.add((self.position[0] - 2, self.position[1]))
            if (
                self.position[0] + 1 < 8
                and self.position[1] - 1 >= 0
                and self.position[0] - 1 >= 0
                and self.position[1] + 1 < 8
            ):
                if board.is_square_occupied(
                    (self.position[0] - 1, self.position[1] - 1)
                ):
                    possible_moves.add((self.position[0] - 1, self.position[1] - 1))
                if board.is_square_occupied(
                    (self.position[0] - 1, self.position[1] + 1)
                ):
                    possible_moves.add((self.position[0] - 1, self.position[1] + 1))
                if board.is_square_occupied((self.position[0] - 1, self.position[1])):
                    possible_moves.remove((self.position[0] - 1, self.position[1]))

        else:
            possible_moves.add((self.position[0] + 1, self.position[1]))
            if (
                self.position[0] == 1
                and board.get_piece_at_square((self.position[0] + 2, self.position[1]))
                is None
            ):
                possible_moves.add((self.position[0] + 2, self.position[1]))
            if (
                self.position[0] + 1 < 8
                and self.position[1] - 1 >= 0
                and self.position[0] - 1 >= 0
                and self.position[1] + 1 < 8
            ):
                if board.is_square_occupied(
                    (self.position[0] + 1, self.position[1] - 1)
                ):
                    possible_moves.add((self.position[0] + 1, self.position[1] - 1))
                if board.is_square_occupied(
                    (self.position[0] + 1, self.position[1] + 1)
                ):
                    possible_moves.add((self.position[0] + 1, self.position[1] + 1))
                if board.is_square_occupied((self.position[0] + 1, self.position[1])):
                    possible_moves.remove((self.position[0] + 1, self.position[1]))

        return possible_moves


class Rook(Piece):
    """
    Rook:
    This is a class for representing a Rook piece.
    It inherits from the Piece class and overrides the generate_possible_moves method.
    It also has properties like name, value, color and position, that are inherited
    from the Piece class.
    """

    def __init__(self, color, position):
        super().__init__(name="Rook", value=5, position=position, color=color)
        self.has_moved = False

    def generate_possible_moves(self, board):
        """
        Generates the possible moves for the rook.

        Parameters:
        board (Board): the board on which the piece is placed.
        """
        possible_moves = set()
        x_current, y_current = self.position  # unpack the current position of the rook

        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x_new, y_new = x_current + i, y_current + j
            while 0 <= x_new < 8 and 0 <= y_new < 8:
                possible_moves.add((x_new, y_new))
                x_new += i
                y_new += j
        return possible_moves


class Knight(Piece):
    """
    Knight:
    This is a class for representing a Knight piece.
    It inherits from the Piece class and overrides the generate_possible_moves method.
    It also has properties like name, value, color and position, that are inherited
    from the Piece class.
    """

    def __init__(self, color, position):
        super().__init__(name="Knight", value=3, position=position, color=color)

    def generate_possible_moves(self, board):
        """
        Generates the possible moves for the knight.

        Parameters:
        board (Board): the board on which the piece is placed.
        """
        possible_moves = set()
        for i in range(8):
            for j in range(8):
                if (
                    abs(i - self.position[0]) + abs(j - self.position[1]) == 3
                    and i != self.position[0]
                    and j != self.position[1]
                ):
                    possible_moves.add((i, j))
        return possible_moves


class Bishop(Piece):
    """
    Bishop:
    This is a class for representing a Bishop piece.
    It inherits from the Piece class and overrides the generate_possible_moves method.
    It also has properties like name, value, color and position, that are inherited
    from the Piece class.
    """

    def __init__(self, color, position):
        super().__init__(name="Bishop", value=3, position=position, color=color)

    def generate_possible_moves(self, board):
        """
        Generates the possible moves for the bishop.

        Parameters:
        board (Board): the board on which the piece is placed.
        """
        possible_moves = set()
        (
            x_current,
            y_current,
        ) = self.position  # unpack the current position of the bishop
        for i, j in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x_new, y_new = x_current + i, y_current + j
            while 0 <= x_new < 8 and 0 <= y_new < 8:
                possible_moves.add((x_new, y_new))
                x_new += i
                y_new += j
        return possible_moves


class Queen(Piece):
    """
    Queen:
    This is a class for representing a Queen piece.
    It inherits from the Piece class and overrides the generate_possible_moves method.
    It also has properties like name, value, color and position, that are inherited
    from the Piece class.
    """

    def __init__(self, color, position):
        super().__init__(name="Queen", value=9, position=position, color=color)

    def generate_possible_moves(self, board):
        """
        Generates the possible moves for the queen.

        Parameters:
        board (Board): the board on which the piece is placed.
        """
        possible_moves = set()
        x_current, y_current = self.position  # unpack the current position of the queen
        # Diagonal moves
        for i, j in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x_new, y_new = x_current + i, y_current + j
            while 0 <= x_new < 8 and 0 <= y_new < 8:
                possible_moves.add((x_new, y_new))
                x_new += i
                y_new += j

        # Horizontal and vertical moves
        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x_new, y_new = x_current + i, y_current + j
            while 0 <= x_new < 8 and 0 <= y_new < 8:
                possible_moves.add((x_new, y_new))
                x_new += i
                y_new += j
        return possible_moves


class King(Piece):
    """
    King:
    This is a class for representing a King piece.
    It inherits from the Piece class and overrides the generate_possible_moves method.
    It also has properties like name, value, color and position, that are inherited
    from the Piece class.
    """

    def __init__(self, color, position):
        super().__init__(name="King", value=100, position=position, color=color)
        self.has_moved = False

    def generate_possible_moves(self, board):
        """
        Generates the possible moves for the king.

        Parameters:
        board (Board): the board on which the piece is placed.
        """
        possible_moves = set()
        x_current, y_current = self.position  # unpack the current position of the king
        for i, j in [
            (1, 1),
            (1, 0),
            (1, -1),
            (0, 1),
            (0, -1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
        ]:
            x_new, y_new = x_current + i, y_current + j
            if (i, j) != (0, 0) and 0 <= x_new < 8 and 0 <= y_new < 8:
                possible_moves.add((x_new, y_new))

        # Castling - check whether the path is blocked or not (use is_path_blocked), whether any squares in the path are under attack,
        # whether the king has moved or not, whether the rook has moved or not
        # and whether the king is under attack or not
        if not self.has_moved:
            if self.color == "black":
                if not board.is_path_blocked((0, 4), (0, 0)):
                    if not board.is_square_attacked((0, 4), "black"):
                        if not board.is_square_attacked((0, 3), "black"):
                            if not board.is_square_attacked((0, 2), "black"):
                                possible_moves.add((0, 2))
                if not board.is_path_blocked((0, 4), (0, 7)):
                    if not board.is_square_attacked((0, 4), "black"):
                        if not board.is_square_attacked((0, 5), "black"):
                            if not board.is_square_attacked((0, 6), "black"):
                                possible_moves.add((0, 6))
            else:
                if not board.is_path_blocked((7, 4), (7, 0)):
                    if not board.is_square_attacked((7, 4), "white"):
                        if not board.is_square_attacked((7, 3), "white"):
                            if not board.is_square_attacked((7, 2), "white"):
                                possible_moves.add((7, 2))
                if not board.is_path_blocked((7, 4), (7, 7)):
                    if not board.is_square_attacked((7, 4), "white"):
                        if not board.is_square_attacked((7, 5), "white"):
                            if not board.is_square_attacked((7, 6), "white"):
                                possible_moves.add((7, 6))

        return possible_moves
