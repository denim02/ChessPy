from PIL import Image   # Using the Python Image Library to crop the sprites

# Open the spritesheet image
with Image.open("./assets/piece_spritesheet.png") as spritesheet:
    # Cropping out each individual piece
    for i in range(12):
        x = i % 6 * 90
        y = i // 6 * 90
        piece = spritesheet.crop((x, y, x + 90, y + 90))
        piece.save(f"./assets/{i}.png")