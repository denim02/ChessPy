"""This module contains unit tests for the pieces module in chess_game/pieces.py."""
from chess_game import pieces, board, constants
import unittest


class TestPiece(unittest.TestCase):
    def setUp(self):
        self.piece = pieces.Pawn(color="black", position=(0, 0))
        self.board = board.Board()
        self.board._place_piece(self.piece)

    def test_init(self):
        self.assertEqual(self.piece.name, "Pawn")
        self.assertEqual(self.piece.value, 1)
        self.assertEqual(self.piece.color, "black")
        self.assertEqual(self.piece.position, (0, 0))
        self.assertIsNone(self.piece.image)
        self.assertEqual(self.piece.coords, (0, 0))
        self.assertEqual(self.piece.legal_moves, ((1, 0), (2, 0)))

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
        self.piece._Piece__refresh_coords()
        self.assertEqual(
            self.piece.coords, (2 * constants.SQUARE_SIZE, 4 * constants.SQUARE_SIZE)
        )

    def test_legal_moves(self):
        self.assertEqual(self.piece.legal_moves, ((1, 0), (2, 0)))
        self.piece.position = (7, 7)
        self.piece.refresh_legal_moves(self.board)
        self.assertEqual(self.piece.legal_moves, ())

    def test__generate_possible_moves(self):
        self.assertEqual(self.piece.legal_moves, ((1, 0), (2, 0)))
        self.piece.position = (7, 7)
        self.piece.refresh_legal_moves(self.board)
        self.assertEqual(self.piece.legal_moves, ())

    def test_refresh_legal_moves(self):
        self.assertEqual(self.piece.legal_moves, ((1, 0), (2, 0)))
        self.piece.position = (6, 5)
        self.piece.refresh_legal_moves(self.board)
        self.assertEqual(self.piece.legal_moves, ((7, 5),))

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
        piece = pieces.Pawn(color="white", position=(0, 0))
        self.assertEqual(piece.to_algebraic_notation(), "P")

        # Test knights
        piece = pieces.Knight(color="white", position=(0, 0))
        self.assertEqual(piece.to_algebraic_notation(), "N")

    def test_repr(self):
        self.assertEqual(repr(self.piece), "Black Pawn")

    def test_eq(self):
        piece1 = pieces.Pawn(color="black", position=(0, 0))
        piece2 = pieces.Pawn(color="black", position=(0, 0))
        piece3 = pieces.Pawn(color="white", position=(0, 0))
        piece4 = pieces.Pawn(color="black", position=(1, 0))
        piece5 = pieces.Queen(color="black", position=(0, 0))
        not_piece = 2

        self.assertNotEqual(piece1, not_piece)
        self.assertEqual(piece1, piece2)
        self.assertNotEqual(piece1, piece3)
        self.assertNotEqual(piece1, piece4)
        self.assertNotEqual(piece1, piece5)


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

    def test_generate_possible_moves_white(self):
        # Test white pawn with no pieces in front of it at start
        possible_moves = self.pawn._generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(5, 0), (4, 0)})

        # Test white pawn that moved
        self.board.move_piece_to_square(self.pawn, (3, 0))
        possible_moves = self.pawn._generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(2, 0)})

        # Test white pawn with potential capture
        self.board.move_piece_to_square(self.pawn, (4, 4))
        self.board._place_piece(pieces.Pawn(color="black", position=(3, 3)))
        self.board._place_piece(pieces.Pawn(color="black", position=(3, 5)))
        possible_moves = self.pawn._generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(3, 4), (3, 3), (3, 5)})
        self.board._remove_piece_at_square((3, 3))
        self.board._remove_piece_at_square((3, 5))

        # Test white pawn with piece in front of it
        self.board._place_piece(pieces.Pawn(color="black", position=(3, 4)))
        possible_moves = self.pawn._generate_possible_moves(self.board)
        self.assertEqual(possible_moves, set())

        # Test white pawn with en passant
        self.board._remove_piece_at_square((3, 4))
        self.board._remove_piece_at_square((4, 4))
        self.pawn = pieces.Pawn(color="white", position=(3, 4))
        self.pawn.has_moved = True
        self.board._place_piece(self.pawn)
        self.board._place_piece(pieces.Pawn(color="black", position=(1, 3)))
        self.board.move_piece_to_square(self.board.get_piece_at_square((1, 3)), (3, 3))
        possible_moves = self.pawn._generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(2, 4), (2, 3)})

    def test_generate_possible_moves_black(self):
        self.board._remove_piece_at_square((6, 0))
        self.pawn = pieces.Pawn(color="black", position=(1, 0))
        self.board._place_piece(self.pawn)

        # Test black pawn with no pieces in front of it at start
        possible_moves = self.pawn._generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(2, 0), (3, 0)})

        # Test black pawn that moved
        self.board.move_piece_to_square(self.pawn, (3, 0))
        possible_moves = self.pawn._generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(4, 0)})

        # Test black pawn with potential capture
        self.board.move_piece_to_square(self.pawn, (4, 4))
        self.board._place_piece(pieces.Pawn(color="white", position=(5, 3)))
        self.board._place_piece(pieces.Pawn(color="white", position=(5, 5)))
        possible_moves = self.pawn._generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(5, 4), (5, 5), (5, 3)})
        self.board._remove_piece_at_square((5, 5))
        self.board._remove_piece_at_square((5, 3))

        # Test black pawn with piece in front of it
        self.board._place_piece(pieces.Pawn(color="white", position=(5, 4)))
        possible_moves = self.pawn._generate_possible_moves(self.board)
        self.assertEqual(possible_moves, set())

        # Test black pawn with en passant
        self.board._remove_piece_at_square((5, 4))
        self.board._remove_piece_at_square((4, 4))
        self.board._place_piece(pieces.Pawn(color="white", position=(6, 3)))
        self.pawn = pieces.Pawn(color="black", position=(4, 4))
        self.pawn.has_moved = True
        self.board._place_piece(self.pawn)
        self.board.move_piece_to_square(self.board.get_piece_at_square((6, 3)), (4, 3))
        possible_moves = self.pawn._generate_possible_moves(self.board)
        self.assertEqual(possible_moves, {(5, 3), (5, 4)})

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
        expected_moves = {
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 6),
            (0, 7),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
        }
        self.assertEqual(expected_moves, self.rook._generate_possible_moves(self.board))

        # Test rook with pieces in front of it (both vertically and
        # horizontally)
        self.board._place_piece(pieces.Pawn(color="black", position=(0, 3)))
        self.board._place_piece(pieces.Pawn(color="black", position=(3, 0)))
        expected_moves = {
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 6),
            (0, 7),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
        }
        self.assertEqual(expected_moves, self.rook._generate_possible_moves(self.board))


