import tkinter as tk

def draw_chessboard():
    root = tk.Tk()
    root.geometry("1280x800")
    canvas = tk.Canvas(root, width=1280, height=800)
    canvas.pack()

    square_size = 90
    x_offset = (1280 - 720) / 2
    y_offset = (800 - 720) / 2

    # Draw the squares
    for row in range(8):
        for col in range(8):
            x1 = col * square_size + x_offset
            y1 = row * square_size + y_offset
            x2 = x1 + square_size
            y2 = y1 + square_size
            color = "#EEEEE2" if (row + col) % 2 == 0 else "#769656"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    # Draw the pieces
    pieces = [
        0, 1, 2, 3, 4, 2, 1, 0, 
        5, 5, 5, 5, 5, 5, 5, 5,
        None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None,
        11, 11, 11, 11, 11, 11, 11, 11,
        6, 7, 8, 9, 10, 8, 7, 6
    ]

    root.mainloop()

draw_chessboard()