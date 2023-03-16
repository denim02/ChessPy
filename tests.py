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
        self.piece.color = "white"
        self.assertEqual(self.piece.color, "white")
        with self.assertRaises(ValueError):
            self.piece.color = "blue"

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

class TestPawn(unittest.TestCase):
    def setUp(self):
        self.pawn = pieces.Pawn(color="white", position=(6, 0))
        self.board = board.Board()
        self.board.place_piece(self.pawn)

    def test_init(self):
        self.assertEqual(self.pawn.name, "Pawn")
        self.assertEqual(self.pawn.value, 1)
        self.assertEqual(self.pawn.color, "white")
        self.assertEqual(self.pawn.position, (6, 0))
        self.assertIsNone(self.pawn.image)
        self.assertEqual(self.pawn.coords, (0, 6 * constants.SQUARE_SIZE))
        self.assertEqual(self.pawn.legal_moves, set())

    def test_generate_possible_moves(self):
        # Test white pawn with no pieces in front of it at start
        possible_moves = self.pawn.generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(5, 0), (4, 0)})

        # Test white pawn that moved
        self.pawn.position = (3, 0)
        possible_moves = self.pawn.generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(2, 0)})

        # Test white pawn with potential capture
        self.pawn.position = (4, 4)
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(3, 3)))
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(3, 5)))
        possible_moves = self.pawn.generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(3, 4), (3, 3), (3, 5)})
        self.board.remove_piece_at_square((3, 3))
        self.board.remove_piece_at_square((3, 5))

        # Test black pawn with no pieces in front of it at start
        self.pawn.color = "black"
        self.pawn.position = (1, 0)
        possible_moves = self.pawn.generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(2, 0), (3, 0)})

        # Test black pawn that moved
        self.pawn.position = (3, 0)
        possible_moves = self.pawn.generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(4, 0)})
        
        # Test black pawn with potential capture
        self.pawn.position = (4, 4)
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(5, 5)))
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(5, 3)))
        possible_moves = self.pawn.generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(5, 4), (5, 5), (5, 3)})
        self.board.remove_piece_at_square((5, 5))
        self.board.remove_piece_at_square((5, 3))

    def test_generate_legal_moves(self):
        # Test white pawn with no pieces in front of it at start
        legal_moves = self.pawn.generate_legal_moves(self.board)
        self.assertEqual(legal_moves, {(5, 0), (4, 0)})

        # Test white pawn that moved
        self.pawn.position = (3, 0)
        legal_moves = self.pawn.generate_legal_moves(self.board)
        self.assertEqual(legal_moves, {(2, 0)})

        # Test white pawn with potential capture
        self.pawn.position = (4, 4)
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(3, 3)))
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(3, 5)))
        legal_moves = self.pawn.generate_legal_moves(self.board)
        self.assertEqual(legal_moves, {(3, 4), (3, 3), (3, 5)})
        self.board.remove_piece_at_square((3, 3))
        self.board.remove_piece_at_square((3, 5))

        # Test black pawn with no pieces in front of it at start
        self.pawn.color = "black"
        self.pawn.position = (1, 0)
        legal_moves = self.pawn.generate_legal_moves(self.board)
        self.assertEqual(legal_moves, {(2, 0), (3, 0)})

        # Test black pawn that moved
        self.pawn.position = (3, 0)
        legal_moves = self.pawn.generate_legal_moves(self.board)
        self.assertEqual(legal_moves, {(4, 0)})

        # Test black pawn with potential capture
        self.pawn.position = (4, 4)
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(5, 5)))
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(5, 3)))
        legal_moves = self.pawn.generate_legal_moves(self.board)
        self.assertEqual(legal_moves, {(5, 4), (5, 5), (5, 3)})
        self.board.remove_piece_at_square((5, 5))
        self.board.remove_piece_at_square((5, 3))
        
    def test_repr(self):
        self.assertEqual(repr(self.pawn), "White Pawn")

