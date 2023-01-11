import tkinter as tk
from game import ChessGame

square_size = 90

def on_piece_move(from_position, to_position):
    # Handle the move event
    game.move_piece(from_position, to_position)

class ChessGameUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=1280, height=860)
        self.canvas.pack()
        self.render_board(self.canvas)
        self.root.mainloop()


    def render_board(self, canvas):
        for row in range(8):
            for col in range(8):
                x1, y1 = col * square_size, row * square_size
                x2, y2 = x1 + square_size, y1 + square_size
                piece = self.game.get_piece(row, col)
                if piece:
                    # Create an image of the chess piece
                    img = tk.PhotoImage(file=piece.image_path)
                    image_on_board = canvas.create_image(x1, y1, image=img, anchor="nw")
                    canvas.tag_bind(image_on_board, "<Button-1>",  lambda event, fp= piece.position, tp= (row, col):on_piece_move(fp,tp) )

game = ChessGame()
ui = ChessGameUI(game)
