import unittest
from chess_game import pieces, board, chess_logic, constants

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.board.populate_board()

    def test_init(self):
        self.board = board.Board()
        self.assertEqual(len(self.board._Board__board_table), 8)
        self.assertEqual(len(self.board._Board__board_table[0]), 8)
        self.assertEqual(self.board.piece_list, [])
        self.assertEqual(self.board.last_piece_captured, None)

    def test_populate_board(self):
        self.assertEqual(len(self.board.piece_list), 32)
        self.assertEqual(self.board._Board__board_table[7][0].name, 'Rook')
        self.assertEqual(self.board._Board__board_table[7][0].color, 'white')

    def test_board_piece_list(self):
        self.assertEqual(len(self.board.piece_list), 32)
        self.assertEqual(self.board.piece_list[0].name, 'Rook')
        self.assertEqual(self.board.piece_list[0].color, 'black')

    def test_refresh_legal_moves(self):
        self.assertEqual(self.board.get_piece_at_square((7,4)).legal_moves, set())
        self.board._remove_piece_at_square((6, 4))
        self.board.refresh_legal_moves()
        self.assertEqual(self.board.get_piece_at_square((7,4)).legal_moves, {(6,4)})
    
    def test_get_piece_at_square(self):
        self.assertEqual(self.board.get_piece_at_square((7,0)).name, 'Rook')
        self.assertEqual(self.board.get_piece_at_square((7,0)).color, 'white')
        self.assertEqual(self.board.get_piece_at_square((0,7)).name, 'Rook')
        self.assertEqual(self.board.get_piece_at_square((0,7)).color, 'black')

    def test_get_piece_at_square_out_of_bounds(self):
        self.assertEqual(self.board.get_piece_at_square((8,0)), None)
        self.assertEqual(self.board.get_piece_at_square((0,8)), None)
        self.assertEqual(self.board.get_piece_at_square((-1,0)), None)
        self.assertEqual(self.board.get_piece_at_square((0,-1)), None)

    def test_place_piece(self):
        self.board._place_piece(pieces.Pawn('white', (4,4)))
        self.assertEqual(self.board.get_piece_at_square((4,4)).name, 'Pawn')
        self.assertEqual(self.board.get_piece_at_square((4,4)).color, 'white')

    def test_place_piece_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.board._place_piece(pieces.Pawn('white', (8,4)))

    def test_place_piece_at_square_already_occupied(self):
        with self.assertRaises(ValueError):
            self.board._place_piece(pieces.Pawn('white', (7,0)))

    def test_remove_piece_at_square(self):
        self.board._remove_piece_at_square((7,0))
        self.assertEqual(self.board.get_piece_at_square((7,0)), None)

    def test_remove_piece_at_square_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.board._remove_piece_at_square((8,4))

    def test_remove_piece_at_square_already_empty(self):
        # Should not raise an error
        try:
            self.board._remove_piece_at_square((5,0))
        except Exception:
            self.fail("Should not raise an error")

    def test_move_piece_to_square(self):
        piece = self.board.get_piece_at_square((7,0))

        # Move piece to empty square
        self.board._remove_piece_at_square((6, 0))
        self.board.move_piece_to_square(piece, (6,0))
        self.assertEqual(self.board.get_piece_at_square((6, 0)).name, 'Rook')
        self.assertEqual(self.board.get_piece_at_square((6, 0)).color, 'white')
        self.assertEqual(self.board.get_piece_at_square((7, 0)), None)

        # Move piece to occupied square
        self.board.move_piece_to_square(piece, (1, 0))
        self.assertEqual(self.board.get_piece_at_square((1,0)).name, 'Rook')
        self.assertEqual(self.board.get_piece_at_square((1,0)).color, 'white')
        self.assertEqual(self.board.get_piece_at_square((7,0)), None)
        self.assertEqual(self.board.last_piece_captured.name, 'Pawn')
        self.assertEqual(self.board.last_piece_captured.color, 'black')
        self.assertNotIn(self.board.last_piece_captured, self.board.piece_list)

        # Move piece after capture
        self.board.move_piece_to_square(piece, (3, 0))
        self.assertEqual(self.board.get_piece_at_square((3,0)), piece)
        self.assertEqual(self.board.get_piece_at_square((1,0)), None)
        self.assertEqual(self.board.last_piece_captured, None)

    def test_move_piece_to_square_out_of_bounds(self):
        piece = self.board.get_piece_at_square((7,0))
        with self.assertRaises(ValueError):
            self.board.move_piece_to_square(piece, (8,0))

    def test_move_none_piece_to_square(self):
        with self.assertRaises(ValueError):
            self.board.move_piece_to_square(None, (6,0))

    def test_revert_move(self):
        piece = self.board.get_piece_at_square((7,0))
        self.board._remove_piece_at_square((6, 0))
        self.board.move_piece_to_square(piece, (6,0))
        self.board.revert_move(piece, (7, 0))
        self.assertEqual(self.board.get_piece_at_square((7,0)).name, 'Rook')
        self.assertEqual(self.board.get_piece_at_square((7,0)).color, 'white')
        self.assertEqual(self.board.get_piece_at_square((6,0)), None)

        # Move piece to occupied square
        self.assertIsNotNone(self.board.get_piece_at_square((1,0)))
        self.assertIsNone(self.board.last_piece_captured)
        self.board.move_piece_to_square(piece, (1, 0))
        self.assertIsNone(self.board.get_piece_at_square((7,0)))
        self.assertIsNotNone(self.board.get_piece_at_square((1,0)))
        self.assertIsNotNone(self.board.last_piece_captured)
        self.assertNotIn(self.board.last_piece_captured, self.board.piece_list)
        self.board.revert_move(piece, (7, 0))
        self.assertIsNotNone(self.board.get_piece_at_square((7,0)))
        self.assertIsNotNone(self.board.get_piece_at_square((1,0)))
        self.assertIsNone(self.board.last_piece_captured)
        self.assertNotIn(self.board.last_piece_captured, self.board.piece_list)
        
    def test_is_square_occupied(self):
        self.assertTrue(self.board.is_square_occupied((7,0)))
        self.assertFalse(self.board.is_square_occupied((5,0)))

    def test_is_square_occupied_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.board.is_square_occupied((8,0))

    def test_is_square_attacked(self):
        self.board._remove_piece_at_square((6, 0))
        self.assertTrue(self.board.is_square_attacked((1,0), 'black'))
        self.assertFalse(self.board.is_square_attacked((7,0), 'white'))

    def test_is_square_attacked_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.board.is_square_attacked((8,0), 'white')

    def test_is_horizontal_path_attacked(self):
        self.board._remove_piece_at_square((1, 0))
        self.assertTrue(self.board.is_horizontal_path_attacked((6,0), (6,5), "white"))
        self.assertFalse(self.board.is_horizontal_path_attacked((1,0), (1,5), "black"))
    
    def test_is_horizontal_path_blocked(self):
        self.assertTrue(self.board.is_path_blocked((6,0), (6,5)))
        self.assertFalse(self.board.is_path_blocked((2,0), (2,5)))

    def test_is_vertical_path_blocked(self):
        self.assertTrue(self.board.is_path_blocked((0,0), (5,0)))
        self.assertFalse(self.board.is_path_blocked((3,0), (5,0)))

    def test_is_diagonal_path_blocked(self):
        self.assertTrue(self.board.is_path_blocked((0,0), (7,7)))
        self.assertFalse(self.board.is_path_blocked((3,0), (5,2)))

    def test_repr(self):
        expected_board ="  a b c d e f g h \n" \
                        "8 r n b q k b n r 8\n" \
                        "7 p p p p p p p p 7\n" \
                        "6 . . . . . . . . 6\n" \
                        "5 . . . . . . . . 5\n" \
                        "4 . . . . . . . . 4\n" \
                        "3 . . . . . . . . 3\n" \
                        "2 P P P P P P P P 2\n" \
                        "1 R N B Q K B N R 1\n" \
                        "  a b c d e f g h \n"

        self.assertEqual(repr(self.board), expected_board)

if __name__ == '__main__':
    unittest.main()