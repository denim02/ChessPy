"""
graphics.py
This module contains the ChessUI class, which is a class for creating a
graphical user interface for a chess game. It uses tkinter library to render
a chess board, and displays the pieces on it. The class also handles drag
and drop events for moving pieces on the board.
"""
import pygame
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
        self.render_board()

        # Variables for event handling
        self.dragged_piece_image = None
        self.dragged_piece = None
        self.original_coords = None
        self.offset = None

    def render_board(self):
        """
        Renders the board.
        """
        self.window.fill(DARK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(self.window, LIGHT, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        self.render_pieces()

    def render_pieces(self):
        """
        Renders the pieces on the board.
        """
        for row in range(8):
            for col in range(8):
                self.render_piece((col, row))

    def render_piece(self, position):
        """
        Renders the piece at its coordinates using the pygame library.

        Parameters:
            position (tuple): the position of the piece to be
                rendered in (x, y) format, where x is the row and y is the column.
        """
        piece = self.board.get_piece_at_square(position)
        if piece is not None:
            piece_image = pygame.image.load(f"./game/assets/{piece.color}-{piece.name.lower()}.png").convert_alpha()
            self.window.blit(piece_image, piece.coords)


    def on_drag_start(self, event):
        """
        Handles the start of a drag event on a piece.
        """
        self.dragged_piece_image = event.widget.find_closest(event.x, event.y)[0]
        self.dragged_piece = self.board.get_piece_at_square(
            (int(event.y // SQUARE_SIZE), int(event.x // SQUARE_SIZE))
        )
        self.original_coords = self.canvas.coords(self.dragged_piece_image)
        self.offset = (
            event.x - self.canvas.coords(self.dragged_piece_image)[0],
            event.y - self.canvas.coords(self.dragged_piece_image)[1],
        )

        for row in range(8):
            for col in range(8):
                if (row, col) in self.board.get_piece_at_square(self.dragged_piece.position).legal_moves:
                    x_coord, y_coord = (
                        col * SQUARE_SIZE + SQUARE_SIZE / 2,
                        row * SQUARE_SIZE + SQUARE_SIZE / 2,
                    )
                    circle = self.canvas.create_oval(
                        x_coord - 15,
                        y_coord - 15,
                        x_coord + 15,
                        y_coord + 15,
                        fill="#C0C0C0",
                        outline="gray",
                        width=1,
                        tags="highlight",
                    )
                    self.canvas.tag_raise(circle)
        self.canvas.tag_raise(self.dragged_piece_image)

    def on_drag_motion(self, event):
        """
        Handles the motion of a drag event on a piece."""
        self.canvas.move(
            self.dragged_piece_image,
            event.x - self.canvas.coords(self.dragged_piece_image)[0] - self.offset[0],
            event.y - self.canvas.coords(self.dragged_piece_image)[1] - self.offset[1],
        )

    def on_drag_release(self, event):
        """
        Handles the release of a drag event on a piece."""
        x_coord, y_coord = (
            round(self.canvas.coords(self.dragged_piece_image)[0] / SQUARE_SIZE)
            * SQUARE_SIZE,
            round(self.canvas.coords(self.dragged_piece_image)[1] / SQUARE_SIZE)
            * SQUARE_SIZE,
        )
        new_position = (y_coord // SQUARE_SIZE, x_coord // SQUARE_SIZE)
        try:
            self.game.make_move(self.dragged_piece.position, new_position)
            self.canvas.coords(self.dragged_piece_image, x_coord, y_coord)
        except ValueError as error:
            self.canvas.coords(self.dragged_piece_image, self.original_coords)
            print(f"Move error: {error}")
        self.render_board()