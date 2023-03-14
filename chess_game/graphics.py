"""
graphics.py
This module contains the ChessUI class, which is a class for creating a
graphical user interface for a chess game. It uses tkinter library to render
a chess board, and displays the pieces on it. The class also handles drag
and drop events for moving pieces on the board.
"""
import pygame
from pygame import gfxdraw
from chess_game.constants import *

class ChessUI:
    """
    ChessUI:
    This is a class for creating a graphical user interface for a chess game.
    It is initialized with a game object, and it creates a tkinter window that
    renders the chess board, and displays the pieces on it. The class also handles
    drag and drop events for moving pieces on the board.
    """

    def __init__(self, game):
        """
        Initializes the board and the game.

        Parameters:
            game (ChessGame): the game to be played.
        """
        self.game = game
        self.board = game.board
        self.window = pygame.display.set_mode((720, 720))
        pygame.display.set_caption("Chess Game")

        # Convert and store the images of the pieces
        for piece in self.board.piece_list:
            piece.image = pygame.image.load(f"./game/assets/{piece.color}-{piece.name.lower()}.png").convert_alpha()

        # Variables for event handling
        self.dragged_piece = None
        self.is_dragging = False
        self.original_coords = None
        self.offset = None

        self.render_board()

    def render_board(self):
        """
        Renders the board.
        """
        self.window.fill(DARK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(self.window, LIGHT, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        self.render_pieces()
        if self.dragged_piece:
            self.render_moves()
            self.render_piece(self.dragged_piece)
        

    def render_pieces(self):
        """
        Renders the pieces on the board.
        """
        for piece in self.board.piece_list:
                if piece != self.dragged_piece:
                    self.render_piece(piece)

    def render_piece(self, piece):
        """
        Renders the piece at its coordinates using the pygame library.

        Parameters:
            position (tuple): the position of the piece to be
                rendered in (x, y) format, where x is the row and y is the column.
        """
        if piece is not None:
            self.window.blit(piece.image, piece.coords)

    def render_moves(self):
        """
        Renders circles on the given squares.

        Parameters:
            circle_squares (list): a list of squares where circles are to be rendered.
        """
        if self.dragged_piece.color == self.game.turn:
            for circle_square in self.dragged_piece.legal_moves:
                self.draw_circle(self.window, (180, 180, 180), (
                    circle_square[1] * SQUARE_SIZE + SQUARE_SIZE // 2, 
                    circle_square[0] * SQUARE_SIZE + SQUARE_SIZE // 2
                    ), 15)

    @staticmethod
    def get_square_at_coords(coords):
        """
        Returns the position of a square at the given coordinates.

        Parameters:
            coords (tuple): the coordinates of the square in (x, y) format,
                where x is the row and y is the column.
        """
        return (coords[1] // SQUARE_SIZE, coords[0] // SQUARE_SIZE)
    
    @staticmethod
    def get_coords_of_square(position):
        """
        Returns the coordinates of the given square.

        Parameters:
            position (tuple): the position of the square in (x, y) format,
                where x is the row and y is the column.
        """
        return (position[1] * SQUARE_SIZE, position[0] * SQUARE_SIZE)

    @staticmethod
    def draw_circle(surface, color, coords, radius):
        gfxdraw.aacircle(surface, coords[0], coords[1], radius, color)
        gfxdraw.filled_circle(surface, coords[0], coords[1], radius, color)