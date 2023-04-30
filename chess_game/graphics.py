"""The graphics module contains the ChessUI class, which is used to
create the graphical user interface for the chess game and the Button and
PromotionBox classes which are used for the pop-up box displayed when a pawn
reaches the end of the board."""
import pygame
from sys import exit
from pygame import gfxdraw
from chess_game import constants
from typing import TYPE_CHECKING, Optional

# USED FOR TYPE HINTING ONLY
if TYPE_CHECKING:
    from chess_game.board import Board
    from chess_game.pieces import Piece


class ChessUI:
    """Class used to create the graphical user interface for the chess game."""

    piece_images = {}

    def __init__(self, board: "Board") -> None:
        self.board = board
        self.window = pygame.display.set_mode(
            (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
        )
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

    def render_all(self) -> None:
        """Renders the board, pieces and possible moves (if there is a piece that the user
        is currently dragging)."""
        self.render_board()
        self.render_pieces()

        if self.dragged_piece:
            self.render_moves()
            self.render_piece(self.dragged_piece)

    def render_board(self) -> None:
        """Renders the board and its squares using the pygame library."""
        self.window.fill(constants.DARK)
        for row in range(constants.ROWS):
            for col in range(row % 2, constants.COLS, 2):
                pygame.draw.rect(
                    self.window,
                    constants.LIGHT,
                    (
                        row * constants.SQUARE_SIZE,
                        col * constants.SQUARE_SIZE,
                        constants.SQUARE_SIZE,
                        constants.SQUARE_SIZE,
                    ),
                )

    def render_pieces(self) -> None:
        """Renders all the pieces on the board using the pygame library."""
        for piece in self.board.piece_list:
            if piece != self.dragged_piece:
                self.render_piece(piece)

    def render_piece(self, piece: "Piece") -> None:
        """Renders a chess piece using the pygame library.

        Parameters
        ----------
        piece : Piece
            Piece to be rendered.
        """
        if piece is not None:
            if not piece.image:
                piece.image = self.piece_images[f"{piece.color}-{piece.name.lower()}"]
            self.window.blit(piece.image, piece.coords)

    def render_moves(self) -> None:
        """Renders circles on the squares that represent the legal positions for
        whichever piece the user is currently dragging."""
        for circle_square in self.dragged_piece.legal_moves:
            self.draw_circle(
                self.window,
                (180, 180, 180),
                (
                    circle_square[1] * constants.SQUARE_SIZE
                    + constants.SQUARE_SIZE // 2,
                    circle_square[0] * constants.SQUARE_SIZE
                    + constants.SQUARE_SIZE // 2,
                ),
                15,
            )

    def render_gameover(self, status: str, winner: Optional[str] = None) -> None:
        """Renders the game over screen.

        Parameters
        ----------
        status : str
            The reason for the game ending. Could be either "checkmate", "stalemate",
            "threefold repetition" or "fifty move rule". Depending on the status, the
            text displayed will be different.
        winner : str, optional
            The color of the winner. Only used if the status is "checkmate".
        """
        self.window.fill(constants.DARK)
        font = pygame.font.SysFont("Arial", 50)
        text = font.render("Game Over", True, constants.LIGHT)
        text_rect = text.get_rect(center=(constants.WINDOW_WIDTH // 2, 50))
        self.window.blit(text, text_rect)

        if status == "checkmate":
            text = font.render(f"Checkmate! {winner} wins!", True, constants.LIGHT)
        elif status == "stalemate":
            text = font.render("Stalemate!", True, constants.LIGHT)
        elif status == "threefold repetition":
            text = font.render("Draw by repetition!", True, constants.LIGHT)
        elif status == "fifty move rule":
            text = font.render(
                "Draw by fifty moves with no pawn moves or captures!",
                True,
                constants.LIGHT,
            )

        self.window.blit(text, text.get_rect(center=(constants.WINDOW_WIDTH // 2, 100)))

        pygame.display.flip()

    @classmethod
    def initialize_images(cls) -> None:
        """Initializes the class variable piece_images with the images of the chess pieces
        from the assets folder."""
        cls.piece_images = {
            "white-pawn": pygame.image.load(
                constants.ASSETS_PATH + "white-pawn.png"
            ).convert_alpha(),
            "white-rook": pygame.image.load(
                constants.ASSETS_PATH + "white-rook.png"
            ).convert_alpha(),
            "white-knight": pygame.image.load(
                constants.ASSETS_PATH + "white-knight.png"
            ).convert_alpha(),
            "white-bishop": pygame.image.load(
                constants.ASSETS_PATH + "white-bishop.png"
            ).convert_alpha(),
            "white-queen": pygame.image.load(
                constants.ASSETS_PATH + "white-queen.png"
            ).convert_alpha(),
            "white-king": pygame.image.load(
                constants.ASSETS_PATH + "white-king.png"
            ).convert_alpha(),
            "black-pawn": pygame.image.load(
                constants.ASSETS_PATH + "black-pawn.png"
            ).convert_alpha(),
            "black-rook": pygame.image.load(
                constants.ASSETS_PATH + "black-rook.png"
            ).convert_alpha(),
            "black-knight": pygame.image.load(
                constants.ASSETS_PATH + "black-knight.png"
            ).convert_alpha(),
            "black-bishop": pygame.image.load(
                constants.ASSETS_PATH + "black-bishop.png"
            ).convert_alpha(),
            "black-queen": pygame.image.load(
                constants.ASSETS_PATH + "black-queen.png"
            ).convert_alpha(),
            "black-king": pygame.image.load(
                constants.ASSETS_PATH + "black-king.png"
            ).convert_alpha(),
        }

    @staticmethod
    def get_square_at_coords(coords: tuple) -> tuple:
        """Returns the square (i.e. the rank and file) at the given coordinates.

        Parameters
        ----------
        coords : tuple
            The coordinates of the square in (x, y) format, where x is the horizontal
            coordinate and y is the vertical coordinate.

        Returns
        -------
        tuple
            The square at the given coordinates in (rank, file) format, where rank is the
            row and file is the column."""
        return (coords[1] // constants.SQUARE_SIZE, coords[0] // constants.SQUARE_SIZE)

    @staticmethod
    def get_coords_of_square(position: tuple) -> tuple:
        """
        Returns the coordinates of the edge of a square given its position.

        Parameters
        ----------
        position : tuple
            The position of the square in (rank, file) format, where rank is the row and
            file is the column.

        Returns
        -------
        tuple
            The coordinates of the edge of the square in (x, y) format, where x is the
            horizontal coordinate and y is the vertical coordinate.
        """
        return (
            position[1] * constants.SQUARE_SIZE,
            position[0] * constants.SQUARE_SIZE,
        )

    @staticmethod
    def draw_circle(
        surface: pygame.Surface, color: str, coords: tuple, radius: int
    ) -> None:
        """Draws a circle on the given surface.

        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the circle on.
        color : str
            The color of the circle.
        coords : tuple
            The coordinates of the center of the circle in (x, y) format, where x is the
            horizontal coordinate and y is the vertical coordinate.
        radius : int
            The radius of the circle.
        """
        gfxdraw.aacircle(surface, coords[0], coords[1], radius, color)
        gfxdraw.filled_circle(surface, coords[0], coords[1], radius, color)


class Button:
    """Class used to draw clickable buttons on the screen."""

    def __init__(
        self,
        x: int,
        y: int,
        image: pygame.Surface,
        scale: float,
        return_value: str,
        window: pygame.Surface,
    ) -> None:
        # Initialize button
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(
            self.image,
            (int(self.image.get_width() * scale), int(self.image.get_height() * scale)),
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.return_value = return_value
        self.window = window
        self.is_clicked = False

    def draw(self) -> None:
        """Draw the button on the screen."""
        self.window.blit(self.image, self.rect.topleft)

    def check_click(self, event: pygame.event.Event) -> None:
        """Check if the button has been clicked by seeing if the
        pygame event (assumed to be a mouse click) is within the button's rect.)"""
        if self.rect.collidepoint(event.pos):
            self.is_clicked = True


class PromotionBox:
    """Class used to draw a popup box that allows the user to choose a piece to promote to."""

    def __init__(self, window: pygame.Surface, piece_color: str) -> None:
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
        button_x = self.x + (self.width - constants.SQUARE_SIZE) // 2
        self.buttons.append(
            Button(
                button_x,
                200,
                f"./game/assets/{piece_color}-queen.png",
                1,
                "Q",
                self.window,
            )
        )
        self.buttons.append(
            Button(
                button_x,
                300,
                f"./game/assets/{piece_color}-rook.png",
                1,
                "R",
                self.window,
            )
        )
        self.buttons.append(
            Button(
                button_x,
                400,
                f"./game/assets/{piece_color}-bishop.png",
                1,
                "B",
                self.window,
            )
        )
        self.buttons.append(
            Button(
                button_x,
                500,
                f"./game/assets/{piece_color}-knight.png",
                1,
                "N",
                self.window,
            )
        )

        # Define final choice
        self.final_choice = None
        self.show()

    def show(self) -> None:
        """Display the popup window.

        The popup window provides the player whose turn it is with the option to promote
        a pawn to a queen, rook, bishop, or knight. The game loop is effectively blocked
        until the player makes a choice. However, they may still close the game."""
        # Show popup window
        self.window.blit(self.surface, (self.x, self.y))
        self.draw()
        self.window.blit(
            self.text, (self.x + (self.width - self.text.get_width()) // 2, 140)
        )
        self.get_promotion_choice()

    def draw(self) -> None:
        """Draws each button onto the surface of the popup window."""
        for button in self.buttons:
            button.draw()

    def get_promotion_choice(self) -> None:
        """Blocks the game loop until the player clicks one of the buttons and
        makes a choice. After that, the final choice is stored in the attribute
        self.final_choice."""
        while self.final_choice is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        button.check_click(event)
                        if button.is_clicked:
                            self.final_choice = button.return_value
                            button.is_clicked = False

            pygame.display.update()
