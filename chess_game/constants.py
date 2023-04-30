"""The constants module contains constants used throughout the game."""
"""GUI"""
# Window constants
WINDOW_WIDTH, WINDOW_HEIGHT = 720, 720
ROWS, COLS = 8, 8
SQUARE_SIZE = WINDOW_WIDTH // COLS

# Color palette
DARK = "#769656"
LIGHT = "#EEEEE2"

# Assets
ASSETS_PATH = "./game/assets/"

"""Game settings"""
FPS = 60
STARTING_FEN_FILE = "./game/game_states/init_position.fen"
MOVE_LOG_ENABLED = True
MOVE_LOG_DIRECTORY = "./game/logs/"
