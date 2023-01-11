from PIL import Image   # Using the Python Image Library to crop the sprites

def crop_sprites(file_path, square_size):
    # Open the spritesheet image
    with Image.open(file_path) as spritesheet:
        # Cropping out each individual piece (6 pieces per row)
        for i in range(12):
            x = i % 6 * square_size
            y = i // 6 * square_size
            piece = spritesheet.crop((x, y, x + square_size, y + square_size))
            piece.save(f"{file_path}/{i}.png")