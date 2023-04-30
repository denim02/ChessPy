"""This module contains unit tests for the chess_logic module in chess_game/chess_logic.py."""
import unittest
from chess_game import chess_logic, board, pieces


class TestChessLogic(unittest.TestCase):
    def test_is_check(self):
        # First, no king is in check
        test_board = board.Board.instantiate_from_fen_file(
            "./game/game_states/test_check.fen"
        )
        self.assertFalse(chess_logic.is_check(test_board, "black"))
        self.assertFalse(chess_logic.is_check(test_board, "white"))

        # Now, the black king is in check
        test_board.move_piece_to_square(test_board.get_piece_at_square((7, 6)), (2, 1))
        self.assertTrue(chess_logic.is_check(test_board, "black"))
        test_board._remove_piece_at_square((2, 1))

        # Now, the white king is in check and the black king is not
        self.assertFalse(chess_logic.is_check(test_board, "black"))
        test_board.move_piece_to_square(test_board.get_piece_at_square((1, 3)), (1, 4))
        self.assertTrue(chess_logic.is_check(test_board, "white"))

    def test_is_checkmate(self):
        # Test simple checkmate for both colors where they have no valid moves
        # to block
        test_board = board.Board.instantiate_from_fen_file(
            "./game/game_states/test_checkmate.fen"
        )
        self.assertFalse(chess_logic.is_checkmate(test_board, "black"))
        self.assertFalse(chess_logic.is_checkmate(test_board, "white"))

        # Black is in checkmate
        test_board.move_piece_to_square(test_board.get_piece_at_square((5, 6)), (0, 6))
        self.assertTrue(chess_logic.is_checkmate(test_board, "black"))
        self.assertFalse(chess_logic.is_checkmate(test_board, "white"))

        # Both are in checkmate
        test_board.move_piece_to_square(test_board.get_piece_at_square((2, 1)), (7, 1))
        self.assertTrue(chess_logic.is_checkmate(test_board, "white"))
        self.assertTrue(chess_logic.is_checkmate(test_board, "black"))

        # A piece is placed so that white can move it to block the check
        test_board._place_piece(pieces.Rook("white", (1, 5)))
        self.assertFalse(chess_logic.is_checkmate(test_board, "white"))

    def test_is_king_in_check_after_move(self):
        test_board = board.Board.instantiate_from_fen_file(
            "./game/game_states/test_checkmate.fen"
        )

        # Test that although the black king is in check after the move, the
        # white king that initiated the move is not in check
        self.assertFalse(
            chess_logic.is_king_in_check_after_move(
                test_board, test_board.get_piece_at_square((1, 7)), (0, 7)
            )
        )
        test_board.move_piece_to_square(test_board.get_piece_at_square((1, 7)), (0, 7))

        # Place defending piece in front of black king and test that the
        # function returns true if the piece is moved
        test_board._place_piece(pieces.Pawn("black", (0, 2)))
        self.assertTrue(
            chess_logic.is_king_in_check_after_move(
                test_board, test_board.get_piece_at_square((0, 2)), (1, 2)
            )
        )

    def test_is_stalemate(self):
        test_board = board.Board.instantiate_from_fen_file(
            "./game/game_states/test_stalemate.fen"
        )

        # Test if one of the kings is in check, the game is not in stalemate
        test_board._place_piece(pieces.Rook("white", (0, 0)))
        self.assertFalse(chess_logic.is_stalemate(test_board, "black"))
        test_board._remove_piece_at_square((0, 0))

        # Test that the game is in stalemate for black and not for white
        self.assertTrue(chess_logic.is_stalemate(test_board, "black"))
        self.assertFalse(chess_logic.is_stalemate(test_board, "white"))

        test_board._remove_piece_at_square((1, 5))
        test_board._place_piece(pieces.Rook("black", (0, 4)))
        test_board._place_piece(pieces.Rook("black", (0, 6)))
        test_board._place_piece(pieces.Rook("black", (1, 7)))
        test_board._place_piece(pieces.Rook("black", (3, 7)))

        # Test that the game is not in stalemate for black and it is for white
        self.assertFalse(chess_logic.is_stalemate(test_board, "black"))
        self.assertTrue(chess_logic.is_stalemate(test_board, "white"))

    def test_is_legal_move(self):
        test_board = board.Board()

        test_board._place_piece(pieces.Rook("white", (0, 0)))

        # Test when the square is not occupied
        self.assertTrue(
            chess_logic.is_legal_move(
                test_board, test_board.get_piece_at_square((0, 0)), (5, 0)
            )
        )

        # Test when the square is occupied by a piece of different color
        test_board._place_piece(pieces.Rook("black", (5, 0)))
        self.assertTrue(
            chess_logic.is_legal_move(
                test_board, test_board.get_piece_at_square((0, 0)), (5, 0)
            )
        )

        # Test when the square is occupied by a piece of the same color
        test_board._remove_piece_at_square((5, 0))
        test_board._place_piece(pieces.Rook("white", (5, 0)))
        self.assertFalse(
            chess_logic.is_legal_move(
                test_board, test_board.get_piece_at_square((0, 0)), (5, 0)
            )
        )

        # Test that the same logic applies to knights (since they can jump over
        # pieces)
        test_board._remove_piece_at_square((5, 0))
        test_board._place_piece(pieces.Knight("white", (5, 0)))
        test_board._place_piece(pieces.Knight("white", (4, 2)))
        self.assertFalse(
            chess_logic.is_legal_move(
                test_board, test_board.get_piece_at_square((5, 0)), (4, 2)
            )
        )

        test_board._remove_piece_at_square((4, 2))
        test_board._place_piece(pieces.Knight("black", (4, 2)))
        self.assertTrue(
            chess_logic.is_legal_move(
                test_board, test_board.get_piece_at_square((5, 0)), (4, 2)
            )
        )

        # Test when the path is blocked by a piece of the same color

        # Vertically
        self.assertFalse(
            chess_logic.is_legal_move(
                test_board, test_board.get_piece_at_square((0, 0)), (7, 0)
            )
        )
        # Horizontally
        test_board._place_piece(pieces.Rook("white", (0, 1)))
        self.assertFalse(
            chess_logic.is_legal_move(
                test_board, test_board.get_piece_at_square((0, 0)), (0, 7)
            )
        )
        # Diagonally
        test_board._place_piece(pieces.Bishop("white", (1, 1)))
        test_board._place_piece(pieces.Bishop("white", (4, 4)))
        self.assertFalse(
            chess_logic.is_legal_move(
                test_board, test_board.get_piece_at_square((1, 1)), (7, 7)
            )
        )
        self.assertTrue(
            chess_logic.is_legal_move(
                test_board, test_board.get_piece_at_square((1, 1)), (3, 3)
            )
        )
