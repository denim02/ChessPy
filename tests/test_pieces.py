import unittest
from chess_game import pieces, board, chess_logic, constants

class TestPiece(unittest.TestCase):
    def setUp(self):
        self.piece = pieces.Piece(name="Test Piece", value=10, color="black", position=(0, 0))
        self.board = board.Board()
        self.board._place_piece(self.piece)

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

        # Test pawns
        pawn_piece = pieces.Piece.from_algebraic_notation("P", position)
        self.assertIsInstance(pawn_piece, pieces.Pawn)
        self.assertEqual(pawn_piece.name, "Pawn")
        self.assertEqual(pawn_piece.value, 1)
        self.assertEqual(pawn_piece.color, "white")
        self.assertEqual(pawn_piece.position, position)

        # Test rooks
        rook_piece = pieces.Piece.from_algebraic_notation("r", position)
        self.assertIsInstance(rook_piece, pieces.Rook)
        self.assertEqual(rook_piece.color, "black")

        # Test knights
        knight_piece = pieces.Piece.from_algebraic_notation("N", position)
        self.assertIsInstance(knight_piece, pieces.Knight)

        # Test bishops
        bishop_piece = pieces.Piece.from_algebraic_notation("B", position)
        self.assertIsInstance(bishop_piece, pieces.Bishop)

        # Test queens
        queen_piece = pieces.Piece.from_algebraic_notation("Q", position)
        self.assertIsInstance(queen_piece, pieces.Queen)

        # Test kings
        king_piece = pieces.Piece.from_algebraic_notation("K", position)
        self.assertIsInstance(king_piece, pieces.King)
        
        with self.assertRaises(ValueError):
            pieces.Piece.from_algebraic_notation("X", position)

    def test_to_algebraic_notation(self):
        piece = pieces.Piece(name="Pawn", value=1, color="white", position=(0, 0))
        self.assertEqual(piece.to_algebraic_notation(), "P")

        # Test knights
        piece = pieces.Knight(color="white", position=(0, 0))
        self.assertEqual(piece.to_algebraic_notation(), "N")

    def test_repr(self):
        self.assertEqual(repr(self.piece), "Black Test Piece")

class TestPawn(unittest.TestCase):
    def setUp(self):
        self.pawn = pieces.Pawn(color="white", position=(6, 0))
        self.board = board.Board()
        self.board._place_piece(self.pawn)

    def test_init(self):
        self.assertEqual(self.pawn.name, "Pawn")
        self.assertEqual(self.pawn.value, 1)
        self.assertEqual(self.pawn.color, "white")
        self.assertEqual(self.pawn.position, (6, 0))
        self.assertIsNone(self.pawn.image)
        self.assertEqual(self.pawn.coords, (0, 6 * constants.SQUARE_SIZE))

    def test_generate_possible_moves(self):
        # Test white pawn with no pieces in front of it at start
        possible_moves = self.pawn.generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(5, 0), (4, 0)})

        # Test white pawn that moved
        self.board.move_piece_to_square(self.pawn, (3, 0))
        possible_moves = self.pawn.generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(2, 0)})

        # Test white pawn with potential capture
        self.board.move_piece_to_square(self.pawn, (4, 4))
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(3, 3)))
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(3, 5)))
        possible_moves = self.pawn.generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(3, 4), (3, 3), (3, 5)})
        self.board._remove_piece_at_square((3, 3))
        self.board._remove_piece_at_square((3, 5))

        # Test white pawn with piece in front of it
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(3, 4)))
        possible_moves = self.pawn.generate_possible_moves(self.board)
        self.assertEqual(possible_moves, set())

        # Test black pawn with no pieces in front of it at start
        self.board._remove_piece_at_square((3, 4))
        self.board._remove_piece_at_square((4, 4))
        self.pawn = pieces.Pawn(color="black", position=(1, 0))
        self.board._place_piece(self.pawn)
        possible_moves = self.pawn.generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(2, 0), (3, 0)})

        # Test black pawn that moved
        self.board.move_piece_to_square(self.pawn, (3, 0))
        possible_moves = self.pawn.generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(4, 0)})
        
        # Test black pawn with potential capture
        self.board.move_piece_to_square(self.pawn, (4, 4))
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(5, 5)))
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(5, 3)))
        possible_moves = self.pawn.generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(5, 4), (5, 5), (5, 3)})
        self.board._remove_piece_at_square((5, 5))
        self.board._remove_piece_at_square((5, 3))

        # Test black pawn with piece in front of it
        self.board.move_piece_to_square(self.pawn, (4, 4))
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(5, 4)))
        possible_moves = self.pawn.generate_possible_moves(self.board)
        self.assertEqual(possible_moves, set())
        
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
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(3, 3)))
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(3, 5)))
        legal_moves = self.pawn.generate_legal_moves(self.board)
        self.assertEqual(legal_moves, {(3, 4), (3, 3), (3, 5)})
        self.board._remove_piece_at_square((3, 3))
        self.board._remove_piece_at_square((3, 5))

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
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(5, 5)))
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(5, 3)))
        legal_moves = self.pawn.generate_legal_moves(self.board)
        self.assertEqual(legal_moves, {(5, 4), (5, 5), (5, 3)})
        self.board._remove_piece_at_square((5, 5))
        self.board._remove_piece_at_square((5, 3))
        
    def test_repr(self):
        self.assertEqual(repr(self.pawn), "White Pawn")

