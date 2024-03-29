"""The game module contains the ChessGame class, which is responsible for managing the state
of the game and making moves on the board. It also contains the run_game function (i.e. the main function)
which bootstraps the game logic and the UI and runs the game loop."""
import pygame
import os.path
import datetime
import chess_game.chess_logic as chess_logic
import chess_game.constants as constants
from chess_game.pieces import King, Pawn
from chess_game.board import Board
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from chess_game.pieces import Piece


class ChessGame:
    """The ChessGame class is responsible for managing the state of the game and making moves on the board.
    Additionally, it is responsible for logging the moves and checking for game over conditions."""

    def __init__(self):
        # Variables for handling the game mechanics
        self.board = Board()
        self.board.populate_board()
        self.captured_pieces = {"white": [], "black": []}
        self.turn = "white"

        # Variable specifically for pawn promotion
        self.promotion_choice = None

        # Variables for game over conditions
        self.is_checkmate = False
        self.is_stalemate = False
        self.is_threefold_repetition = False
        self.fifty_move_counter = 0

        # Variable for logging
        self.position_log = []
        self.move_log_enabled = constants.MOVE_LOG_ENABLED
        self.move_log_file_path = (
            constants.MOVE_LOG_DIRECTORY
            + "g_"
            + datetime.datetime.now().strftime("%y%m%d_%H%M")
            + ".txt"
        )
        if self.move_log_enabled and os.path.exists(self.move_log_file_path):
            self.move_log_file_path = self.move_log_file_path[:-4] + "_1.txt"

        self.fullmove_counter = 0
        self.halfmove_counter = 0

        # Add initial position to the log
        self.position_log.append(self.get_current_game_position())

    def make_move(self, original_position: tuple, new_position: tuple) -> None:
        """Execute a move on the board.

        This method is responsible for executing a move on the board, checking if the move is legal,
        checking for game over conditions and logging the move. It distinguishes between a normal move,
        a capture, a pawn promotion and a castle and handles each case accordingly. Additionally, it
        contains some side effects such as updating the turn, incrementing the fifty-move-draw counter,
        and updating the position log.

        Parameters
        ----------
        original_position : tuple
            Position of the piece to be moved.
        new_position : tuple
            New position of the piece to be moved.

        Raises
        ------
        TypeError
            If there is no piece at the given position.
        ValueError
            If the move is illegal.
        Exception
            If it is not the turn of the player whose piece is being moved or if the move
            would put the player's king in check
        """
        print(
            f"Original position: {self.board.get_algebraic_notation(original_position)}\n"
            f"New position: {self.board.get_algebraic_notation(new_position)}"
        )
        piece = self.board.get_piece_at_square(original_position)

        # Check for invalid moves
        if piece is None:
            raise TypeError("No piece at the given position.")
        if piece.color != self.turn:
            raise Exception("It is not your turn.")
        if new_position not in piece.legal_moves:
            raise ValueError("Illegal move.")
        if chess_logic.is_king_in_check_after_move(self.board, piece, new_position):
            raise Exception("This move would put your king in check.")

        captured_piece = None

        # Check if the desired move is a castle.
        if isinstance(piece, King) and abs(new_position[1] - original_position[1]) > 1:
            # Check if the king is castling to the left.
            if new_position[1] < original_position[1]:
                rook = self.board.get_piece_at_square((original_position[0], 0))
                self.board.move_piece_to_square(rook, (original_position[0], 3))

            # Check if the king is castling to the right.
            else:
                rook = self.board.get_piece_at_square((original_position[0], 7))
                self.board.move_piece_to_square(rook, (original_position[0], 5))

        # Move the piece to the new position.
        captured_piece = self.board.move_piece_to_square(piece, new_position)

        # Check if the desired move is a pawn promotion
        if self.promotion_choice is not None:
            self.board.promote_pawn(piece, self.promotion_choice)
            self.promotion_choice = None

        # Counter for fifty-move-draw rule.
        if captured_piece is None and not isinstance(piece, Pawn):
            self.fifty_move_counter += 1
        else:
            self.fifty_move_counter = 0

        # Keep track of captured pieces
        if captured_piece is not None:
            self.captured_pieces[self.turn].append(captured_piece)

        self.turn = "white" if self.turn == "black" else "black"

        # Increment the halfmove clock
        self.halfmove_counter += 1

        # Incremented by one every time black moves; if the turn is white then
        # black just moved.
        if self.turn == "white":
            self.fullmove_counter += 1

        # Log the current position
        self.position_log.append(self.get_current_game_position())
        if self.move_log_enabled:
            self.log_move(piece, original_position, captured_piece)

        # Check for game over conditions
        self.is_checkmate = chess_logic.is_checkmate(self.board, self.turn)
        self.is_stalemate = chess_logic.is_stalemate(self.board, self.turn)
        self.is_threefold_repetition = self.check_threefold_repetition()

    def get_current_game_position(self) -> dict:
        """Returns a dictionary containing information about the current game position.

        The dictionary has information on the placement of pieces on the board in FEN notation,
        the color which has the next move, castling rights, and the en passant target square.

        Returns
        -------
        dict
            A dictionary containing information about the current game position.
        """
        game_state = self.get_fen_game_state()

        return {
            "piece_placement": game_state["piece_placement"],
            "turn": game_state["turn"],
            "castling_availability": game_state["castling_availability"],
            "en_passant_target_square": game_state["en_passant_target_square"],
        }

    def check_threefold_repetition(self) -> bool:
        """Checks if the current position has occurred three times or more.

        Returns
        -------
        bool
            True if the current position has occurred three times or more, False otherwise.
        """
        if self.position_log.count(self.get_current_game_position()) >= 3:
            return True
        return False

    def get_fen_game_state(self) -> dict:
        """Returns a dictionary containing information about the current game state in FEN notation.

        The dictionary has information on the placement of pieces on the board in FEN notation,
        the color which has the next move, castling rights, the en passant target square, the
        halfmove clock, and the fullmove counter.

        Returns
        -------
        dict
            A dictionary containing information about the current game state in FEN notation.
        """
        board_state = self.board.get_fen_board_state()
        return {
            "piece_placement": board_state["piece_placement"],
            "turn": self.turn[0].lower(),
            "castling_availability": board_state["castling_availability"],
            "en_passant_target_square": board_state["en_passant_target_square"],
            "halfmove_clock": self.halfmove_counter,
            "fullmove_counter": self.fullmove_counter,
        }

    def log_move(
        self,
        piece: "Piece",
        original_position: tuple,
        captured_piece: Optional["Piece"] = None,
    ) -> None:
        """Logs a move represented in algebraic notation to a move log file.

        Parameters
        ----------
        piece : Piece
            The piece that is being moved.
        original_position : tuple
            The original position of the piece.
        captured_piece : Piece, optional
            The piece that was captured by the move, if there is one. Defaults to None.
        """
        move = self.get_move_in_algebraic_notation(
            piece, original_position, captured_piece
        )
        with open(self.move_log_file_path, "a") as file:
            # Check if it is the first move of a new turn.
            if self.halfmove_counter % 2 != 0:
                file.write(str(self.fullmove_counter + 1) + ". " + move + " ")
            else:
                file.write(move + "\n")

    def get_move_in_algebraic_notation(
        self,
        piece: "Piece",
        original_position: tuple,
        captured_piece: Optional["Piece"] = None,
    ) -> str:
        """Returns a move represented in algebraic notation.

        The function takes in a piece, its original position, and the piece that was captured by
        the move (if there is one) and returns the move in algebraic notation. To parse the move into
        algebraic notation, the function distinguishes between regular moves, captures, en passants,
        pawn promotions, castles, and moves that place a player into check or checkmate.

        Parameters
        ----------
        piece : Piece
            The piece that is being moved.
        original_position : tuple
            The original position of the piece.
        captured_piece : Piece, optional
            The piece that was captured by the move, if there is one. Defaults to None.

        Returns
        -------
        str
            The move represented in algebraic notation.
        """
        new_position = piece.position
        piece_notation = piece.to_algebraic_notation().upper()
        new_position_notation = self.board.get_algebraic_notation(new_position)

        result = ""

        # Check if the move is a castle.
        if isinstance(piece, King) and abs(new_position[1] - original_position[1]) > 1:
            # Check if the king is castling to the left (queenside).
            if new_position[1] < original_position[1]:
                result += "O-O-O"
            # Check if the king is castling to the right (kingside).
            else:
                result += "O-O"
        # Check if the move is a pawn promotion.
        elif isinstance(piece, Pawn) and (new_position[0] == 0 or new_position[0] == 7):
            result += (
                new_position_notation
                + "="
                + self.board.get_piece_at_square(new_position)
                .to_algebraic_notation()
                .upper()
            )
        # Check if the move is a capture.
        elif captured_piece is not None:
            # Check if the capture was done by a pawn
            if isinstance(piece, Pawn):
                result += (
                    self.board.get_algebraic_notation(original_position)[0]
                    + "x"
                    + new_position_notation
                )
                # If en passant
                if (
                    isinstance(captured_piece, Pawn)
                    and captured_piece.position[0] != new_position[0]
                ):
                    result += "e.p."
            # Otherwise, the capture was done by a piece other than a pawn.
            else:
                result += piece_notation + "x" + new_position_notation
        # Check if the move is a pawn move.
        elif isinstance(piece, Pawn):
            result += new_position_notation
        # Then it must be a normal move.
        else:
            result += piece_notation + new_position_notation

        # Check if the move is a checkmate.
        if chess_logic.is_checkmate(self.board, self.turn):
            result += "#"
        # Check if the move is a check.
        elif chess_logic.is_check(self.board, self.turn):
            result += "+"

        return result


