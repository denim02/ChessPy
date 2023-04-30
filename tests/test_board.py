import unittest
import unittest.mock
import io
from chess_game import pieces, board, constants


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.board.populate_board()

    def test_init(self):
        self.board = board.Board()
        self.assertEqual(len(self.board._Board__board_table), 8)
        self.assertEqual(len(self.board._Board__board_table[0]), 8)
        self.assertEqual(self.board.piece_list, ())
        self.assertEqual(self.board.last_piece_captured, None)

    def test_populate_board(self):
        self.assertEqual(len(self.board.piece_list), 32)
        self.assertEqual(self.board._Board__board_table[7][0].name, "Rook")
        self.assertEqual(self.board._Board__board_table[7][0].color, "white")

    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_populate_board_init_file_missing(self, mock_stdout):
        # Change init file path in constants to one that doesn't exist
        old_init_file = constants.STARTING_FEN_FILE
        constants.STARTING_FEN_FILE = "nonexistent_file.txt"
        new_board = board.Board()
        new_board.populate_board()

        # Check that the board is still populated with the pieces of a standard
        # game
        self.assertEqual(new_board._Board__board_table, self.board._Board__board_table)
        self.assertEqual(new_board.piece_list, self.board.piece_list)

        # Check that the error message is printed
        self.assertEqual(
            mock_stdout.getvalue(),
            "Starting FEN file not found! Using default starting position.\n",
        )

        # Reset the constants file
        constants.STARTING_FEN_FILE = old_init_file

    def test_board_piece_list(self):
        self.assertEqual(len(self.board.piece_list), 32)
        self.assertEqual(self.board.piece_list[0].name, "Rook")
        self.assertEqual(self.board.piece_list[0].color, "black")

    def test_refresh_legal_moves(self):
        self.assertEqual(self.board.get_piece_at_square((7, 4)).legal_moves, ())
        self.board._remove_piece_at_square((6, 4))
        self.board._Board__refresh_legal_moves()
        self.assertEqual(self.board.get_piece_at_square((7, 4)).legal_moves, ((6, 4),))

    def test_get_piece_at_square(self):
        self.assertEqual(self.board.get_piece_at_square((7, 0)).name, "Rook")
        self.assertEqual(self.board.get_piece_at_square((7, 0)).color, "white")
        self.assertEqual(self.board.get_piece_at_square((0, 7)).name, "Rook")
        self.assertEqual(self.board.get_piece_at_square((0, 7)).color, "black")

    def test_get_piece_at_square_out_of_bounds(self):
        self.assertEqual(self.board.get_piece_at_square((8, 0)), None)
        self.assertEqual(self.board.get_piece_at_square((0, 8)), None)
        self.assertEqual(self.board.get_piece_at_square((-1, 0)), None)
        self.assertEqual(self.board.get_piece_at_square((0, -1)), None)

    def test_place_piece(self):
        self.board._place_piece(pieces.Pawn("white", (4, 4)))
        self.assertEqual(self.board.get_piece_at_square((4, 4)).name, "Pawn")
        self.assertEqual(self.board.get_piece_at_square((4, 4)).color, "white")

    def test_place_piece_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.board._place_piece(pieces.Pawn("white", (8, 4)))

    def test_place_piece_at_square_already_occupied(self):
        with self.assertRaises(ValueError):
            self.board._place_piece(pieces.Pawn("white", (7, 0)))

    def test_remove_piece_at_square(self):
        self.board._remove_piece_at_square((7, 0))
        self.assertEqual(self.board.get_piece_at_square((7, 0)), None)

    def test_remove_piece_at_square_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.board._remove_piece_at_square((8, 4))

    def test_remove_piece_at_square_already_empty(self):
        # Should not raise an error
        try:
            self.board._remove_piece_at_square((5, 0))
        except Exception:
            self.fail("Should not raise an error")

    def test_move_piece_to_square(self):
        piece = self.board.get_piece_at_square((7, 0))

        # Move piece to empty square
        self.board._remove_piece_at_square((6, 0))
        piece_has_moved = piece.has_moved
        self.board.move_piece_to_square(piece, (6, 0))
        self.assertNotEqual(piece.has_moved, piece_has_moved)
        self.assertTrue(piece.has_moved)
        self.assertEqual(self.board.get_piece_at_square((6, 0)).name, "Rook")
        self.assertEqual(self.board.get_piece_at_square((6, 0)).color, "white")
        self.assertEqual(self.board.get_piece_at_square((7, 0)), None)

        # Move piece to occupied square
        self.board.move_piece_to_square(piece, (1, 0))
        self.assertEqual(self.board.get_piece_at_square((1, 0)).name, "Rook")
        self.assertEqual(self.board.get_piece_at_square((1, 0)).color, "white")
        self.assertEqual(self.board.get_piece_at_square((7, 0)), None)
        self.assertEqual(self.board.last_piece_captured.name, "Pawn")
        self.assertEqual(self.board.last_piece_captured.color, "black")
        self.assertNotIn(self.board.last_piece_captured, self.board.piece_list)

        # Move piece after capture
        self.board.move_piece_to_square(piece, (3, 0))
        self.assertEqual(self.board.get_piece_at_square((3, 0)), piece)
        self.assertEqual(self.board.get_piece_at_square((1, 0)), None)
        self.assertEqual(self.board.last_piece_captured, None)

    def test_move_piece_to_square_out_of_bounds(self):
        piece = self.board.get_piece_at_square((7, 0))
        with self.assertRaises(ValueError):
            self.board.move_piece_to_square(piece, (8, 0))

    def test_move_piece_to_square_en_passant_attr(self):
        # Initialize almost empty board
        self.board = board.Board()
        self.board._place_piece(pieces.Pawn("white", (5, 4)))
        self.board._place_piece(pieces.Pawn("black", (3, 3)))

        # Check the side-effects of moving a pawn two rows forward (do not need to keep track of has_moved)
        # That would be done by generate_possible_moves()
        self.board.move_piece_to_square(
            self.board.get_piece_at_square((5, 4)), (3, 4), change_en_passant=False
        )
        self.assertIsNone(self.board.en_passant_piece)
        self.board.move_piece_to_square(
            self.board.get_piece_at_square((3, 4)), (5, 4), change_en_passant=False
        )

        self.board.move_piece_to_square(
            self.board.get_piece_at_square((5, 4)), (3, 4), change_en_passant=True
        )
        self.assertEqual(
            self.board.en_passant_piece, self.board.get_piece_at_square((3, 4))
        )

        # Do additional move to clear en passant
        self.board.move_piece_to_square(
            self.board.get_piece_at_square((3, 4)), (2, 4), change_en_passant=True
        )
        self.assertIsNone(self.board.en_passant_piece)

    def test_move_piece_to_square_en_passant(self):
        # Initialize almost empty board
        self.board = board.Board()
        self.board._place_piece(pieces.Pawn("white", (5, 4)))
        self.board._place_piece(pieces.Pawn("black", (3, 3)))

        # Test en passant capture with white pawn
        capturing_piece = self.board.get_piece_at_square((5, 4))
        captured_piece = self.board.get_piece_at_square((3, 3))
        self.board.move_piece_to_square(
            self.board.get_piece_at_square((3, 3)), (5, 3), change_en_passant=True
        )
        self.board.move_piece_to_square(
            self.board.get_piece_at_square((5, 4)), (4, 3), change_en_passant=True
        )
        self.assertEqual(self.board.get_piece_at_square((5, 3)), None)
        self.assertEqual(self.board.get_piece_at_square((4, 3)), capturing_piece)
        self.assertEqual(self.board.last_piece_captured, captured_piece)

        self.board = board.Board()
        self.board._place_piece(pieces.Pawn("white", (5, 4)))
        self.board._place_piece(pieces.Pawn("black", (3, 3)))

        # Test en passant capture with black pawn
        capturing_piece = self.board.get_piece_at_square((3, 3))
        captured_piece = self.board.get_piece_at_square((5, 4))
        self.board.move_piece_to_square(
            self.board.get_piece_at_square((5, 4)), (3, 4), change_en_passant=True
        )
        self.board.move_piece_to_square(
            self.board.get_piece_at_square((3, 3)), (4, 4), change_en_passant=True
        )
        self.assertEqual(self.board.get_piece_at_square((3, 4)), None)
        self.assertEqual(self.board.get_piece_at_square((4, 4)), capturing_piece)
        self.assertEqual(self.board.last_piece_captured, captured_piece)

    def test_revert_move(self):
        piece = self.board.get_piece_at_square((7, 0))
        self.board._remove_piece_at_square((6, 0))
        self.board.move_piece_to_square(piece, (6, 0))
        self.board.revert_move(piece, (7, 0))
        self.assertEqual(self.board.get_piece_at_square((7, 0)).name, "Rook")
        self.assertEqual(self.board.get_piece_at_square((7, 0)).color, "white")
        self.assertEqual(self.board.get_piece_at_square((6, 0)), None)

        # Move piece to occupied square
        self.assertIsNotNone(self.board.get_piece_at_square((1, 0)))
        self.assertIsNone(self.board.last_piece_captured)
        self.board.move_piece_to_square(piece, (1, 0))
        self.assertIsNone(self.board.get_piece_at_square((7, 0)))
        self.assertIsNotNone(self.board.get_piece_at_square((1, 0)))
        self.assertIsNotNone(self.board.last_piece_captured)
        self.assertNotIn(self.board.last_piece_captured, self.board.piece_list)
        self.board.revert_move(piece, (7, 0))
        self.assertIsNotNone(self.board.get_piece_at_square((7, 0)))
        self.assertIsNotNone(self.board.get_piece_at_square((1, 0)))
        self.assertIsNone(self.board.last_piece_captured)
        self.assertNotIn(self.board.last_piece_captured, self.board.piece_list)

    def test_promote_pawn(self):
        test_board = board.Board()
        test_board._place_piece(pieces.Pawn("white", (0, 0)))
        test_board._place_piece(pieces.Pawn("black", (7, 0)))
        test_board._place_piece(pieces.Pawn("white", (0, 2)))
        test_board._place_piece(pieces.Pawn("black", (7, 2)))

        # Test promotion on invalid piece
        test_board._place_piece(pieces.Rook("white", (0, 1)))
        with self.assertRaises(ValueError):
            test_board.promote_pawn(test_board.get_piece_at_square((0, 1)), "Q")

        # Test promotion with invalid choice
        with self.assertRaises(ValueError):
            test_board.promote_pawn(test_board.get_piece_at_square((0, 0)), "Invalid")

        # Test promotion on invalid square
        test_board._place_piece(pieces.Pawn("white", (1, 1)))
        test_board._place_piece(pieces.Pawn("black", (6, 1)))
        with self.assertRaises(ValueError):
            test_board.promote_pawn(test_board.get_piece_at_square((1, 1)), "Q")
        with self.assertRaises(ValueError):
            test_board.promote_pawn(test_board.get_piece_at_square((6, 1)), "Q")

        # Test promotion to queen
        test_board.promote_pawn(test_board.get_piece_at_square((7, 0)), "Q")
        self.assertEqual(test_board.get_piece_at_square((7, 0)).name[0], "Q")
        self.assertEqual(test_board.get_piece_at_square((7, 0)).color, "black")

        # Test promotion to rook
        test_board.promote_pawn(test_board.get_piece_at_square((0, 0)), "R")
        self.assertEqual(test_board.get_piece_at_square((0, 0)).name[0], "R")
        self.assertEqual(test_board.get_piece_at_square((0, 0)).color, "white")

        # Test promotion to bishop
        test_board.promote_pawn(test_board.get_piece_at_square((7, 2)), "B")
        self.assertEqual(test_board.get_piece_at_square((7, 2)).name[0], "B")
        self.assertEqual(test_board.get_piece_at_square((7, 2)).color, "black")

        # Test promotion to knight
        test_board.promote_pawn(test_board.get_piece_at_square((0, 2)), "N")
        self.assertEqual(
            test_board.get_piece_at_square((0, 2)).to_algebraic_notation()[0].upper(),
            "N",
        )
        self.assertEqual(test_board.get_piece_at_square((0, 2)).color, "white")

    def test_is_square_occupied(self):
        self.assertTrue(self.board.is_square_occupied((7, 0)))
        self.assertFalse(self.board.is_square_occupied((5, 0)))

    def test_is_square_occupied_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.board.is_square_occupied((8, 0))

    def test_is_square_attacked(self):
        self.board._remove_piece_at_square((6, 0))
        self.assertTrue(self.board.is_square_attacked((1, 0), "black"))
        self.assertFalse(self.board.is_square_attacked((7, 0), "white"))

    def test_is_square_attacked_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.board.is_square_attacked((8, 0), "white")

    def test_is_horizontal_path_attacked(self):
        self.board._remove_piece_at_square((1, 0))
        self.assertTrue(self.board.is_horizontal_path_attacked((6, 0), (6, 5), "white"))
        self.assertFalse(
            self.board.is_horizontal_path_attacked((1, 0), (1, 5), "black")
        )

    def test_is_horizontal_path_blocked(self):
        self.assertTrue(self.board.is_path_blocked((6, 0), (6, 5)))
        self.assertFalse(self.board.is_path_blocked((2, 0), (2, 5)))

    def test_is_vertical_path_blocked(self):
        self.assertTrue(self.board.is_path_blocked((0, 0), (5, 0)))
        self.assertFalse(self.board.is_path_blocked((3, 0), (5, 0)))

    def test_is_diagonal_path_blocked(self):
        self.assertTrue(self.board.is_path_blocked((0, 0), (7, 7)))
        self.assertFalse(self.board.is_path_blocked((3, 0), (5, 2)))

    def test_instantiate_from_fen(self):
        test_fen_board = board.Board.instantiate_from_fen_file(
            "./game/game_states/test_stalemate.fen"
        )
        test_board = board.Board()
        test_board._place_piece(pieces.King("black", (0, 5)))
        test_board._place_piece(pieces.Pawn("white", (1, 5)))
        test_board._place_piece(pieces.King("white", (2, 5)))

        self.assertEqual(
            test_fen_board._Board__board_table, test_board._Board__board_table
        )
        self.assertEqual(test_fen_board.piece_list, test_board.piece_list)

    def test_repr(self):
        expected_board = (
            "  a b c d e f g h \n"
            "8 r n b q k b n r 8\n"
            "7 p p p p p p p p 7\n"
            "6 . . . . . . . . 6\n"
            "5 . . . . . . . . 5\n"
            "4 . . . . . . . . 4\n"
            "3 . . . . . . . . 3\n"
            "2 P P P P P P P P 2\n"
            "1 R N B Q K B N R 1\n"
            "  a b c d e f g h \n"
        )

        self.assertEqual(repr(self.board), expected_board)

    def test_get_algebraic_notation(self):
        self.assertEqual(self.board.get_algebraic_notation((0, 0)), "a8")
        self.assertEqual(self.board.get_algebraic_notation((7, 7)), "h1")

    def test_get_algebraic_notation_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.board.get_algebraic_notation((8, 0))

    def test_get_square_from_algebraic_notation(self):
        self.assertEqual(self.board.get_square_from_algebraic_notation("a8"), (0, 0))
        self.assertEqual(self.board.get_square_from_algebraic_notation("h1"), (7, 7))

    def test_parse_fen(self):
        test_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        new_board = self.board.parse_fen(test_fen)
        expected_board = board.Board()
        expected_board.populate_board()

        self.assertListEqual(new_board, expected_board._Board__board_table)

    def test_parse_fen_from_file(self):
        test_fen_path = "./game/game_states/test_parse.fen"
        new_board = self.board.parse_fen_from_file(test_fen_path)
        expected_board = board.Board()

        for i in range(4):
            expected_board._place_piece(pieces.Pawn("black", (1, i)))

        self.assertEqual(repr(new_board), repr(expected_board._Board__board_table))

        # Test when the file does not exist
        with self.assertRaises(FileNotFoundError):
            self.board.parse_fen_from_file("does_not_exist.fen")

    def test_get_fen_board_state(self):
        expected_output = {
            "piece_placement": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
            "castling_availability": "KQkq",
            "en_passant_target_square": "-",
        }

        actual_output = self.board.get_fen_board_state()
        self.assertEqual(actual_output, expected_output)

    def test_get_fen_board(self):
        expected_output = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        actual_output = self.board._get_fen_board()
        self.assertEqual(actual_output, expected_output)

        self.board.move_piece_to_square(self.board.get_piece_at_square((1, 0)), (3, 0))
        expected_output = "rnbqkbnr/1ppppppp/8/p7/8/8/PPPPPPPP/RNBQKBNR"
        actual_output = self.board._get_fen_board()
        self.assertEqual(actual_output, expected_output)

    def test_get_fen_castling_rights(self):
        # Total castling rights
        expected_output = "KQkq"
        actual_output = self.board._get_fen_castling_rights()
        self.assertEqual(actual_output, expected_output)

        # No castling rights for white
        self.board.get_piece_at_square((0, 4)).has_moved = True
        expected_output = "KQ"
        actual_output = self.board._get_fen_castling_rights()
        self.assertEqual(actual_output, expected_output)

        # No castling rights at all
        self.board.get_piece_at_square((7, 4)).has_moved = True
        expected_output = "-"
        actual_output = self.board._get_fen_castling_rights()
        self.assertEqual(actual_output, expected_output)

    def test_get_fen_en_passant_target_square(self):
        # No en passant target square
        expected_output = "-"
        actual_output = self.board._get_fen_en_passant_target_square()
        self.assertEqual(actual_output, expected_output)

        # En passant target square
        self.board.move_piece_to_square(self.board.get_piece_at_square((1, 4)), (3, 4))
        expected_output = "e6"
        actual_output = self.board._get_fen_en_passant_target_square()
        self.assertEqual(actual_output, expected_output)


if __name__ == "__main__":
    unittest.main()
