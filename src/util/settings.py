# settings.py
FRAME_W: int = 1000
FRAME_H: int = 800
FRAME_RES: tuple[int, int] = (FRAME_W, FRAME_H)

FONT_DIR_PATH: str = "assets/font/PressStart2P-Regular.ttf"

BLOCK_OFFSET_X: int = 50 # Offset between the image and the grid inside it
BLOCK_OFFSET_Y: int = 100 # Offset between the image and the grid inside it
BLOCK_OFFSET: tuple[int, int] = (BLOCK_OFFSET_X, BLOCK_OFFSET_Y)
TILE_SIZE: int = 30