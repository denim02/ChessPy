"""The board module contains the Board class, which represents the chess board.

The Board class is responsible for maintaining the chess board and its state. It contains methods 
for moving pieces, promoting pawns, checking if a square is occupied, checking if a square is attacked, 
and checking  if a path is blocked. Additionally, it has a method for refreshing the legal moves 
for all pieces on the board."""
from typing import Union, Optional
from chess_game import pieces, constants


class Board:
    """Class representing the chess board and its pieces/state."""

    def __init__(self):
        self.__board_table = [[None for _ in range(8)] for _ in range(8)]
        self.__piece_list = []

        # Intialize variables needed for en passant and reverting moves (for is_king_in_check_after_move)
        self.en_passant_piece = None
        self.last_piece_captured = None
        self.has_moved_changed = False

    @property
    def piece_list(self) -> tuple:
        """A tuple containing all pieces on the board."""
        return tuple(self.__piece_list)

    def __refresh_legal_moves(self) -> None:
        # Refreshes the legal moves for all pieces on the board by calling the refresh_legal_moves method for each
        for piece in self.__piece_list:
            piece.refresh_legal_moves(self)

    def get_piece_at_square(self, position: tuple) -> Union["pieces.Piece", None]:
        """Returns the piece at a given position on the board.

        Parameters
        ----------
        position : tuple
            Position on the board in (x, y) format, where x is the rank and y is the file.

        Returns
        -------
        piece : Piece, None
            piece at the given position on the board.
        """
        if position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7:
            return None
        return self.__board_table[position[0]][position[1]]

    def _place_piece(self, piece: pieces.Piece) -> None:
        # Places a piece on the board at a given position
        if self.get_piece_at_square(piece.position) is not None:
            raise ValueError("Square is already occupied!")
        elif (
            piece.position[0] < 0
            or piece.position[0] > 7
            or piece.position[1] < 0
            or piece.position[1] > 7
        ):
            raise ValueError("Invalid position!")
        self.__board_table[piece.position[0]][piece.position[1]] = piece
        self.__piece_list.append(piece)
        self.__refresh_legal_moves()

    def _remove_piece_at_square(self, position: tuple) -> None:
        # Removes a piece from the board at a given position
        if position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7:
            raise ValueError("Invalid position!")

        piece = self.get_piece_at_square(position)
        self.__board_table[position[0]][position[1]] = None

        if piece is not None:
            self.__piece_list.remove(piece)
            self.__refresh_legal_moves()

    def move_piece_to_square(
        self,
        piece: "pieces.Piece",
        new_position: tuple,
        change_en_passant: Optional[bool] = True,
    ) -> Union["pieces.Piece", None]:
        """Move a piece to a new position on the board.

        This method is used to move a piece to a new position on the board. It also handles en passant logic.
        In order to allow reverting moves (for checking if the king is in check after a move), the method
        modifies a series of attributes in the Board object, such as has_move_changed, en_passant_piece, and
        last_piece_captured. These attributes are used by the revert_move method.

        Parameters
        ----------
        piece : Piece
            Piece to be moved.
        new_position : tuple
            New position on the board in (x, y) format, where x is the rank and y is the file.
        change_en_passant : bool, optional
            Whether or not to change the en passant piece (default is True). This is used to allow en passant
            on the next move.

        Returns
        -------
        occupying_piece : Piece, None
            The piece that was at the new position before the move. None if there was no piece at the new position.

        Raises
        ------
        ValueError
            If the new position is invalid.
        """
        # Check first if the move is to a valid position on the board
        if not (0 <= new_position[0] <= 7 and 0 <= new_position[1] <= 7):
            raise ValueError("New position is invalid!")

        # Get the piece at the new position (if there is one)
        occupying_piece = self.get_piece_at_square(new_position)

        # Set has_moved to True if the piece has not moved yet (used for castling/revert move)
        self.has_moved_changed = not piece.has_moved
        piece.has_moved = True

        # En passant logic
        # Check if the move was an en passant capture and remove the captured piece
        if (
            piece.name == "Pawn"
            and self.en_passant_piece is not None
            and self.en_passant_piece.position
            == (
                new_position[0] + (1 if piece.color == "white" else -1),
                new_position[1],
            )
            and self.en_passant_piece.color != piece.color
        ):
            occupying_piece = self.en_passant_piece
            self.__board_table[self.en_passant_piece.position[0]][
                self.en_passant_piece.position[1]
            ] = None

        # Check if the move was a pawn leaping two squares (used to allow possible en passant next move)
        # (used to detect possibility of en passant)
        if change_en_passant:
            if piece.name == "Pawn" and abs(new_position[0] - piece.position[0]) == 2:
                self.en_passant_piece = piece
            else:
                self.en_passant_piece = None

        # Clear the piece that was captured last time (used for reverting moves)
        if self.last_piece_captured is not None:
            self.last_piece_captured = None

        # Remove the piece at the new position (if there is one)
        if occupying_piece is not None:
            self.last_piece_captured = occupying_piece
            self.__piece_list.remove(occupying_piece)

        # Move the piece to the new position
        self.__board_table[piece.position[0]][piece.position[1]] = None
        piece.position = new_position
        self.__board_table[new_position[0]][new_position[1]] = piece

        # Refresh the legal moves for all pieces
        self.__refresh_legal_moves()
        return occupying_piece

    def revert_move(self, piece: "pieces.Piece", old_position: tuple) -> None:
        """Revert a move made by a piece (must be the last move made on the board).

        Parameters
        ----------
        piece : Piece
            Piece to be revert the move of.
        old_position : tuple
            Old position of the piece in (x, y) format, where x is the rank and y is the file.
        """
        # Revert the capturing of a piece (if there was one)
        if self.last_piece_captured is not None:
            self.__piece_list.append(self.last_piece_captured)
            self.__board_table[piece.position[0]][
                piece.position[1]
            ] = self.last_piece_captured
            self.last_piece_captured = None
        else:
            self.__board_table[piece.position[0]][piece.position[1]] = None

        # If the piece moved for the first time, set has_moved to False
        if self.has_moved_changed is True:
            piece.has_moved = False
            self.has_moved_changed = False

        # Set the piece's position to the old position
        piece.position = old_position
        self.__board_table[old_position[0]][old_position[1]] = piece

        self.__refresh_legal_moves()

    def promote_pawn(self, piece: "pieces.Piece", choice: str) -> None:
        """Promote a pawn to a different piece.

        This method is used to promote a pawn to a different piece. It swaps the piece
        in place, meaning that the pawn is replaced by the new piece without changing
        the position of the piece. Thus, the position must be changed manually.

        Parameters
        ----------
        piece : Piece
            Pawn to be promoted.
        choice : str
            Choice of piece to promote to. Must be one of "Q", "R", "B", or "N".

        Raises
        ------
        ValueError
            If the piece is not a pawn, if the choice is invalid, or if
            the pawn is not at the end of the board.
        """
        if piece.name != "Pawn":
            raise ValueError("Piece is not a pawn!")

        if (piece.color == "white" and piece.position[0] != 0) or (
            piece.color == "black" and piece.position[0] != 7
        ):
            raise ValueError("Pawn is not at the end of the board!")

        if choice == "Q":
            new_piece = pieces.Queen(piece.color, piece.position)
        elif choice == "R":
            new_piece = pieces.Rook(piece.color, piece.position)
        elif choice == "B":
            new_piece = pieces.Bishop(piece.color, piece.position)
        elif choice == "N":
            new_piece = pieces.Knight(piece.color, piece.position)
        else:
            raise ValueError("Invalid choice!")

        self.__piece_list.remove(piece)
        self.__piece_list.append(new_piece)
        self.__board_table[piece.position[0]][piece.position[1]] = new_piece
        self.__refresh_legal_moves()

    def is_square_occupied(self, position: tuple) -> bool:
        """Check if a given position on the board is occupied by a piece.

        Parameters
        ----------
        position : tuple
            Position on the board in (x, y) format, where x is the rank and y is the file.

        Returns
        -------
        bool
            True if the position is occupied, False otherwise.

        Raises
        ------
        ValueError
            If the position is invalid.
        """
        if position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7:
            raise ValueError("Invalid position!")

        return self.__board_table[position[0]][position[1]] is not None

    def is_square_attacked(self, position: tuple, color: str) -> bool:
        """Check if a given position on the board is under attack for a given color.

        Parameters
        ----------
        position : tuple
            Position on the board in (x, y) format, where x is the rank and y is the file.
        color : str
            Color to check whether it is under attack. Must be either "white" or "black".

        Returns
        -------
        bool
            True if the position is under attack, False otherwise.

        Raises
        ------
        ValueError
            If the position is invalid.
        """
        if position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7:
            raise ValueError("Invalid position!")

        return any(
            position in piece.legal_moves
            for piece in self.piece_list
            if piece.color != color
        )

    def is_horizontal_path_attacked(
        self, start_position: tuple, end_position: tuple, color: str
    ) -> bool:
        """Check if a horizontal path on the board is under attack for a given color.

        Parameters
        ----------
        start_position : tuple
            Starting position of the path on the board in (x, y) format, where x is the rank and y is the file.
        end_position : tuple
            Ending position of the path on the board in (x, y) format, where x is the rank and y is the file.
        color : str
            Color to check whether it is under attack. Must be either "white" or "black".

        Returns
        -------
        bool
            True if the path is under attack, False otherwise.
        """
        return any(
            self.is_square_attacked((start_position[0], i), color)
            for i in range(start_position[1], end_position[1] + 1)
        )

    def is_path_blocked(self, start_position: tuple, end_position: tuple) -> bool:
        """Check if the path between two positions is blocked by a piece.

        This method can be used to check if the path between two positions is blocked,
        regardless of whether that path is horizontal, vertical, or diagonal.

        Parameters
        ----------
        start_position : tuple
            Starting position of the path on the board in (x, y) format, where x is the rank and y is the file.
        end_position : tuple
            Ending position of the path on the board in (x, y) format, where x is the rank and y is the file.

        Returns
        -------
        bool
            True if the path is blocked, False otherwise.
        """
        # Path on same row
        if start_position[0] == end_position[0]:
            for i in range(
                min(start_position[1], end_position[1]) + 1,
                max(start_position[1], end_position[1]),
            ):
                if self.is_square_occupied((start_position[0], i)):
                    return True
        # Path on same column
        elif start_position[1] == end_position[1]:
            for i in range(
                min(start_position[0], end_position[0]) + 1,
                max(start_position[0], end_position[0]),
            ):
                if self.is_square_occupied((i, start_position[1])):
                    return True
        # Path on diagonal
        elif abs(start_position[0] - end_position[0]) == abs(
            start_position[1] - end_position[1]
        ):
            for i in range(1, abs(start_position[0] - end_position[0])):
                if self.is_square_occupied(
                    (
                        start_position[0] + i
                        if start_position[0] < end_position[0]
                        else start_position[0] - i,
                        start_position[1] - i
                        if start_position[1] >= end_position[1]
                        else start_position[1] + i,
                    )
                ):
                    return True
        return False

    def populate_board(self) -> None:
        """Populate the board with pieces in their starting positions as specified by the STARTING_FEN_FILE
        parameter in the game constants."""
        try:
            self.__board_table = Board.parse_fen_from_file(constants.STARTING_FEN_FILE)
        except FileNotFoundError:
            print("Starting FEN file not found! Using default starting position.")
            self.__board_table = Board.parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        finally:
            self.__piece_list = [
                piece for row in self.__board_table for piece in row if piece is not None
            ]
            self.__refresh_legal_moves()

    @classmethod
    def instantiate_from_fen_file(cls, fen_filepath: str) -> "Board":
        """Instantiate a board from a FEN file.

        Parameters
        ----------
        fen_filepath : str
            Path to the FEN file.

        Returns
        -------
        Board
            Board object instantiated from the FEN file."""
        board = cls()
        board._Board__board_table = Board.parse_fen_from_file(fen_filepath)
        board._Board__piece_list = [
            piece
            for row in board._Board__board_table
            for piece in row
            if piece is not None
        ]
        board._Board__refresh_legal_moves()
        return board

    def __repr__(self) -> str:
        # Returns a string representation of the board.
        string = "  a b c d e f g h \n"
        for i in range(8):
            string += str(8 - i) + " "
            for j in range(8):
                if self.__board_table[i][j] is None:
                    string += ". "
                else:
                    string += self.__board_table[i][j].to_algebraic_notation() + " "
            string += str(8 - i) + "\n"
        string += "  a b c d e f g h \n"
        return string

    @staticmethod
    def get_algebraic_notation(position: tuple) -> str:
        """Returns the algebraic notation of a position on the board.

        Parameters
        ----------
        position : tuple
            Position on the board in (x, y) format, where x is the row and y is the column.

        Returns
        -------
        str
            Algebraic notation of the position (e.g. "a1", "e5", "h8").

        Raises
        ------
        ValueError
            If the position is not valid.
        """
        if position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7:
            raise ValueError("Invalid position!")

        return chr(position[1] + 97) + str(8 - position[0])

    @staticmethod
    def get_square_from_algebraic_notation(algebraic_notation: str) -> tuple:
        """Returns the position on the board from its algebraic notation.

        Parameters
        ----------
        algebraic_notation : str
            Algebraic notation of the position (e.g. "a1", "e5", "h8").

        Returns
        -------
        tuple
            Position on the board in (x, y) format, where x is the rank and y is the file.
        """
        return (8 - int(algebraic_notation[1]), ord(algebraic_notation[0]) - 97)

    @staticmethod
    def parse_fen(fen_string: str) -> list:
        """Parse a string representing a board in FEN notation and return 
        a list with the pieces that should be on the board.

        Parameters
        ----------
        fen_string : str
            String containing FEN representation of a chess board.

        Returns
        -------
        list
            List with the pieces that should be on the board.
        """
        ranks = fen_string.split("/")

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
                        board[i].append(
                            pieces.Piece.from_algebraic_notation(
                                j, (i, len(board[i]))
                            )
                        )

        return board

    @staticmethod
    def parse_fen_from_file(fen_filepath: str) -> list:
        """Returns a list with the pieces that should be on the board from a FEN file.
        
        Parameters
        ----------
        fen_filepath : str
            Path to the FEN file.
            
        Returns
        -------
        list
            List with the pieces that should be on the board.

        Raises
        ------
        FileNotFoundError
            If the FEN file does not exist at the specified path.
        """
        try:
            with open(fen_filepath, encoding="utf8") as file:
                string_fen = file.read()
                return Board.parse_fen(string_fen)
        except FileNotFoundError:
            raise
        

    def get_fen_board_state(self) -> dict:
        """Returns a dictionary with the state of the board.

        This dictionary contains the positions of the pieces on the board in FEN notation,
        the castling rights of each player and the en passant target square (i.e. the square
        where a pawn would move if it can perform an en passant capture).

        Returns
        -------
        dict
            Dictionary with the state of the board.
        """
        return {
            "piece_placement": self._get_fen_board(),
            "castling_availability": self._get_fen_castling_rights(),
            "en_passant_target_square": self._get_fen_en_passant_target_square(),
        }

    def _get_fen_board(self) -> str:
        # Returns a string representing the board in FEN notation.
        fen = ""
        for row in self.__board_table:
            empty_squares = 0
            for piece in row:
                if piece is None:
                    empty_squares += 1
                else:
                    if empty_squares > 0:
                        fen += str(empty_squares)
                        empty_squares = 0
                    fen += piece.to_algebraic_notation()
            if empty_squares > 0:
                fen += str(empty_squares)
            fen += "/"

        return fen[:-1]

    def _get_fen_castling_rights(self) -> str:
        # Returns a string representing the castling rights in FEN notation.
        fen = ""

        black_king = self.get_piece_at_square((0, 4))
        black_queenside_rook = self.get_piece_at_square((0, 0))
        black_kingside_rook = self.get_piece_at_square((0, 7))

        white_king = self.get_piece_at_square((7, 4))
        white_queenside_rook = self.get_piece_at_square((7, 0))
        white_kingside_rook = self.get_piece_at_square((7, 7))

        if isinstance(white_king, pieces.King) and not white_king.has_moved:
            if (
                isinstance(white_kingside_rook, pieces.Rook)
                and not white_kingside_rook.has_moved
            ):
                fen += "K"
            if (
                isinstance(white_queenside_rook, pieces.Rook)
                and not white_queenside_rook.has_moved
            ):
                fen += "Q"

        if isinstance(black_king, pieces.King) and not black_king.has_moved:
            if (
                isinstance(black_kingside_rook, pieces.Rook)
                and not black_kingside_rook.has_moved
            ):
                fen += "k"
            if (
                isinstance(black_queenside_rook, pieces.Rook)
                and not black_queenside_rook.has_moved
            ):
                fen += "q"

        if fen == "":
            fen = "-"

        return fen

    def _get_fen_en_passant_target_square(self) -> str:
        # Returns a string representing the en passant target square in FEN notation.
        if self.en_passant_piece is None:
            return "-"
        else:
            direction = 1 if self.en_passant_piece.color == "white" else -1
            return Board.get_algebraic_notation(
                (
                    self.en_passant_piece.position[0] + direction,
                    self.en_passant_piece.position[1],
                )
            )