class TestRook(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.rook = pieces.Rook("white", (0, 0))
        self.board._place_piece(self.rook)

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
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(0, 3)))
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(3, 0)))
        expected_moves = {(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), 
                          (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)}
        self.assertEqual(expected_moves, self.rook.generate_possible_moves(self.board))

    def test_generate_legal_moves(self):
        # Test rook with no pieces in front of it
        expected_moves = {(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), 
                          (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)}
        self.assertEqual(expected_moves, self.rook.generate_legal_moves(self.board))

        # Test rook with enemy pieces in front of it (both vertically and horizontally)
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(0, 3)))
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(3, 0)))
        expected_moves = {(0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)}
        self.assertEqual(expected_moves, self.rook.generate_legal_moves(self.board))
        self.board._remove_piece_at_square((0, 3))
        self.board._remove_piece_at_square((3, 0))

        # Test rook with friendly pieces in front of it (both vertically and horizontally)
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(0, 4)))
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(4, 0)))
        expected_moves = {(0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)}
        self.assertEqual(expected_moves, self.rook.generate_legal_moves(self.board))

class TestKnight(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.knight = pieces.Knight("white", (0, 1))
        self.board._place_piece(self.knight)

    def test_generate_possible_moves(self):
        expected_moves = {(2, 0), (2, 2), (1, 3)}
        self.assertEqual(self.knight.generate_possible_moves(self.board), expected_moves)

    def test_generate_legal_moves(self):
        # No other pieces on the board
        expected_moves = {(2, 0), (2, 2), (1, 3)}
        self.assertEqual(self.knight.generate_legal_moves(self.board), expected_moves)

        # Enemy piece where knight can move
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(2, 0)))
        expected_moves = {(2, 2), (1, 3), (2, 0)}
        self.assertEqual(self.knight.generate_legal_moves(self.board), expected_moves)

        # Friendly piece where knight can move
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(2, 2)))
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
        self.board._place_piece(self.bishop)

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
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(5, 5)))
        expected_moves = {(3, 3), (2, 2), (1, 1), (0, 0),
                            (5, 3), (6, 2), (7, 1), (3, 5), (2, 6), (1, 7), (5, 5)}
        self.assertEqual(self.bishop.generate_legal_moves(self.board), expected_moves)

        # Friendly piece where bishop can move
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(3, 3)))
        expected_moves = {(5, 3), (6, 2), (7, 1), (3, 5), (2, 6), (1, 7), (5, 5)}
        self.assertEqual(self.bishop.generate_legal_moves(self.board), expected_moves)

    def test_refresh_legal_moves(self):
        expected_moves = {(5, 5), (6, 6), (7, 7), (3, 3), (2, 2), (1, 1), (0, 0),
                            (5, 3), (6, 2), (7, 1), (3, 5), (2, 6), (1, 7)}
        self.bishop.refresh_legal_moves(self.board)
        self.assertEqual(self.bishop.legal_moves, expected_moves)

