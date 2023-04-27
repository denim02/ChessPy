import unittest
from unittest.mock import patch, mock_open
from chess_game.game import ChessGame
from chess_game import board, pieces, constants

class TestChessGame(unittest.TestCase):
    def setUp(self):
        self.game = ChessGame()
        self.game.move_log_enabled = False

    def test_init(self):
        test_board = board.Board()
        test_board.populate_board()

        self.assertEqual(self.game.board.piece_list, test_board.piece_list)

        captured_pieces = {
            "white": [],
            "black": []
        }
        self.assertEqual(self.game.captured_pieces, captured_pieces)

        self.assertEqual(self.game.turn, "white")
        self.assertIsNone(self.game.promotion_choice)
        self.assertFalse(self.game.is_checkmate)
        self.assertFalse(self.game.is_stalemate)
        self.assertFalse(self.game.is_threefold_repetition)
        self.assertEqual(self.game.fifty_move_counter, 0)
        self.assertEqual(self.game.position_log, [self.game.get_current_game_position()])
        self.assertEqual(self.game.move_log_enabled, False)
        self.assertRegex(self.game.move_log_file_path, r"g_\d{6}_\d{4}\.txt")
        self.assertEqual(self.game.fullmove_counter, 0)
        self.assertEqual(self.game.halfmove_counter, 0)

    def test_make_move_errors(self):
        # No piece at position
        with self.assertRaises(TypeError) as e:
            self.game.make_move((4, 4), (5, 5))
        
        # Wrong color piece
        with self.assertRaises(Exception) as e:
            self.game.make_move((1, 0), (2, 0))

        # Illegal move
        with self.assertRaises(ValueError) as e:
            self.game.make_move((6, 0), (4, 4))

        # The move places the player's own king in check
        self.game.board._place_piece(
            pieces.Queen(color="black", position=(5, 2))
        )

        with self.assertRaises(Exception) as e:
            self.game.make_move((6, 3), (5, 3))

    def test_make_move_castle(self):
        self.game.board = board.Board()
        # Place white king and white queenside rook
        white_king = pieces.King(color="white", position=(7, 4))
        white_rook = pieces.Rook(color="white", position=(7, 0))
        self.game.board._place_piece(
            white_rook
        )
        self.game.board._place_piece(
            white_king
        )

        # Place black king and black kingside rook
        black_king = pieces.King(color="black", position=(0, 4))
        black_rook = pieces.Rook(color="black", position=(0, 7))
        self.game.board._place_piece(
            black_king
        )
        self.game.board._place_piece(
            black_rook
        )

        # Try to castle queenside (to the left)
        self.game.make_move((7, 4), (7, 2))
        self.assertEqual(self.game.board.get_piece_at_square((7, 2)), white_king)
        self.assertEqual(self.game.board.get_piece_at_square((7, 3)), white_rook)

        # Try to castle kingside (to the right)
        self.game.make_move((0, 4), (0, 6))
        self.assertEqual(self.game.board.get_piece_at_square((0, 6)), black_king)
        self.assertEqual(self.game.board.get_piece_at_square((0, 5)), black_rook)

        # Try king move that is not a castle
        self.game.make_move((7, 2), (6, 2))
        self.assertEqual(self.game.board.get_piece_at_square((6, 2)), white_king)
        self.assertEqual(self.game.board.get_piece_at_square((7, 3)), white_rook)

    def test_make_move_pawn_promotion(self):
        self.game.board = board.Board()

        # Place kings
        white_king = pieces.King(color="white", position=(7, 4))
        black_king = pieces.King(color="black", position=(1, 4))
        self.game.board._place_piece(
            white_king
        )
        self.game.board._place_piece(
            black_king
        )

        # Place white pawn
        white_pawn = pieces.Pawn(color="white", position=(1, 0))
        self.game.board._place_piece(
            white_pawn
        )

        # Test wrong promotion choice
        with self.assertRaises(ValueError) as e:
            self.game.promotion_choice = "F"
            self.game.make_move((1, 0), (0, 0))

        self.game.turn = "black"

        # Test promotion 
        black_pawn = pieces.Pawn(color="black", position=(6, 0))
        self.game.board._place_piece(
            black_pawn
        )
        self.game.promotion_choice = "Q"
        self.game.make_move((6, 0), (7, 0))
        self.assertEqual(self.game.board.get_piece_at_square((7, 0)).name, "Queen")
        self.assertIsNone(self.game.promotion_choice)

    def test_make_move_general(self):
        # Test move
        white_pawn = self.game.board.get_piece_at_square((6, 0))
        self.game.make_move((6, 0), (5, 0))
        self.assertEqual(self.game.board.get_piece_at_square((5, 0)), white_pawn)

    def test_make_move_captured_piece(self):
        # Place piece to be captured
        black_pawn = pieces.Pawn(color="black", position=(5, 0))
        self.game.board._place_piece(
            black_pawn
        )

        # Test captured piece
        self.assertEqual(self.game.captured_pieces["white"], [])
        self.game.make_move((6, 1), (5, 0))
        self.assertEqual(self.game.captured_pieces["white"], [black_pawn])
        self.assertEqual(self.game.captured_pieces["black"], [])

    def test_make_move_counters(self):
        # Test counters
        self.assertEqual(self.game.turn, "white")
        self.assertEqual(self.game.fullmove_counter, 0)
        self.assertEqual(self.game.halfmove_counter, 0)
        self.assertEqual(self.game.fifty_move_counter, 0)

        self.game.make_move((6, 0), (5, 0))
        self.assertEqual(self.game.turn, "black")
        self.assertEqual(self.game.fullmove_counter, 0)
        self.assertEqual(self.game.halfmove_counter, 1)
        self.assertEqual(self.game.fifty_move_counter, 0)

        self.game.make_move((1, 0), (2, 0))
        self.assertEqual(self.game.turn, "white")
        self.assertEqual(self.game.fullmove_counter, 1)
        self.assertEqual(self.game.halfmove_counter, 2)
        self.assertEqual(self.game.fifty_move_counter, 0)

        # Test fifty move counter
        self.game.make_move((7, 0), (6, 0))
        self.assertEqual(self.game.fifty_move_counter, 1)
        self.game.make_move((0, 0), (1, 0))
        self.assertEqual(self.game.fifty_move_counter, 2)
        self.game.make_move((6, 0), (7, 0))
        self.assertEqual(self.game.fifty_move_counter, 3)
        self.game.make_move((1, 0), (0, 0))
        self.assertEqual(self.game.fifty_move_counter, 4)

        # Pawn move resets fifty move counter
        self.game.make_move((5, 0), (4, 0))
        self.assertEqual(self.game.fifty_move_counter, 0)

        self.game.make_move((0, 0), (1, 0))
        self.game.make_move((7, 0), (6, 0))
        self.game.make_move((1, 0), (0, 0))
        self.assertEqual(self.game.fifty_move_counter, 3)

        # Capture resets fifty move counter
        self.game.board._place_piece(
            pieces.Pawn(color="black", position=(3, 1))
        )
        self.game.make_move((4, 0), (3, 1))
        self.assertEqual(self.game.fifty_move_counter, 0)

    def test_make_move_game_over_conditions(self):
        # Test checkmate
        self.game.board = board.Board.instantiate_from_fen(
            "./game/game_states/test_checkmate.fen"
        )
        self.assertFalse(self.game.is_checkmate)
        self.game.make_move((5, 6), (0, 6))
        self.assertTrue(self.game.is_checkmate)

        # Test stalemate
        self.game = ChessGame()
        self.game.move_log_enabled = False

        self.game.board = board.Board.instantiate_from_fen(
            "./game/game_states/test_stalemate.fen"
        )
        # Place random white piece to move
        self.game.board._place_piece(
            pieces.Pawn(color="white", position=(7, 0))
        )
        self.assertFalse(self.game.is_stalemate)
        self.game.make_move((7, 0), (6, 0))
        self.assertTrue(self.game.is_stalemate)

        # Test threefold repetition
        self.game = ChessGame()
        self.game.move_log_enabled = False
        # Move knights back and forth
        self.game.make_move((7, 1), (5, 0))
        self.game.make_move((0, 1), (2, 0))
        self.assertFalse(self.game.is_threefold_repetition)
        self.game.make_move((5, 0), (7, 1))
        self.game.make_move((2, 0), (0, 1))
        self.assertFalse(self.game.is_threefold_repetition)
        self.game.make_move((7, 1), (5, 0))
        self.game.make_move((0, 1), (2, 0))
        self.assertFalse(self.game.is_threefold_repetition)
        self.game.make_move((5, 0), (7, 1))
        self.game.make_move((2, 0), (0, 1))
        self.assertTrue(self.game.is_threefold_repetition)

    def test_make_move_position_log(self):
        # Test logging
        log = [self.game.get_current_game_position()]
        self.assertEqual(self.game.position_log, log)
        
        self.game.make_move((6, 0), (5, 0))
        log.append(self.game.get_current_game_position())
        self.assertEqual(self.game.position_log, log)

    def test_make_move_move_log_file(self):
        self.game.move_log_enabled = True
        with patch("builtins.open", mock_open()) as mock_file:
            self.game.make_move((6, 4), (4, 4))
            mock_file.assert_called_with(
                self.game.move_log_file_path, "a"
            )
            mock_file().write.assert_called_with("1. e4 ")

            self.game.make_move((1, 3), (3, 3))
            mock_file().write.assert_called_with("d5\n")

            self.game.make_move((4, 4), (3, 3))
            mock_file().write.assert_called_with("2. exd5 ")

    def test_get_current_game_position(self):
        start_state = {
            "piece_placement": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
            "turn": "w",
            "castling_availability": "KQkq",
            "en_passant_target_square": "-",
        }
        self.assertEqual(self.game.get_current_game_position(), start_state)

        # After moving white pawn to E4
        self.game.make_move((6, 4), (4, 4))
        state = {
            "piece_placement": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR",
            "turn": "b",
            "castling_availability": "KQkq",
            "en_passant_target_square": "e3",
        }
        self.assertEqual(self.game.get_current_game_position(), state)

    def test_check_threefold_repetition(self):
        self.game.make_move((6, 0), (5, 0))
        self.game.make_move((1, 0), (2, 0))
        self.assertFalse(self.game.check_threefold_repetition())
        self.game.make_move((7, 0), (6, 0))
        self.game.make_move((0, 0), (1, 0))
        self.assertFalse(self.game.check_threefold_repetition())
        self.game.make_move((6, 0), (7, 0))
        self.game.make_move((1, 0), (0, 0))
        self.assertFalse(self.game.check_threefold_repetition())
        self.game.make_move((7, 0), (6, 0))
        self.game.make_move((0, 0), (1, 0))
        self.assertFalse(self.game.check_threefold_repetition())
        self.game.make_move((6, 0), (7, 0))
        self.game.make_move((1, 0), (0, 0))
        self.assertFalse(self.game.check_threefold_repetition())
        self.game.make_move((7, 0), (6, 0))
        self.game.make_move((0, 0), (1, 0))
        self.assertTrue(self.game.check_threefold_repetition())

    def test_get_fen_game_state(self):
        start_state = {
            "piece_placement": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
            "turn": "w",
            "castling_availability": "KQkq",
            "en_passant_target_square": "-",
            "halfmove_clock": 0,
            "fullmove_counter": 0
        }
        self.assertEqual(self.game.get_fen_game_state(), start_state)

        # After moving white pawn to E4
        self.game.make_move((6, 4), (4, 4))
        state = {
            "piece_placement": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR",
            "turn": "b",
            "castling_availability": "KQkq",
            "en_passant_target_square": "e3",
            "halfmove_clock": 1,
            "fullmove_counter": 0
        }
        self.assertEqual(self.game.get_fen_game_state(), state)

    def test_log_move(self):
        self.game.move_log_enabled = True
        with patch("builtins.open", mock_open()) as mock_file:
            white_pawn = self.game.board.get_piece_at_square((6, 4))
            white_pawn.position = (4, 4)
            # Simulate movement
            self.game.halfmove_counter += 1

            # First move in round
            self.game.log_move(white_pawn, (6, 4))
            mock_file.assert_called_with(
                self.game.move_log_file_path, "a"
            )
            mock_file().write.assert_called_with("1. e4 ")

            # Second move in round
            black_pawn = self.game.board.get_piece_at_square((1, 3))
            self.game.turn = "black"
            self.game.halfmove_counter += 1
            black_pawn.position = (3, 3)
            self.game.log_move(black_pawn, (3, 3))
            mock_file().write.assert_called_with("d5\n")

    def test_get_move_in_algebraic_notation_castle(self):
        # Test castle queenside
        expected_result = "O-O-O"
        self.assertEqual(
            self.game.get_move_in_algebraic_notation(
                pieces.King(color="white", position=(7, 2)),
                (7, 4)
            ),
            expected_result
        )

        # Test castle kingside
        expected_result = "O-O"
        self.assertEqual(
            self.game.get_move_in_algebraic_notation(
                pieces.King(color="white", position=(7, 6)),
                (7, 4)
            ),
            expected_result
        )

    def test_get_move_in_algebraic_notation_pawn_promotion(self):
        expected_result = "a8=Q"
        # Create new board
        self.game.board = board.Board()

        piece = pieces.Pawn(color="white", position=(1, 0))
        self.game.board._place_piece(
            piece
        )
        self.game.board._place_piece(
            pieces.King(color="black", position=(3, 2))
        )
        self.game.board._place_piece(
            pieces.King(color="white", position=(7, 0))
        )
        
        self.game.promotion_choice = "Q"
        self.game.make_move((1, 0), (0, 0))

        self.assertEqual(
            self.game.get_move_in_algebraic_notation(
                piece,
                (1, 0)
            ),
            expected_result
        )

    def test_get_move_in_algebraic_notation_pawn_capture(self):
        expected_result = "cxb6"

        white_pawn = pieces.Pawn(color="white", position=(2, 1))
        black_pawn = pieces.Pawn(color="black", position=(2, 1))

        # Create new board
        self.game.board = board.Board()
        self.game.board._place_piece(
            white_pawn
        )
        self.game.board._place_piece(
            pieces.King(color="black", position=(3, 2))
        )
        self.game.board._place_piece(
            pieces.King(color="white", position=(7, 0))
        )

        self.assertEqual(
            self.game.get_move_in_algebraic_notation(
                white_pawn,
                (3, 2),
                black_pawn
            ),
            expected_result
        )

    def test_get_move_in_algebraic_notation_en_passant_capture(self):
        expected_result = "cxb7e.p."

        white_pawn = pieces.Pawn(color="white", position=(1, 1))
        black_pawn = pieces.Pawn(color="black", position=(2, 1))

        # Create new board
        self.game.board = board.Board()
        self.game.board._place_piece(
            white_pawn
        )
        self.game.board._place_piece(
            pieces.King(color="black", position=(3, 2))
        )
        self.game.board._place_piece(
            pieces.King(color="white", position=(7, 0))
        )

        self.assertEqual(
            self.game.get_move_in_algebraic_notation(
                white_pawn,
                (2, 2),
                black_pawn
            ),
            expected_result
        )

    def test_get_move_in_algebraic_notation_regular_capture(self):
        expected_result = "Rxb7"

        white_rook = pieces.Rook(color="white", position=(1, 1))
        black_pawn = pieces.Pawn(color="black", position=(2, 1))

        # Create new board
        self.game.board = board.Board()
        self.game.board._place_piece(
            white_rook
        )
        self.game.board._place_piece(
            pieces.King(color="black", position=(3, 2))
        )
        self.game.board._place_piece(
            pieces.King(color="white", position=(7, 0))
        )

        self.assertEqual(
            self.game.get_move_in_algebraic_notation(
                white_rook,
                (2, 2),
                black_pawn
            ),
            expected_result
        )

    def test_get_move_in_algebraic_notation_pawn_move(self):
        expected_result = "e4"

        white_pawn = pieces.Pawn(color="white", position=(4, 4))
        
        self.assertEqual(
            self.game.get_move_in_algebraic_notation(
                white_pawn,
                (6, 4)
            ),
            expected_result
        )

    def test_get_move_in_algebraic_notation_regular_move(self):
        expected_result = "Re4"

        white_rook = pieces.Rook(color="white", position=(4, 4))
        
        self.assertEqual(
            self.game.get_move_in_algebraic_notation(
                white_rook,
                (6, 4)
            ),
            expected_result
        )

    def test_get_move_in_algebraic_notation_regular_move_with_check(self):
        expected_result = "Re5+"

        rook = pieces.Rook(color="white", position=(3, 4))
        
        # Create new board
        self.game.board = board.Board()
        self.game.turn = "black"
        self.game.board._place_piece(
            rook
        )
        self.game.board._place_piece(
            pieces.King(color="black", position=(3, 2))
        )
        self.game.board._place_piece(
            pieces.King(color="white", position=(7, 0))
        )

        self.assertEqual(
            self.game.get_move_in_algebraic_notation(
                rook,
                (6, 4)
            ),
            expected_result
        )
    
    def test_get_move_in_algebraic_notation_regular_move_with_checkmate(self):
        expected_result = "Rg8#"
        
        rook = pieces.Rook(color="white", position=(0, 6))

        # Create new board
        self.game.board = board.Board().instantiate_from_fen(
            "./game/game_states/test_checkmate.fen"
        )
        self.game.turn = "black"
        self.game.board._place_piece(
            rook
        )

        self.assertEqual(
            self.game.get_move_in_algebraic_notation(
                rook,
                (5, 6)
            ),
            expected_result
        )

if __name__ == "__main__":
    unittest.main()


