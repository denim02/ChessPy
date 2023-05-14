"""Project: ChessPy
Student: Deni Mastori (ID: 200149096)
Class: Programming in Python

This is the main file for the chess game. It simply runs the game through
the run_game() function from the game module."""
from chess_game.game import run_game, run_multiplayer
import chess_game.constants as constants
import argparse


def main():

    if constants.START_IN_ONLINE_MODE:
        parser = argparse.ArgumentParser(description="A Chess Game Program")
        parser.add_argument("-s", "--server", action="store_true", help="Run as server")
        parser.add_argument("-c", "--client", action="store_true", help="Run as client")

        args = parser.parse_args()

        if args.server:
            constants.START_AS_WHITE = True
        elif args.client:
            constants.START_AS_WHITE = False
        else:
            print("Please specify whether to run as server or client")
            exit(1)

        run_multiplayer()
    else:
        run_game()


if __name__ == "__main__":
    main()
