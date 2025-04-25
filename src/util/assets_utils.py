# assets_utils.py
import pygame
from util.settings import TILE_SIZE

# Định nghĩa các đường dẫn (sửa để trỏ đúng từ thư mục src/)
BLOCK_TEXTURE_DIR_PATH: dict[int, str] = {
    1: "assets/block/Tetromino_block1_1.png",
    2: "assets/block/Tetromino_block1_2.png",
    3: "assets/block/Tetromino_block1_3.png",
    4: "assets/block/Tetromino_block1_4.png",
    5: "assets/block/Tetromino_block1_5.png",
    6: "assets/block/Tetromino_block1_6.png",
    7: "assets/block/Tetromino_block1_7.png",
}

MUSIC: dict[str, str] = {
    "start-up": "assets/music/start_up.mp3",
    "menu": "assets/music/menu_theme.mp3",
    "game": "assets/music/tetris_theme.mp3",
    "after-game": "assets/music/after_game.mp3"
}

SFX_DIR_PATH: dict[str, str] = {
    "hard-landing": "assets/sfx/hard_landing.wav",
    "line-clear": "assets/sfx/line_clear.wav",
    "select": "assets/sfx/select.wav"
}

GRID_IMG_DIR_PATH = "assets/img/Grid.png"
BORDER_IMG_DIR_PATH = "assets/img/Border.png"
TITLE_IMG_DIR_PATH = "assets/img/Title_No_BG.png"

COLORS: dict[str, tuple[int, int, int]] = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "gray": (169, 169, 169),
    "lightblue": (173, 216, 230),
}

BLOCK_TEXTURE: dict[int, pygame.Surface] = None

def shrink_image(image_path: str, target_size: tuple[int, int]) -> pygame.Surface:
    """Thu nhỏ hình ảnh về kích thước mục tiêu."""
    try:
        image: pygame.Surface = pygame.image.load(image_path).convert_alpha()
        bounding_rect: pygame.Rect = image.get_bounding_rect()
        cropped_image: pygame.Surface = image.subsurface(bounding_rect)
        scaled_image: pygame.Surface = pygame.transform.smoothscale(cropped_image, target_size)
        return scaled_image
    except pygame.error as e:
        print(f"Error loading image from {image_path}: {e}")
        raise

def load_block_textures() -> dict[int, pygame.Surface]:
    """Tải texture cho các khối."""
    global BLOCK_TEXTURE
    if BLOCK_TEXTURE is None:
        BLOCK_TEXTURE = {}
        for key, path in BLOCK_TEXTURE_DIR_PATH.items():
            try:
                BLOCK_TEXTURE[key] = shrink_image(path, (TILE_SIZE, TILE_SIZE))
            except pygame.error as e:
                print(f"Error loading texture for block {key} from {path}: {e}")
                raise FileNotFoundError(f"Could not load texture for block {key} from {path}")
    return BLOCK_TEXTURE

def draw_loading_bar(screen, duration=5000, width=400, height=50, x=None, y=None,
                     bg_color=COLORS.get("black"),
                     fill_color=COLORS.get("yellow"),
                     border_color=COLORS.get("white"),
                     border_width=2):
    screen_width, screen_height = screen.get_size()

    if x is None:
        x = (screen_width - width) // 2
    if y is None:
        y = (screen_height - height) // 2

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return  # exit early if window closed

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        progress = min(1, elapsed_time / duration)
        fill_width = int(width * progress)

        screen.fill(COLORS.get("black"))

        # Border
        pygame.draw.rect(screen, border_color, (x, y, width, height), border_width)

        # Background inside bar
        pygame.draw.rect(screen, bg_color, (
            x + border_width, y + border_width,
            width - 2 * border_width, height - 2 * border_width
        ))

        # Progress fill
        pygame.draw.rect(screen, fill_color, (
            x + border_width, y + border_width,
            max(0, fill_width - 2 * border_width), height - 2 * border_width
        ))

        pygame.display.flip()

        if elapsed_time >= duration:
            running = False

        clock.tick(5)