class TestQueen(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.queen = pieces.Queen("white", (4, 4))
        self.board._place_piece(self.queen)

    def test_generate_possible_moves(self):
        expected_moves = {(5, 5), (6, 6), (7, 7), (3, 3), (2, 2), (1, 1), (0, 0),
                          (5, 3), (6, 2), (7, 1), (3, 5), (2, 6), (1, 7),
                          (5, 4), (6, 4), (7, 4), (4, 5), (4, 6), (4, 7), (3, 4), (2, 4), (1, 4), (0, 4),
                          (4, 0), (4, 1), (4, 2), (4, 3)}
        self.assertEqual(self.queen.generate_possible_moves(self.board), expected_moves)

    def test_generate_legal_moves(self):
        # No other pieces on the board
        expected_moves = {(5, 5), (6, 6), (7, 7), (3, 3), (2, 2), (1, 1), (0, 0),
                          (5, 3), (6, 2), (7, 1), (3, 5), (2, 6), (1, 7),
                          (5, 4), (6, 4), (7, 4), (4, 5), (4, 6), (4, 7), (3, 4), (2, 4), (1, 4), (0, 4),
                          (4, 0), (4, 1), (4, 2), (4, 3)}
        self.assertEqual(self.queen.generate_legal_moves(self.board), expected_moves)

        # Enemy piece where queen can move
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(5, 5)))
        expected_moves = {(3, 3), (2, 2), (1, 1), (0, 0),
                          (5, 3), (6, 2), (7, 1), (3, 5), (2, 6), (1, 7),
                          (5, 4), (6, 4), (7, 4), (4, 5), (4, 6), (4, 7), (3, 4), (2, 4), (1, 4), (0, 4), (5, 5),
                          (4, 0), (4, 1), (4, 2), (4, 3)}
        self.assertEqual(self.queen.generate_legal_moves(self.board), expected_moves)

        # Friendly piece where queen can move
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(3, 3)))
        expected_moves = {(5, 3), (6, 2), (7, 1), (3, 5), (2, 6), (1, 7),
                            (5, 4), (6, 4), (7, 4), (4, 5), (4, 6), (4, 7), (3, 4), (2, 4), (1, 4), (0, 4), (5, 5),
                            (4, 0), (4, 1), (4, 2), (4, 3)}
        self.assertEqual(self.queen.generate_legal_moves(self.board), expected_moves)

    def test_refresh_legal_moves(self):
        expected_moves = {(5, 5), (6, 6), (7, 7), (3, 3), (2, 2), (1, 1), (0, 0),
                          (5, 3), (6, 2), (7, 1), (3, 5), (2, 6), (1, 7),
                          (5, 4), (6, 4), (7, 4), (4, 5), (4, 6), (4, 7), (3, 4), (2, 4), (1, 4), (0, 4),
                          (4, 0), (4, 1), (4, 2), (4, 3)}
        self.queen.refresh_legal_moves(self.board)
        self.assertEqual(self.queen.legal_moves, expected_moves)

