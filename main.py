"""
main.py
This module contains the main script for running a chess game with a graphical user interface.
It imports the ChessGame and ChessUI classes from the game and graphics modules, respectively.
It creates an instance of the ChessGame and ChessUI classes, and runs the game with the UI.
"""
from chess_game.game import ChessGame
from chess_game.graphics import ChessUI
import pygame

game = ChessGame()
ui = ChessUI(game)

def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        ui.render_board()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
