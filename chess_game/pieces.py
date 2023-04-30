"""The pieces module contains the Piece class and its subclasses, which represent the pieces of the chess game.

Each class contains the same data fields and methods, but with different implementations. 
The only abstract method is _generate_possible_moves, which defines how to generate the possible moves for 
a piece, and, therefore, how each piece is supposed to move according to the rules of chess. It is thus 
implemented differently for each subclass.
"""
from chess_game import constants, chess_logic
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

# FOR TYPE HINTS ONLY
# The following import is only used for type checking to avoid circular imports.
if TYPE_CHECKING:
    from chess_game.board import Board


class Piece(ABC):
    """Abstract class that represents a piece of the chess game."""

    def __init__(self, name: str, value: int, color: str, position: tuple) -> None:
        self.name = name
        self.value = value
        self.__color = color
        self.image = None
        self.__position = position
        self.__coords = ()
        self.has_moved = False
        self.__legal_moves = set()
        self.__refresh_coords()

    @property
    def color(self) -> str:
        """The color of the piece: "white" or "black"."""
        return self.__color

    @color.setter
    def color(self, color: str) -> None:
        if color not in ("white", "black"):
            raise ValueError("Invalid color.")
        else:
            self.__color = color

    @property
    def coords(self) -> tuple:
        """The coordinates of the piece in (x, y) format, where x is the horizontal
        coordinate and y is the vertical one."""
        return self.__coords

    @coords.setter
    def coords(self, coords: tuple) -> None:
        self.__coords = coords

    def __refresh_coords(self) -> None:
        # Determines the coordinates of the piece based on its rank, file, and the
        # defined square size of the GUI.
        self.__coords = (
            self.position[1] * constants.SQUARE_SIZE,
            self.position[0] * constants.SQUARE_SIZE,
        )

    @property
    def position(self):
        """The position of the piece in (x, y) format, where x is the rank and y is the file.
        Both x and y are integers between 0 and 7, inclusive."""
        return self.__position

    @position.setter
    def position(self, position: tuple):
        if not (0 <= position[0] <= 7 and 0 <= position[1] <= 7):
            raise ValueError("Invalid position.")
        else:
            self.__position = position
            self.__refresh_coords()

    @property
    def legal_moves(self) -> tuple:
        """The legal moves of the piece in a tuple of tuples, where each tuple
        is a position on the board in (x, y) format."""
        return tuple(self.__legal_moves)

    @abstractmethod
    def _generate_possible_moves(self, board: "Board") -> set:
        """Generates the possible moves for the piece.

        Parameters
        ----------
        board : Board
            The board on which the piece is placed.

        Returns
        -------
        possible_moves : set
            A set of tuples, where each tuple is a position in (x, y) format.
        """

    def refresh_legal_moves(self, board: "Board") -> None:
        """Refreshes the legal moves of the piece.

        Parameters
        ----------
        board : Board
            The board on which the piece is placed.
        """
        self.__legal_moves = self._generate_legal_moves(board)

    def _generate_legal_moves(self, board: "Board") -> set:
        # Generate the legal moves for a piece by checking if they comply with the rules of chess
        possible_moves = self._generate_possible_moves(board)
        legal_moves = set(
            filter(
                lambda move: (
                    move != self.position
                    and chess_logic.is_legal_move(board, self, move)
                ),
                possible_moves,
            )
        )
        return legal_moves

    # Define a 'constructor' to create piece from algebraic notation
    @staticmethod
    def from_algebraic_notation(algebraic_notation: str, position: tuple) -> "Piece":
        """Returns a piece based on its algebraic notation and position.

        Parameters
        ----------
        algebraic_notation : str
            The algebraic notation of the piece (e.g. "K" for a white king).
        position : tuple
            The position of the piece in (x, y) format, where x is the rank and y is the file.

        Returns
        -------
        piece : Piece
            The piece corresponding to the algebraic notation and position.

        Raises
        ------
        ValueError
            If the algebraic notation is invalid.
        """
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

    def to_algebraic_notation(self) -> str:
        """Returns the algebraic notation of the piece.

        Returns
        -------
        algebraic_notation : str
            The algebraic notation of the piece (e.g. "K" for a white king).
        """
        if self.name == "Knight":
            return "n" if self.color == "black" else "N"
        return self.name[0].lower() if self.color == "black" else self.name[0].upper()

    def __repr__(self) -> str:
        # Returns a string representation of the piece (i.e. its color and name, e.g. "White King")
        return f"{self.color.title()} {self.name}"

    def __eq__(self, other: "Piece") -> bool:
        # Returns True if the pieces' names, colors, and positions are equal, False otherwise
        if not isinstance(other, Piece):
            return False

        return (
            self.name == other.name
            and self.color == other.color
            and self.position == other.position
        )