def run_game() -> None:
    """Runs the main game loop for the chess game and handles user input, updating the game state,
    and interfacing between the different components of the game (logic, board state, graphics)."""
    # Import for the graphics module is placed here so the method definitions inside it do not
    # count towards the coverage report and pollute its results.
    from chess_game.graphics import ChessUI, PromotionBox

    # Initialize pygame.
    pygame.init()
    clock = pygame.time.Clock()

    # Create the game and ui objects.
    game = ChessGame()
    ui = ChessUI(game.board)

    # Create flag for the game loop.
    is_running = True

    # Create flag for displaying game_over screen.
    is_game_over = False
    game_status = ""

    while is_running:
        clock.tick(60)

        for event in pygame.event.get():
            # Check if the user presses the close button.
            if event.type == pygame.QUIT:
                is_running = False

            if not is_game_over and is_running:
                # If the user left clicks on the board, check whether they clicked on a piece.
                # If they did, then set the ui.dragged_piece to that piece.
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked_piece = game.board.get_piece_at_square(
                        ui.get_square_at_coords(event.pos)
                    )
                    if clicked_piece and clicked_piece.color == game.turn:
                        ui.dragged_piece = clicked_piece
                        ui.is_dragging = True
                        ui.original_coords = ui.dragged_piece.coords
                        ui.offset = (
                            event.pos[0] - ui.dragged_piece.coords[0],
                            event.pos[1] - ui.dragged_piece.coords[1],
                        )

                # If the user is dragging a piece, then update the position of
                # the piece.
                elif event.type == pygame.MOUSEMOTION:
                    if ui.is_dragging:
                        ui.dragged_piece.coords = (
                            event.pos[0] - ui.offset[0],
                            event.pos[1] - ui.offset[1],
                        )

                # If the user was dragging a piece, then check whether they dropped it on a valid square.
                # If they did, then make the move.
                elif event.type == pygame.MOUSEBUTTONUP:
                    if ui.is_dragging:
                        ui.is_dragging = False
                        new_square = ui.get_square_at_coords(event.pos)

                        if new_square:
                            # Check if the move is a pawn promotion.
                            if (
                                ui.dragged_piece.name == "Pawn"
                                and new_square[0] in (0, 7)
                                and new_square in ui.dragged_piece.legal_moves
                            ):
                                ui.promotion_box = PromotionBox(
                                    ui.window, ui.dragged_piece.color
                                )
                                game.promotion_choice = ui.promotion_box.final_choice
                                ui.promotion_box = None

                            # Make the move.
                            try:
                                game.make_move(ui.dragged_piece.position, new_square)
                            except Exception as ex:
                                print(ex)
                                ui.dragged_piece.coords = ui.original_coords

                            ui.dragged_piece = None

                            if (
                                game.is_checkmate
                                or game.is_stalemate
                                or game.is_threefold_repetition
                                or game.fifty_move_counter >= 50
                            ):
                                if game.is_checkmate:
                                    game_status = "checkmate"
                                elif game.is_stalemate:
                                    game_status = "stalemate"
                                elif game.is_threefold_repetition:
                                    game_status = "threefold repetition"
                                elif game.fifty_move_counter >= 50:
                                    game_status = "fifty move rule"

                                is_game_over = True

                        else:
                            ui.dragged_piece.coords = ui.original_coords

        if is_game_over:
            winner = "White" if game.turn == "black" else "Black"
            ui.render_gameover(game_status, winner)
        else:
            ui.render_all()
        pygame.display.update()

    pygame.quit()


