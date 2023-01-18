from PIL import Image  # Using the Python Image Library to crop the sprites
import tkinter as tk

square_size = 90


class ChessUI:
    def __init__(self, game):
        """
        Initializes the board and the game.

        Parameters:
            game (ChessGame): the game to be played.
        """
        self.game = game
        self.board = game.board
        self.turn = game.turn
        self.game_over = game.game_over
        self.window = tk.Tk()
        self.window.title("Chess")
        self.window.geometry("720x720")
        self.window.resizable(False, False)
        self.canvas = tk.Canvas(self.window, width=720, height=720, bg="white")
        self.render_board()
        self.canvas.pack()
        self.window.mainloop()

    def render_board(self):
        """
        Renders the board.
        """
        for row in range(8):
            for col in range(8):
                x1, y1 = col * square_size, row * square_size
                x2, y2 = x1 + square_size, y1 + square_size
                color = "#EEEEE2" if (row + col) % 2 == 0 else "#769656"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                self.render_piece((row, col))

    def render_piece(self, position):
        """
        Renders the piece at the given position.

        Parameters:
            position (tuple): the position of the piece to be rendered in (x, y) format, where x is the row and y is the column.
        """
        piece = self.board.get_piece_at_square(position)
        if piece:
            x1, y1 = position[1] * square_size, position[0] * square_size
            piece.image = tk.PhotoImage(file=f"./assets/{piece.color}-{piece.name}.png")
            image_on_board = self.canvas.create_image(
                x1, y1, anchor=tk.NW, image=piece.image
            )
            self.canvas.tag_bind(image_on_board, "<ButtonPress-1>", self.on_drag_start)
            self.canvas.tag_bind(image_on_board, "<B1-Motion>", self.on_drag_motion)
            self.canvas.tag_bind(
                image_on_board, "<ButtonRelease-1>", self.on_drag_release
            )

    def on_drag_start(self, event):
        self.dragged_piece_image = event.widget.find_closest(event.x, event.y)[0]
        self.dragged_piece = self.board.get_piece_at_square(
            (int(event.y // square_size), int(event.x // square_size))
        )
        self.dragged_image_coords = self.canvas.coords(self.dragged_piece_image)

        self.original_coords = self.canvas.coords(self.dragged_piece_image)
        self.original_position = self.dragged_piece.position

        self.offset_x = event.x - self.canvas.coords(self.dragged_piece_image)[0]
        self.offset_y = event.y - self.canvas.coords(self.dragged_piece_image)[1]
        for row in range(8):
            for col in range(8):
                if (row, col) in self.board.get_legal_moves(
                    self.board.get_piece_at_square(self.dragged_piece.position)
                ):
                    x, y = (
                        col * square_size + square_size / 2,
                        row * square_size + square_size / 2,
                    )
                    circle = self.canvas.create_oval(
                        x - 15,
                        y - 15,
                        x + 15,
                        y + 15,
                        fill="#C0C0C0",
                        outline="gray",
                        width=1,
                        tags="highlight",
                    )
                    self.canvas.tag_raise(circle)
        self.canvas.tag_raise(self.dragged_piece_image)

    def on_drag_motion(self, event):
        self.canvas.move(
            self.dragged_piece_image,
            event.x - self.dragged_image_coords[0] - self.offset_x,
            event.y - self.dragged_image_coords[1] - self.offset_y,
        )
        self.dragged_image_coords = self.canvas.coords(self.dragged_piece_image)

    def on_drag_release(self, event):
        x, y = (
            round(self.dragged_image_coords[0] / square_size) * square_size,
            round(self.dragged_image_coords[1] / square_size) * square_size,
        )
        new_position = (y // square_size, x // square_size)
        try:
            self.game.make_move(self.original_position, new_position)
            self.canvas.coords(self.dragged_piece_image, x, y)
        except ValueError as e:
            self.canvas.coords(self.dragged_piece_image, self.original_coords)
            print(f"Move error: {e}")
        self.render_board()


def crop_sprites(file_path, square_size):
    # Open the spritesheet image
    with Image.open(file_path) as spritesheet:
        # Cropping out each individual piece (6 pieces per row)
        for i in range(12):
            x = i % 6 * square_size
            y = i // 6 * square_size
            piece = spritesheet.crop((x, y, x + square_size, y + square_size))
            piece.save(f"{file_path}/{i}.png")