class TestKing(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.king = pieces.King("white", (4, 4))
        self.board._place_piece(self.king)

    def test_generate_possible_moves(self):
        expected_moves = {(5, 5), (5, 4), (5, 3), (4, 5), (4, 3), (3, 5), (3, 4), (3, 3)}
        self.assertEqual(self.king.generate_possible_moves(self.board), expected_moves)

    def test_generate_legal_moves(self):
        # No other pieces on the board
        expected_moves = {(5, 5), (5, 4), (5, 3), (4, 5), (4, 3), (3, 5), (3, 4), (3, 3)}
        self.assertEqual(self.king.generate_legal_moves(self.board), expected_moves)

        # Enemy piece where king can move
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="black", position=(5, 5)))
        expected_moves = {(5, 4), (5, 3), (4, 5), (4, 3), (3, 5), (3, 4), (3, 3), (5, 5)}
        self.assertEqual(self.king.generate_legal_moves(self.board), expected_moves)

        # Friendly piece where king can move
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(3, 3)))
        expected_moves = {(5, 4), (5, 3), (4, 5), (4, 3), (3, 5), (3, 4), (5, 5)}
        self.assertEqual(self.king.generate_legal_moves(self.board), expected_moves)

        # Check if king can move to a square that would put him in check (enemy rook)
        self.board._place_piece(pieces.Rook("black", (4, 7)))
        expected_moves = {(5, 4), (5, 3), (4, 5), (4, 3), (3, 5), (3, 4), (5, 5)}
        self.assertEqual(self.king.generate_legal_moves(self.board), expected_moves)
        self.board._remove_piece_at_square((4, 7))

        # Castleing, queen and king side
        self.board._remove_piece_at_square((4, 4))
        self.king = pieces.King("white", (7, 4))
        self.board._place_piece(self.king)

        self.board._place_piece(pieces.Rook("white", (7, 7)))
        self.board._place_piece(pieces.Rook("white", (7, 0)))
        expected_moves = {(6, 4), (6, 3), (6, 5), (7, 5), (7, 3), (7, 6), (7, 2)}
        self.assertEqual(self.king.generate_legal_moves(self.board), expected_moves)

        # Castleing, queen and king side, but rook has moved
        self.board.get_piece_at_square((7, 7)).has_moved = True
        expected_moves = {(6, 4), (6, 3), (6, 5), (7, 5), (7, 3), (7, 2)}
        self.assertEqual(self.king.generate_legal_moves(self.board), expected_moves)

        # Castleing, queen and king side, but king has moved
        self.board.get_piece_at_square((7, 7)).has_moved = False
        self.king.has_moved = True
        expected_moves = {(6, 4), (6, 3), (6, 5), (7, 5), (7, 3)}
        self.assertEqual(self.king.generate_legal_moves(self.board), expected_moves)

        # Castleing, queen and king side, but king is in check
        self.board._place_piece(pieces.Rook("black", (6, 4)))
        self.king.has_moved = False
        expected_moves = {(6, 3), (6, 5), (7, 5), (7, 3), (6, 4)}
        self.assertEqual(self.king.generate_legal_moves(self.board), expected_moves)
        self.board._remove_piece_at_square((6, 4))

        # Castleing, but path is blocked by friendly piece king side
        self.board._place_piece(pieces.Piece(name="Test Piece", value=10, color="white", position=(7, 6)))
        expected_moves = {(6, 3), (6, 4), (6, 5), (7, 3), (7, 2), (7, 5)}
        self.assertEqual(self.king.generate_legal_moves(self.board), expected_moves)
        self.board._remove_piece_at_square((7, 6))
        
        # Castleing, but path is under attack by distant enemy piece (enemy queen)
        self.board._remove_piece_at_square((5, 5))
        self.board._place_piece(pieces.Queen("black", (5, 5)))
        expected_moves = {(6, 4), (6, 3), (6, 5), (7, 5), (7, 3)}
        self.assertEqual(self.king.generate_legal_moves(self.board), expected_moves)

    def test_refresh_legal_moves(self):
        expected_moves = {(5, 5), (5, 4), (5, 3), (4, 5), (4, 3), (3, 5), (3, 4), (3, 3)}
        self.king.refresh_legal_moves(self.board)
        self.assertEqual(self.king.legal_moves, expected_moves)

if __name__ == '__main__':
    unittest.main()