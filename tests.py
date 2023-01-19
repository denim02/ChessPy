import unittest
import pieces

class Test(unittest.TestCase):
    def test(self):
        self.assertEqual(1, 1)

class TestPieces(unittest.TestCase):
    def test_piece_attributes(self):
        piece = pieces.Pawn("white", (0, 0))
        self.assertEqual(piece.name, "Pawn")
        self.assertEqual(piece.value, 1)
        self.assertEqual(piece.color, "white")
        self.assertEqual(piece.position, (0, 0))
        self.assertEqual(piece.legal_moves, set())
