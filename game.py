"""
game.py
This module contains the ChessGame class.
This class is used to represent a chess game. It has properties like board, turn, game_over and methods make_move, run etc.
It is responsible for managing the state of the game and making moves on the board.
"""
from board import Board
import chess_logic


class ChessGame:
    """
    ChessGame:
    This is a class for representing a chess game.
    It has properties like board, turn and game_over, and methods make_move, run etc.
    It is responsible for managing the state of the game and making moves on the board."""

    def __init__(self):
        """
        Initializes the board and the turn.
        """
        self.board = Board()
        self.turn = "white"
        self.game_over = False

    def make_move(self, original_position, new_position):
        """
        Make a move on the board.

        Parameters:
            original_position (tuple): original position on the board
                in (x, y) format, where x is the row and y is the column.
            new_position (tuple): new position on the board
                in (x, y) format, where x is the row and y is the column.
        """
        piece = self.board.get_piece_at_square(original_position)
        print(piece)
        print("Original position: ", original_position)
        print("New position: ", new_position)
        if piece is None:
            raise ValueError("No piece at the given position.")
        if piece.color != self.turn:
            raise ValueError("It is not your turn.")
        if new_position not in piece.legal_moves:
            raise ValueError("Invalid move.")
        if chess_logic.is_king_in_check_after_move(
                self.board, piece, new_position):
            raise ValueError("This move would put your king in check.")

        self.board.move_piece_to_square(piece, new_position)
        print(self.board)
        self.turn = "white" if self.turn == "black" else "black"

    def run(self):
        """
        Runs the game.
        """
        while not self.game_over:
            print(self.board)
            original_position = tuple(
                map(
                    int,
                    Board.get_position_from_algebraic_notation(
                        input(
                            "Enter the original position of the piece you want to move: "
                        )
                    ),
                )
            )
            new_position = tuple(map(int, Board.get_position_from_algebraic_notation(
                input("Enter the new position of the piece you want to move: ")), ))
            try:
                self.make_move(original_position, new_position)
            except ValueError as error:
                print(error)
