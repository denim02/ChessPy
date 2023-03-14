"""
board.py
This module contains the implementation of the Board class,
which is responsible for maintaining the chess board and its state.
The class contains methods for moving pieces, checking if a square is occupied,
checking if a square is attacked, and checking if a path is blocked. Additionally,
it has a method for refreshing the legal moves for all pieces on the board.
"""
from chess_game.pieces import Piece


class Board:
    """
    Initializes the board with a 2D array of pieces and a list of all pieces on the board.
    """

    def __init__(self):
        """
        Initializes the board with a 2D array of pieces and a list of all pieces on the board.
        """
        self.__board_table = self.populate_board()
        self.__piece_list = [
            piece for row in self.__board_table for piece in row if piece is not None
        ]
        self.last_piece_captured = None
        self.refresh_legal_moves()

    @property
    def piece_list(self):
        """
        Returns a list of all pieces on the board.
        """
        return self.__piece_list

    def refresh_legal_moves(self):
        """
        Generates all valid moves for all pieces on the board.
        """
        for piece in self.piece_list:
            piece.refresh_legal_moves(self)

    def get_piece_at_square(self, position):
        """
        Returns the piece at the given position on the board.

        Parameters:
            position (tuple): position on the board in (x, y) format,
                where x is the row and y is the column.

        Returns:
            Piece: piece at the given position or None if the position is empty.
        """
        return self.__board_table[position[0]][position[1]]

    def move_piece_to_square(self, piece, new_position):
        """
        Move a piece to a new position on the board.

        Parameters:
            piece (Piece): piece to be moved.
            new_position (tuple): new position on the board in (x, y) format,
                where x is the row and y is the column.
        """
        occupying_piece = self.get_piece_at_square(new_position)

        if self.last_piece_captured is not None:
            self.last_piece_captured = None

        if occupying_piece is not None:
            self.last_piece_captured = occupying_piece
            self.piece_list.remove(occupying_piece)

        self.__board_table[piece.position[0]][piece.position[1]] = None
        piece.position = new_position
        self.__board_table[new_position[0]][new_position[1]] = piece
        self.refresh_legal_moves()
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
            self.piece_list.append(self.last_piece_captured)
            self.__board_table[piece.position[0]][
                piece.position[1]
            ] = self.last_piece_captured
            self.last_piece_captured = None
        else:
            self.__board_table[piece.position[0]][piece.position[1]] = None

        piece.position = old_position
        self.__board_table[old_position[0]][old_position[1]] = piece
        
        self.refresh_legal_moves()

    def is_square_occupied(self, position):
        """
        Check if a given position on the board is occupied by a piece.

        Parameters:
            position (tuple): position on the board in (x, y)
                format, where x is the row and y is the column.

        Returns:
            bool: True if the position is occupied, False otherwise.
        """
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
        for piece in self.piece_list:
            if piece.color != color and position in piece.legal_moves:
                return True
        return False

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
        return Board.parse_fen("./game/game_states/init_position.fen")

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

    def print_board_from_piece_list(self):
        """
        Print the board in a pretty readable format from the piece list.
        """
        string = "  a b c d e f g h \n"
        for i in range(8):
            string += str(8 - i) + " "
            for j in range(8):
                found = False
                for piece in self.piece_list:
                    if piece.position == (i, j):
                        string += piece.to_algebraic_notation() + " "
                        found = True
                        break
                if not found:
                    string += ". "
            string += str(8 - i) + "\n"
        string += "  a b c d e f g h \n"
        print(string)

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
        return chr(position[1] + 97) + str(8 - position[0])

    @staticmethod
    def get_position_from_algebraic_notation(algebraic_notation):
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
