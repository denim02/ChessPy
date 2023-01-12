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
        self.render_board(self.canvas)
        self.canvas.pack()
        self.root.mainloop()


    def render_board(self, canvas):
        print(self.game.board)
        for row in range(8):
            for col in range(8):
                x1, y1 = col * square_size, row * square_size
                x2, y2 = x1 + square_size, y1 + square_size
                color = "#EEEEE2" if (row + col) % 2 == 0 else "#769656"
                canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                piece = self.game.get_piece((row, col))
                if piece:
                    piece.image = tk.PhotoImage(file=f"./assets/{piece.color}-{piece.name}.png")
                    image_on_board = canvas.create_image(x1, y1, anchor=tk.NW, image=piece.image)
                    canvas.tag_bind(image_on_board, "<ButtonPress-1>", self.on_drag_start)
                    canvas.tag_bind(image_on_board, "<B1-Motion>", self.on_drag_motion)
                    canvas.tag_bind(image_on_board, "<ButtonRelease-1>", self.on_drag_release)
                    
    def on_drag_start(self, event):
        self.dragged_piece = event.widget.find_closest(event.x, event.y)[0]
        # Original position of piece
        self.original_piece_pos = self.canvas.coords(self.dragged_piece)
        self.offset_x = event.x - self.canvas.coords(self.dragged_piece)[0]
        self.offset_y = event.y - self.canvas.coords(self.dragged_piece)[1]
        self.dragged_piece_pos = self.canvas.coords(self.dragged_piece)
        self.canvas.tag_raise(self.dragged_piece)
        
    def on_drag_motion(self, event):
        self.canvas.move(self.dragged_piece, event.x - self.dragged_piece_pos[0] - self.offset_x, 
                         event.y - self.dragged_piece_pos[1] - self.offset_y)
        self.dragged_piece_pos = self.canvas.coords(self.dragged_piece)
        
    def on_drag_release(self, event):
        new_pos = self.get_square_at_position(event.x, event.y)
        if new_pos and self.game.is_valid_move(self.dragged_piece_pos, new_pos):
            x, y = new_pos[1] * square_size, new_pos[0] * square_size
            self.canvas.coords(self.dragged_piece, x, y)
            self.game.move_piece(self.get_piece_position(self.dragged_piece), new_pos)
        else:
            self.canvas.coords(self.dragged_piece, self.original_piece_pos)
        self.render_board()
            
    def get_square_at_position(self, x, y):
        col = int(x / square_size)
        row = int(y / square_size)
        return (row, col)
        
    def get_piece_position(self, piece_id):
        x, y = self.canvas.coords(piece_id)[:2]
        col = int(x / square_size)
        row = int(y / square_size)
        return (row, col)

game = ChessGame()
ui = ChessGameUI(game)
