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
    piece_images = {}

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

        # Load piece images
        self.initialize_images()

        for piece in self.board.piece_list:
            piece.image = self.piece_images[f"{piece.color}-{piece.name.lower()}"]

        # Variables for event handling
        self.dragged_piece = None
        self.is_dragging = False
        self.original_coords = None
        self.offset = None

        # Variables for promotion box
        self.promotion_box = None

        self.render_all()

    def render_all(self):
        """
        Renders the board and the pieces on it.
        """
        self.render_board()
        self.render_pieces()

        if self.dragged_piece:
            self.render_moves()
            self.render_piece(self.dragged_piece)

    def render_board(self):
        """
        Renders the board.
        """
        self.window.fill(DARK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(
                    self.window,
                    LIGHT,
                    (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                )

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
            if not piece.image:
                piece.image = self.piece_images[f"{piece.color}-{piece.name.lower()}"]
            self.window.blit(piece.image, piece.coords)

    def render_moves(self):
        """
        Renders circles on the given squares.

        Parameters:
            circle_squares (list): a list of squares where circles are to be rendered.
        """
        if self.dragged_piece.color == self.game.turn:
            for circle_square in self.dragged_piece.legal_moves:
                self.draw_circle(
                    self.window,
                    (180, 180, 180),
                    (
                        circle_square[1] * SQUARE_SIZE + SQUARE_SIZE // 2,
                        circle_square[0] * SQUARE_SIZE + SQUARE_SIZE // 2,
                    ),
                    15,
                )

    @classmethod
    def initialize_images(cls):
        """
        Initializes the images of the pieces.
        """
        cls.piece_images = {
            "white-pawn": pygame.image.load("./game/assets/white-pawn.png").convert_alpha(),
            "white-rook": pygame.image.load("./game/assets/white-rook.png").convert_alpha(),
            "white-knight": pygame.image.load("./game/assets/white-knight.png").convert_alpha(),
            "white-bishop": pygame.image.load("./game/assets/white-bishop.png").convert_alpha(),
            "white-queen": pygame.image.load("./game/assets/white-queen.png").convert_alpha(),
            "white-king": pygame.image.load("./game/assets/white-king.png").convert_alpha(),
            "black-pawn": pygame.image.load("./game/assets/black-pawn.png").convert_alpha(),
            "black-rook": pygame.image.load("./game/assets/black-rook.png").convert_alpha(),
            "black-knight": pygame.image.load("./game/assets/black-knight.png").convert_alpha(),
            "black-bishop": pygame.image.load("./game/assets/black-bishop.png").convert_alpha(),
            "black-queen": pygame.image.load("./game/assets/black-queen.png").convert_alpha(),
            "black-king": pygame.image.load("./game/assets/black-king.png").convert_alpha(),
        }

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

class Button:
    def __init__(self, x, y, image, scale, return_value, window):
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.return_value = return_value
        self.window = window
        self.is_clicked = False

    def draw(self):
        # draw button
        self.window.blit(self.image, self.rect.topleft)

    def check_click(self, event):
        # check if button is clicked
        if self.rect.collidepoint(event.pos):
            self.is_clicked = True

class PromotionBox:
    def __init__(self, window, piece_color):
        # Define width and height of popup window
        self.width = 300
        self.height = 500
        self.window = window
        self.x = (self.window.get_width() - self.width) // 2
        self.y = (self.window.get_height() - self.height) // 2

        # Create a surface for the popup box
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0, 0, 0))
        self.surface.set_alpha(128)

        # Add text
        font = pygame.font.SysFont("arial", 40)
        self.text = font.render("Promote to:", True, (255, 255, 255))

        # Create buttons
        self.buttons = []
        button_x = self.x + (self.width - SQUARE_SIZE) // 2
        self.buttons.append(Button(button_x, 200, f"./game/assets/{piece_color}-queen.png", 1, "Queen", self.window))
        self.buttons.append(Button(button_x, 300, f"./game/assets/{piece_color}-rook.png", 1, "Rook", self.window))
        self.buttons.append(Button(button_x, 400, f"./game/assets/{piece_color}-bishop.png", 1, "Bishop", self.window))
        self.buttons.append(Button(button_x, 500, f"./game/assets/{piece_color}-knight.png", 1, "Knight", self.window))

        # Define final choice
        self.final_choice = None
        self.show()

    def show(self):
        # Show popup window
        self.window.blit(self.surface, (self.x, self.y))
        self.draw()
        self.window.blit(self.text, (self.x + (self.width - self.text.get_width()) // 2, 140))
        self.get_promotion_choice()

    def draw(self):
        # Draw 
        for button in self.buttons:
            button.draw()

    def get_promotion_choice(self):
        # Block the game until a choice is made
        while self.final_choice is None:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        button.check_click(event)
                        if button.is_clicked:
                            self.final_choice = button.return_value
                            button.is_clicked = False

            pygame.display.update()
