"""
game.py
This module contains the ChessGame class.
This class is used to represent a chess game. It has properties like board, turn,
game_over and methods make_move, run etc. It is responsible for managing the
state of the game and making moves on the board.
"""
import chess_game.chess_logic as chess_logic
import pygame
from chess_game.graphics import ChessUI
from chess_game.pieces import King
from chess_game.board import Board
from chess_game.constants import *

class ChessGame:
    """
    ChessGame:
    This is a class for representing a chess game.
    It has properties like board, turn and game_over, and methods make_move, run etc.
    It is responsible for managing the state of the game and making moves on the board."""

    def __init__(self):
        """
        Initializes the board and the turn.
        """
        self.board = Board()
        self.pieces_taken = {
            "white": [],
            "black": []
        }
        self.turn = "white"
        self.game_over = False

    def make_move(self, original_position, new_position):
        """
        Make a move on the board.

        Parameters:
            original_position (tuple): original position on the board
                in (x, y) format, where x is the row and y is the column.
            new_position (tuple): new position on the board
                in (x, y) format, where x is the row and y is the column.
        """
        piece = self.board.get_piece_at_square(original_position)
        print(piece)
        print("Original position: ", original_position)
        print("New position: ", new_position)
        
        if piece is None:
            raise ValueError("No piece at the given position.")
        if piece.color != self.turn:
            raise ValueError("It is not your turn.")
        if new_position not in piece.legal_moves:
            raise ValueError("Invalid move.")
        if chess_logic.is_king_in_check_after_move(self.board, piece, new_position):
            raise ValueError("This move would put your king in check.")
        
        taken_piece = None

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

        taken_piece = self.board.move_piece_to_square(piece, new_position)
        print(self.board)
        if taken_piece is not None:
            self.pieces_taken[self.turn].append(taken_piece)
            print(self.pieces_taken)

        self.turn = "white" if self.turn == "black" else "black"

def run_game():
    game = ChessGame()
    ui = ChessUI(game)
    is_running = True
    clock = pygame.time.Clock()

    while is_running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the user left clicks on the board, check whether they clicked on a piece.
                # If they did, then set the ui.dragged_piece to that piece.
                if event.button == 1:
                    clicked_square = ui.get_square_at_coords(event.pos)
                    ui.dragged_piece = game.board.get_piece_at_square(clicked_square)
                    if ui.dragged_piece:
                        ui.is_dragging = True
                        ui.original_coords = ui.dragged_piece.coords
                        ui.offset = (
                            event.pos[0] -  ui.dragged_piece.coords[0],
                            event.pos[1] - ui.dragged_piece.coords[1],
                        )
                else:
                    continue
            elif event.type == pygame.MOUSEMOTION:
                # If the user is dragging a piece, then update the position of the piece.
                if ui.is_dragging:
                    ui.dragged_piece.coords = (
                        event.pos[0] - ui.offset[0],
                        event.pos[1] - ui.offset[1],
                    )
            elif event.type == pygame.MOUSEBUTTONUP:
                # If the user was dragging a piece, then check whether they dropped it on a valid square.
                # If they did, then make the move.
                if ui.is_dragging:
                    ui.is_dragging = False
                    new_square = ui.get_square_at_coords(event.pos)
                    if new_square:
                        try:
                            game.make_move(ui.dragged_piece.position, new_square)
                            # If the move was successful, then set the dragged_piece to None and move the piece to the
                            # center of the new square.
                            ui.dragged_piece.coords = (
                                round(event.pos[0] // SQUARE_SIZE * SQUARE_SIZE),
                                round(event.pos[1] // SQUARE_SIZE * SQUARE_SIZE),
                            )
                            ui.dragged_piece = None
                        except ValueError as error:
                            print(error)
                            ui.dragged_piece.coords = ui.original_coords
                            ui.dragged_piece = None
                    else:
                        ui.dragged_piece.coords = ui.original_coords

        ui.render_board()
        pygame.display.update()

    pygame.quit()