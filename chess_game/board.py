"""
board.py
This module contains the implementation of the Board class,
which is responsible for maintaining the chess board and its state.
The class contains methods for moving pieces, checking if a square is occupied,
checking if a square is attacked, and checking if a path is blocked. Additionally,
it has a method for refreshing the legal moves for all pieces on the board.
"""
from chess_game.pieces import *

class Board:
    """
    Initializes the board with a 2D array of pieces and a list of all pieces on the board.
    """

    def __init__(self):
        """
        Initializes the board with a 2D array of pieces and a list of all pieces on the board.
        """
        self.__board_table = [[None for _ in range(8)] for _ in range(8)]
        self.__piece_list = []

        # Intialize variables needed for en passant and reverting moves (for is_king_in_check_after_move)
        self.en_passant_piece = None
        self.last_piece_captured = None
        self.has_moved_changed = False

    @property
    def piece_list(self):
        """
        Returns a list of all pieces on the board.
        """
        return tuple(self.__piece_list)

    def __refresh_legal_moves(self):
        """
        Generates all valid moves for all pieces on the board.
        """
        for piece in self.__piece_list:
            piece._refresh_legal_moves(self)

    def get_piece_at_square(self, position):
        """
        Returns the piece at the given position on the board.

        Parameters:
            position (tuple): position on the board in (x, y) format,
                where x is the row and y is the column.

        Returns:
            Piece: piece at the given position or None if the position is empty.
        """
        if position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7:
            return None
        return self.__board_table[position[0]][position[1]]

    def _place_piece(self, piece):
        """
        Places a piece on the board.

        Parameters:
            piece (Piece): piece to be placed on the board.
        """
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

    def _remove_piece_at_square(self, position):
        """
        Removes a piece from the board.

        Parameters:
            position (tuple): position on the board in (x, y) format,
                where x is the row and y is the column.
        """
        if position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7:
            raise ValueError("Invalid position!")

        piece = self.get_piece_at_square(position)
        self.__board_table[position[0]][position[1]] = None

        if piece is not None:
            self.__piece_list.remove(piece)
            self.__refresh_legal_moves()

    def move_piece_to_square(self, piece, new_position, change_en_passant=True):
        """
        Move a piece to a new position on the board.

        Parameters:
            piece (Piece): piece to be moved.
            new_position (tuple): new position on the board in (x, y) format,
                where x is the row and y is the column.
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
            if(
                piece.name == "Pawn"
                and abs(new_position[0] - piece.position[0]) == 2
            ):
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

    def revert_move(self, piece, old_position):
        """
        Revert a move and replace any captured piece.

        Parameters:
            piece (Piece): piece to be moved.
            old_position (tuple): old position on the board in (x, y) format,
                where x is the row and y is the column.
        """
        if self.last_piece_captured is not None:
            self.__piece_list.append(self.last_piece_captured)
            self.__board_table[piece.position[0]][
                piece.position[1]
            ] = self.last_piece_captured
            self.last_piece_captured = None
        else:
            self.__board_table[piece.position[0]][piece.position[1]] = None

        if self.has_moved_changed is True:
            piece.has_moved = False
            self.has_moved_changed = False

        piece.position = old_position
        self.__board_table[old_position[0]][old_position[1]] = piece

        self.__refresh_legal_moves()

    def promote_pawn(self, piece, choice):
        """
        Promote a pawn to a new piece.

        Parameters:
            piece (Piece): pawn to be promoted.
            choice (str): type of piece to promote to.
        """
        if piece.name != "Pawn":
            raise ValueError("Piece is not a pawn!")

        if (piece.color == "white" and piece.position[0] != 0) or (
            piece.color == "black" and piece.position[0] != 7
        ):
            raise ValueError("Pawn is not at the end of the board!")

        if choice == "Queen":
            new_piece = Queen(piece.color, piece.position)
        elif choice == "Rook":
            new_piece = Rook(piece.color, piece.position)
        elif choice == "Bishop":
            new_piece = Bishop(piece.color, piece.position)
        elif choice == "Knight":
            new_piece = Knight(piece.color, piece.position)
        else:
            raise ValueError("Invalid choice!")

        self.__piece_list.remove(piece)
        self.__piece_list.append(new_piece)
        self.__board_table[piece.position[0]][piece.position[1]] = new_piece
        self.__refresh_legal_moves()

    def is_square_occupied(self, position):
        """
        Check if a given position on the board is occupied by a piece.

        Parameters:
            position (tuple): position on the board in (x, y)
                format, where x is the row and y is the column.

        Returns:
            bool: True if the position is occupied, False otherwise.
        """
        if position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7:
            raise ValueError("Invalid position!")

        return self.__board_table[position[0]][position[1]] is not None

    def is_square_attacked(self, position, color):
        """
        Check if a given position on the board is attacked by any piece of a different color.

        Parameters:
            position (tuple): position on the board in (x, y)
                format, where x is the row and y is the column.
            color (str): color of the attacking pieces,
                either "white" or "black".

        Returns:
            bool: True if the position is attacked, False otherwise.
        """
        if position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7:
            raise ValueError("Invalid position!")

        return any(
            position in piece.legal_moves
            for piece in self.piece_list
            if piece.color != color
        )

    def is_horizontal_path_attacked(self, start_position, end_position, color):
        return any(
            self.is_square_attacked((start_position[0], i), color)
            for i in range(start_position[1], end_position[1] + 1)
        )

    def is_path_blocked(self, original_position, new_position):
        """
        Check if there is a piece blocking the path between two positions on the board.

        Parameters:
            original_position (tuple): original position on the board
                in (x, y) format, where x is the row and y is the column.
            new_position (tuple): new position on the board
                in (x, y) format, where x is the row and y is the column.

        Returns:
            bool: True if the path is blocked, False otherwise.
        """
        # Path on same row
        if original_position[0] == new_position[0]:
            for i in range(
                min(original_position[1], new_position[1]) + 1,
                max(original_position[1], new_position[1]),
            ):
                if self.is_square_occupied((original_position[0], i)):
                    return True
        # Path on same column
        elif original_position[1] == new_position[1]:
            for i in range(
                min(original_position[0], new_position[0]) + 1,
                max(original_position[0], new_position[0]),
            ):
                if self.is_square_occupied((i, original_position[1])):
                    return True
        # Path on diagonal
        elif abs(original_position[0] - new_position[0]) == abs(
            original_position[1] - new_position[1]
        ):
            for i in range(1, abs(original_position[0] - new_position[0])):
                if self.is_square_occupied(
                    (
                        original_position[0] + i
                        if original_position[0] < new_position[0]
                        else original_position[0] - i,
                        original_position[1] - i
                        if original_position[1] >= new_position[1]
                        else original_position[1] + i,
                    )
                ):
                    return True
        return False

    def populate_board(self):
        """
        Populate the board with pieces from a file in FEN notation.

        Returns:
            list: 2D array of pieces representing the board.
        """
        self.__board_table = Board.parse_fen("./game/game_states/init_position.fen")
        self.__piece_list = [
            piece for row in self.__board_table for piece in row if piece is not None
        ]
        self.__refresh_legal_moves()

    @classmethod
    def instantiate_from_fen(cls, fen_path):
        """
        Instantiate a board from a file in FEN notation.

        Parameters:
            fen_path (str): path to the FEN file.

        Returns:
            Board: board object.
        """
        board = cls()
        board._Board__board_table = Board.parse_fen(fen_path)
        board._Board__piece_list = [
            piece
            for row in board._Board__board_table
            for piece in row
            if piece is not None
        ]
        board._Board__refresh_legal_moves()
        return board

    def __repr__(self):
        """
        Print the board in a pretty readable format.
        """
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
    def get_algebraic_notation(position):
        """
        Convert a position in the board to algebraic notation.

        Parameters:
            position (tuple): position on the board in
                (x, y) format, where x is the row and y is the column.

        Returns:
            str: algebraic notation of the position.
        """
        if position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7:
            raise ValueError("Invalid position!")

        return chr(position[1] + 97) + str(8 - position[0])

    @staticmethod
    def get_square_from_algebraic_notation(algebraic_notation):
        """
        Convert a position in algebraic notation to a position on the board.

        Parameters:
            algebraic_notation (str): algebraic notation of the position.

        Returns:
            tuple: position on the board in (x, y) format, where x is the row and y is the column.
        """
        return (8 - int(algebraic_notation[1]), ord(algebraic_notation[0]) - 97)

    @staticmethod
    def parse_fen(file_path):
        """
        Parse the FEN notation from a file and return a 2D array of pieces.

        Parameters:
            file_path (str): path to the file containing the FEN notation.

        Returns:
            list: 2D array of pieces representing the board.
        """
        with open(file_path, encoding="utf8") as file:
            string_fen = file.read()
            ranks = string_fen.split("/")

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
                                Piece.from_algebraic_notation(j, (i, len(board[i])))
                            )

            return board
        
    def get_fen_board_state(self):
        """
        Return the FEN notation of the current board state.

        Returns:
            =dict: FEN notation of the current board state.
        """
        
        return {
            "piece_placement": self._get_fen_board(),
            "castling_availability": self._get_fen_castling_rights(),
            "en_passant_target_square": self._get_fen_en_passant_target_square()
        }
    
    def _get_fen_board(self):
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

    def _get_fen_castling_rights(self):
        """
        Return the FEN notation of the castling rights.

        Returns:
            str: FEN notation of the castling rights.
        """
        fen = ""

        black_king = self.get_piece_at_square((0, 4))
        black_queenside_rook = self.get_piece_at_square((0, 0))
        black_kingside_rook = self.get_piece_at_square((0, 7))

        white_king = self.get_piece_at_square((7, 4))
        white_queenside_rook = self.get_piece_at_square((7, 0))
        white_kingside_rook = self.get_piece_at_square((7, 7))

        if isinstance(white_king, King) and not white_king.has_moved:
            if isinstance(white_kingside_rook, Rook) and not white_kingside_rook.has_moved:
                fen += "K"
            if isinstance(white_queenside_rook, Rook) and not white_queenside_rook.has_moved:
                fen += "Q"
            
        if isinstance(black_king, King) and not black_king.has_moved:
            if isinstance(black_kingside_rook, Rook) and not black_kingside_rook.has_moved:
                fen += "k"
            if isinstance(black_queenside_rook, Rook) and not black_queenside_rook.has_moved:
                fen += "q"
        
        if fen == "":
            fen = "-"

        return fen
            
    def _get_fen_en_passant_target_square(self):
        """
        Return the FEN notation of the en passant target square.

        Returns:
            str: FEN notation of the en passant target square.
        """
        if self.en_passant_piece is None:
            return "-"
        else:
            direction = 1 if self.en_passant_piece.color == "white" else -1
            return Board.get_algebraic_notation(
                (self.en_passant_piece.position[0] + direction, self.en_passant_piece.position[1])
            )
       