class TestKnight(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.knight = pieces.Knight("white", (0, 1))
        self.board._place_piece(self.knight)

    def test_generate_possible_moves(self):
        expected_moves = {(2, 0), (2, 2), (1, 3)}
        self.assertEqual(
            self.knight._generate_possible_moves(self.board), expected_moves
        )


class TestBishop(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.bishop = pieces.Bishop("white", (4, 4))
        self.board._place_piece(self.bishop)

    def test_generate_possible_moves(self):
        expected_moves = {
            (5, 5),
            (6, 6),
            (7, 7),
            (3, 3),
            (2, 2),
            (1, 1),
            (0, 0),
            (5, 3),
            (6, 2),
            (7, 1),
            (3, 5),
            (2, 6),
            (1, 7),
        }
        self.assertEqual(
            self.bishop._generate_possible_moves(self.board), expected_moves
        )


class TestQueen(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.queen = pieces.Queen("white", (4, 4))
        self.board._place_piece(self.queen)

    def test_generate_possible_moves(self):
        expected_moves = {
            (5, 5),
            (6, 6),
            (7, 7),
            (3, 3),
            (2, 2),
            (1, 1),
            (0, 0),
            (5, 3),
            (6, 2),
            (7, 1),
            (3, 5),
            (2, 6),
            (1, 7),
            (5, 4),
            (6, 4),
            (7, 4),
            (4, 5),
            (4, 6),
            (4, 7),
            (3, 4),
            (2, 4),
            (1, 4),
            (0, 4),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
        }
        self.assertEqual(
            self.queen._generate_possible_moves(self.board), expected_moves
        )


class TestKing(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()
        self.king = pieces.King("white", (4, 4))
        self.board._place_piece(self.king)

    def test_generate_possible_moves(self):
        # No other pieces on the board
        expected_moves = {
            (5, 5),
            (5, 4),
            (5, 3),
            (4, 5),
            (4, 3),
            (3, 5),
            (3, 4),
            (3, 3),
        }
        self.assertEqual(self.king._generate_possible_moves(self.board), expected_moves)

        # Castleing, queen and king side
        self.board._remove_piece_at_square((4, 4))
        self.king = pieces.King("white", (7, 4))
        self.board._place_piece(self.king)

        self.board._place_piece(pieces.Rook(color="white", position=(7, 7)))

        self.board._place_piece(pieces.Rook("white", (7, 0)))
        expected_moves = {(6, 4), (6, 3), (6, 5), (7, 5), (7, 3), (7, 6), (7, 2)}
        self.assertEqual(self.king._generate_possible_moves(self.board), expected_moves)

        # Castleing, queen and king side, but rook has moved
        self.board.get_piece_at_square((7, 7)).has_moved = True
        expected_moves = {(6, 4), (6, 3), (6, 5), (7, 5), (7, 3), (7, 2)}
        self.assertEqual(self.king._generate_possible_moves(self.board), expected_moves)

        # Castleing, queen and king side, but king has moved
        self.board.get_piece_at_square((7, 7)).has_moved = False
        self.king.has_moved = True
        expected_moves = {(6, 4), (6, 3), (6, 5), (7, 5), (7, 3)}
        self.assertEqual(self.king._generate_possible_moves(self.board), expected_moves)

        # Castleing, queen and king side, but king is in check
        self.board._place_piece(pieces.Rook(color="black", position=(6, 4)))
        self.king.has_moved = False
        expected_moves = {(6, 3), (6, 5), (7, 5), (7, 3), (6, 4)}
        self.assertEqual(self.king._generate_possible_moves(self.board), expected_moves)
        self.board._remove_piece_at_square((6, 4))

        # Castleing, but path is blocked by friendly piece king side
        self.board._place_piece(pieces.Pawn(color="white", position=(7, 6)))
        expected_moves = {(6, 3), (6, 4), (6, 5), (7, 3), (7, 2), (7, 5)}
        self.assertEqual(self.king._generate_possible_moves(self.board), expected_moves)
        self.board._remove_piece_at_square((7, 6))

        # Castleing, but path is under attack by distant enemy piece (enemy
        # queen)
        self.board._remove_piece_at_square((5, 5))
        self.board._place_piece(pieces.Queen(color="black", position=(5, 5)))
        expected_moves = {(6, 4), (6, 3), (6, 5), (7, 5), (7, 3)}
        self.assertEqual(self.king._generate_possible_moves(self.board), expected_moves)


if __name__ == "__main__":
    unittest.main()
