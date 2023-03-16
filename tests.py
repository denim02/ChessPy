import unittest
from chess_game import pieces, chess_logic, board, constants

class TestPiece(unittest.TestCase):
    def setUp(self):
        self.piece = pieces.Piece(name="Test Piece", value=10, color="black", position=(0, 0))
        self.board = board.Board()
        self.board.place_piece(self.piece)

    def test_init(self):
        self.assertEqual(self.piece.name, "Test Piece")
        self.assertEqual(self.piece.value, 10)
        self.assertEqual(self.piece.color, "black")
        self.assertEqual(self.piece.position, (0, 0))
        self.assertIsNone(self.piece.image)
        self.assertEqual(self.piece.coords, (0, 0))
        self.assertEqual(self.piece.legal_moves, set())

    def test_color(self):
        self.assertEqual(self.piece.color, "black")

    def test_coords(self):
        self.assertEqual(self.piece.coords, (0, 0))
        self.piece.coords = (100, 200)
        self.assertEqual(self.piece.coords, (100, 200))

    def test_position(self):
        self.assertEqual(self.piece.position, (0, 0))
        self.piece.position = (7, 7)
        self.assertEqual(self.piece.position, (7, 7))
        with self.assertRaises(ValueError):
            self.piece.position = (-1, 0)
        with self.assertRaises(ValueError):
            self.piece.position = (8, 0)

    def test_refresh_coords(self):
        self.assertEqual(self.piece.coords, (0, 0))
        self.piece.position = (4, 2)
        self.piece.refresh_coords()
        self.assertEqual(self.piece.coords, (2 * constants.SQUARE_SIZE, 4 * constants.SQUARE_SIZE))

    def test_legal_moves(self):
        self.assertEqual(self.piece.legal_moves, set())

    def test_generate_possible_moves(self):
        possible_moves = self.piece.generate_possible_moves(board)
        self.assertEqual(possible_moves, set())

    def test_refresh_legal_moves(self):
        self.piece.refresh_legal_moves(board)
        self.assertEqual(self.piece.legal_moves, set())

    def test_generate_legal_moves(self):
        legal_moves = self.piece.generate_legal_moves(board)
        self.assertEqual(legal_moves, set())

    def test_from_algebraic_notation(self):
        position = (0, 0)
        piece = pieces.Piece.from_algebraic_notation("P", position)
        self.assertIsInstance(piece, pieces.Pawn)
        self.assertEqual(piece.name, "Pawn")
        self.assertEqual(piece.value, 1)
        self.assertEqual(piece.color, "white")
        self.assertEqual(piece.position, position)

        with self.assertRaises(ValueError):
            pieces.Piece.from_algebraic_notation("X", position)

    def test_to_algebraic_notation(self):
        piece = pieces.Piece(name="Pawn", value=1, color="white", position=(0, 0))
        self.assertEqual(piece.to_algebraic_notation(), "P")

    def test_repr(self):
        self.assertEqual(repr(self.piece), "Black Test Piece")