class TestRook(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.rook = pieces.Rook("white", (0, 0))
        self.board.place_piece(self.rook)

    def test_init(self):
        self.assertEqual(self.rook.name, "Rook")
        self.assertEqual(self.rook.value, 5)
        self.assertEqual(self.rook.color, "white")
        self.assertEqual(self.rook.position, (0, 0))
        self.assertEqual(self.rook.has_moved, False)

    def test_generate_possible_moves(self):
        # Test rook with no pieces in front of it
        expected_moves = {(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), 
                          (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)}
        self.assertEqual(expected_moves, self.rook.generate_possible_moves(self.board))

        # Test rook with pieces in front of it (both vertically and horizontally)
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(0, 3)))
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(3, 0)))
        expected_moves = {(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), 
                          (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)}
        self.assertEqual(expected_moves, self.rook.generate_possible_moves(self.board))

    def test_generate_legal_moves(self):
        # Test rook with no pieces in front of it
        expected_moves = {(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), 
                          (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)}
        self.assertEqual(expected_moves, self.rook.generate_legal_moves(self.board))

        # Test rook with enemy pieces in front of it (both vertically and horizontally)
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(0, 3)))
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(3, 0)))
        expected_moves = {(0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)}
        self.assertEqual(expected_moves, self.rook.generate_legal_moves(self.board))
        self.board.remove_piece_at_square((0, 3))
        self.board.remove_piece_at_square((3, 0))

        # Test rook with friendly pieces in front of it (both vertically and horizontally)
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(0, 4)))
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(4, 0)))
        expected_moves = {(0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)}
        self.assertEqual(expected_moves, self.rook.generate_legal_moves(self.board))

class TestKnight(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.knight = pieces.Knight("white", (0, 1))
        self.board.place_piece(self.knight)

    def test_generate_possible_moves(self):
        expected_moves = {(2, 0), (2, 2), (1, 3)}
        self.assertEqual(self.knight.generate_possible_moves(self.board), expected_moves)

    def test_generate_legal_moves(self):
        # No other pieces on the board
        expected_moves = {(2, 0), (2, 2), (1, 3)}
        self.assertEqual(self.knight.generate_legal_moves(self.board), expected_moves)

        # Enemy piece where knight can move
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(2, 0)))
        expected_moves = {(2, 2), (1, 3), (2, 0)}
        self.assertEqual(self.knight.generate_legal_moves(self.board), expected_moves)

        # Friendly piece where knight can move
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(2, 2)))
        expected_moves = {(1, 3), (2, 0)}
        self.assertEqual(self.knight.generate_legal_moves(self.board), expected_moves)

    def test_refresh_legal_moves(self):
        expected_moves = {(2, 0), (2, 2), (1, 3)}
        self.knight.refresh_legal_moves(self.board)
        self.assertEqual(self.knight.legal_moves, expected_moves)

class TestBishop(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.bishop = pieces.Bishop("white", (4, 4))
        self.board.place_piece(self.bishop)

    def test_generate_possible_moves(self):
        expected_moves = {(5, 5), (6, 6), (7, 7), (3, 3), (2, 2), (1, 1), (0, 0),
                          (5, 3), (6, 2), (7, 1), (3, 5), (2, 6), (1, 7)}
        self.assertEqual(self.bishop.generate_possible_moves(self.board), expected_moves)

    def test_generate_legal_moves(self):
        # No other pieces on the board
        expected_moves = {(5, 5), (6, 6), (7, 7), (3, 3), (2, 2), (1, 1), (0, 0),
                            (5, 3), (6, 2), (7, 1), (3, 5), (2, 6), (1, 7)}
        self.assertEqual(self.bishop.generate_legal_moves(self.board), expected_moves)

        # Enemy piece where bishop can move
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(5, 5)))
        expected_moves = {(3, 3), (2, 2), (1, 1), (0, 0),
                            (5, 3), (6, 2), (7, 1), (3, 5), (2, 6), (1, 7), (5, 5)}
        self.assertEqual(self.bishop.generate_legal_moves(self.board), expected_moves)

        # Friendly piece where bishop can move
        self.board.place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(3, 3)))
        expected_moves = {(5, 3), (6, 2), (7, 1), (3, 5), (2, 6), (1, 7), (5, 5)}
        self.assertEqual(self.bishop.generate_legal_moves(self.board), expected_moves)

    def test_refresh_legal_moves(self):
        expected_moves = {(5, 5), (6, 6), (7, 7), (3, 3), (2, 2), (1, 1), (0, 0),
                            (5, 3), (6, 2), (7, 1), (3, 5), (2, 6), (1, 7)}
        self.bishop.refresh_legal_moves(self.board)
        self.assertEqual(self.bishop.legal_moves, expected_moves)