class Pawn(Piece):
    """Class representing a pawn piece."""

    def __init__(self, color: str, position: tuple) -> None:
        super().__init__(name="Pawn", value=1, position=position, color=color)

    def _generate_possible_moves(self, board: "Board") -> set:
        possible_moves = set()
        # set the direction of the pawn based on its color
        direction = -1 if self.color == "white" else 1

        # check for a single step forward
        x_new = self.position[0] + direction
        if 0 <= x_new < 8 and not board.is_square_occupied((x_new, self.position[1])):
            possible_moves.add((x_new, self.position[1]))

            # check for a double step forward if the pawn has not moved yet
            if not self.has_moved:
                x_new = self.position[0] + 2 * direction
                if 0 <= x_new < 8 and not board.is_square_occupied(
                    (x_new, self.position[1])
                ):
                    possible_moves.add((x_new, self.position[1]))

        # check for captures
        for j in [-1, 1]:
            y_new = self.position[1] + j
            if 0 <= y_new < 8:
                x_new = self.position[0] + direction
                if (
                    0 <= x_new <= 7
                    and board.is_square_occupied((x_new, y_new))
                    and board.get_piece_at_square((x_new, y_new)).color != self.color
                ):
                    possible_moves.add((x_new, y_new))

        # check for en passant
        if (
            board.en_passant_piece is not None
            and board.en_passant_piece.color != self.color
        ):
            if (
                0 <= x_new < 8
                and board.en_passant_piece.position[0] == self.position[0]
                and abs(board.en_passant_piece.position[1] - self.position[1]) == 1
            ):
                possible_moves.add((x_new, board.en_passant_piece.position[1]))

        return possible_moves


class Rook(Piece):
    """Class representing a rook piece."""

    def __init__(self, color: str, position: tuple) -> None:
        super().__init__(name="Rook", value=5, position=position, color=color)

    def _generate_possible_moves(self, board: "Board") -> set:
        possible_moves = set()
        x_current, y_current = self.position

        for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x_new, y_new = x_current + i, y_current + j
            while 0 <= x_new < 8 and 0 <= y_new < 8:
                possible_moves.add((x_new, y_new))
                x_new += i
                y_new += j
        return possible_moves


class Knight(Piece):
    """Class representing a knight piece."""

    def __init__(self, color: str, position: tuple) -> None:
        super().__init__(name="Knight", value=3, position=position, color=color)

    def _generate_possible_moves(self, board: "Board") -> set:
        """
        Generates the possible moves for the knight.

        Parameters:
        board (Board): the board on which the piece is placed.
        """
        possible_moves = set()
        for i, j in [
            (2, 1),
            (1, 2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (-1, -2),
            (1, -2),
            (2, -1),
        ]:
            x_new, y_new = self.position[0] + i, self.position[1] + j
            if 0 <= x_new < 8 and 0 <= y_new < 8:
                if (
                    not board.is_square_occupied((x_new, y_new))
                    or board.get_piece_at_square((x_new, y_new)).color != self.color
                ):
                    possible_moves.add((x_new, y_new))

        return possible_moves


class Bishop(Piece):
    """Class representing a bishop piece."""

    def __init__(self, color: str, position: tuple) -> None:
        super().__init__(name="Bishop", value=3, position=position, color=color)

    def _generate_possible_moves(self, board: "Board") -> set:
        """
        Generates the possible moves for the bishop.

        Parameters:
        board (Board): the board on which the piece is placed.
        """
        possible_moves = set()
        (
            x_current,
            y_current,
        ) = self.position
        for i, j in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x_new, y_new = x_current + i, y_current + j
            while 0 <= x_new < 8 and 0 <= y_new < 8:
                possible_moves.add((x_new, y_new))
                x_new += i
                y_new += j
        return possible_moves


class Queen(Piece):
    """Class representing a queen piece."""

    def __init__(self, color: str, position: tuple) -> None:
        super().__init__(name="Queen", value=9, position=position, color=color)

    def _generate_possible_moves(self, board: "Board") -> set:
        possible_moves = set()
        x_current, y_current = self.position
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
    """Class representing a king piece."""

    def __init__(self, color: str, position: tuple) -> None:
        super().__init__(name="King", value=100, position=position, color=color)

    def _generate_possible_moves(self, board: "Board") -> set:
        possible_moves = set()
        x_current, y_current = self.position
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

        # Castling - check whether the path is blocked or not (use is_path_blocked), 
        # whether any squares in the path are under attack, whether the king has moved or not, 
        # whether the rook has moved or not, and whether the king is under attack or not.
        if not self.has_moved:
            queen_side_rook = board.get_piece_at_square((self.position[0], 0))
            # Check whether the king can castle queen side
            if (
                isinstance(queen_side_rook, Rook)
                and (not queen_side_rook.has_moved)
                and (
                    not board.is_path_blocked(
                        (self.position[0], 4), (self.position[0], 0)
                    )
                )
                and (
                    not board.is_horizontal_path_attacked(
                        (self.position[0], 0), (self.position[0], 4), self.color
                    )
                )
                and (not chess_logic.is_check(board, self.color))
            ):

                possible_moves.add((self.position[0], 2))

            king_side_rook = board.get_piece_at_square((self.position[0], 7))
            # Check whether the king can castle king side
            if (
                isinstance(king_side_rook, Rook)
                and (not king_side_rook.has_moved)
                and (
                    not board.is_path_blocked(
                        (self.position[0], 4), (self.position[0], 7)
                    )
                )
                and (
                    not board.is_horizontal_path_attacked(
                        (self.position[0], 4), (self.position[0], 7), self.color
                    )
                )
                and (not chess_logic.is_check(board, self.color))
            ):

                possible_moves.add((self.position[0], 6))

        return possible_moves
