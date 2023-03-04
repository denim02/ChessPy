"""
main.py
This module contains the main script for running a chess game with a graphical user interface.
It imports the ChessGame and ChessUI classes from the game and graphics modules, respectively.
It creates an instance of the ChessGame and ChessUI classes, and runs the game with the UI.
"""
from chess_game.game import ChessGame
from chess_game.graphics import ChessUI

game = ChessGame()
ui = ChessUI(game)