def run_multiplayer() -> None:
    """Runs the main game loop for the chess game and handles user input, updating the game state,
    and interfacing between the different components of the game (logic, board state, graphics)."""
    # Import for the graphics module is placed here so the method definitions inside it do not
    # count towards the coverage report and pollute its results.
    from chess_game.graphics import ChessUI, PromotionBox
    from chess_game.networking import ClientConnect, ServerConnect

    # Initialize pygame.
    pygame.init()
    clock = pygame.time.Clock()

    # Create the game and ui objects.
    game = ChessGame()
    ui = ChessUI(game.board)
    socket = (
        ServerConnect(constants.PORT)
        if constants.START_AS_WHITE
        else ClientConnect(constants.HOST, constants.PORT)
    )
    player_color = "white" if constants.START_AS_WHITE else "black"

    # Create flag for the game loop.
    is_running = True

    # Create flag for displaying game_over screen.
    is_game_over = False
    game_status = ""

    # If the player is the server, then wait for 30s for the client to connect.
    if constants.START_AS_WHITE:
        socket.wait_for_client()

    while is_running:
        clock.tick(60)

        for event in pygame.event.get():
            # Check if the user presses the close button.
            if event.type == pygame.QUIT:
                is_running = False

            if not is_game_over and is_running:
                if player_color == game.turn:
                    # If the user left clicks on the board, check whether they clicked on a piece.
                    # If they did, then set the ui.dragged_piece to that piece.
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        clicked_piece = game.board.get_piece_at_square(
                            ui.get_square_at_coords(event.pos)
                        )
                        if clicked_piece and clicked_piece.color == game.turn:
                            ui.dragged_piece = clicked_piece
                            ui.is_dragging = True
                            ui.original_coords = ui.dragged_piece.coords
                            ui.offset = (
                                event.pos[0] - ui.dragged_piece.coords[0],
                                event.pos[1] - ui.dragged_piece.coords[1],
                            )

                    # If the user is dragging a piece, then update the position of
                    # the piece.
                    elif event.type == pygame.MOUSEMOTION:
                        if ui.is_dragging:
                            ui.dragged_piece.coords = (
                                event.pos[0] - ui.offset[0],
                                event.pos[1] - ui.offset[1],
                            )

                    # If the user was dragging a piece, then check whether they dropped it on a valid square.
                    # If they did, then make the move.
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if ui.is_dragging:
                            ui.is_dragging = False
                            new_square = ui.get_square_at_coords(event.pos)

                            if new_square:
                                # Check if the move is a pawn promotion.
                                if (
                                    ui.dragged_piece.name == "Pawn"
                                    and new_square[0] in (0, 7)
                                    and new_square in ui.dragged_piece.legal_moves
                                ):
                                    ui.promotion_box = PromotionBox(
                                        ui.window, ui.dragged_piece.color
                                    )
                                    game.promotion_choice = (
                                        ui.promotion_box.final_choice
                                    )
                                    ui.promotion_box = None

                                # Make the move.
                                try:
                                    original_square = ui.dragged_piece.position
                                    promotion_choice = game.promotion_choice
                                    game.make_move(
                                        ui.dragged_piece.position, new_square
                                    )
                                    socket.send_move(
                                        original_square, new_square, promotion_choice
                                    )
                                except ConnectionAbortedError:  # Connection closed.
                                    is_running = False
                                    print("Connection closed.")
                                except Exception as ex:
                                    print(ex)
                                    ui.dragged_piece.coords = ui.original_coords

                                ui.dragged_piece = None

                                if (
                                    game.is_checkmate
                                    or game.is_stalemate
                                    or game.is_threefold_repetition
                                    or game.fifty_move_counter >= 50
                                ):
                                    if game.is_checkmate:
                                        game_status = "checkmate"
                                    elif game.is_stalemate:
                                        game_status = "stalemate"
                                    elif game.is_threefold_repetition:
                                        game_status = "threefold repetition"
                                    elif game.fifty_move_counter >= 50:
                                        game_status = "fifty move rule"

                                    is_game_over = True

                            else:
                                ui.dragged_piece.coords = ui.original_coords

                else:
                    try:
                        move = socket.receive_move()
                        print(move)
                        game.promotion_choice = move["promotion_choice"]
                        game.make_move(move["old_position"], move["new_position"])

                        if (
                            game.is_checkmate
                            or game.is_stalemate
                            or game.is_threefold_repetition
                            or game.fifty_move_counter >= 50
                        ):
                            if game.is_checkmate:
                                game_status = "checkmate"
                            elif game.is_stalemate:
                                game_status = "stalemate"
                            elif game.is_threefold_repetition:
                                game_status = "threefold repetition"
                            elif game.fifty_move_counter >= 50:
                                game_status = "fifty move rule"

                            is_game_over = True
                    except BlockingIOError:  # No data received.
                        pass
                    except ConnectionAbortedError:  # Connection closed.
                        is_running = False
                        print("Connection closed.")
                    except Exception as ex:
                        print(ex)
                        ui.dragged_piece.coords = ui.original_coords

        if is_game_over:
            winner = "White" if game.turn == "black" else "Black"
            ui.render_gameover(game_status, winner)
        else:
            ui.render_all()
        pygame.display.update()

    pygame.quit()
