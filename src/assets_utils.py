import pygame
from settings import TILE_SIZE

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
    "line-clear": "assets/sfx/line_clear.wav"
}

GRID_IMG_DIR_PATH = "assets/Grid.png"
BORDER_IMG_DIR_PATH = "assets/Border.png"

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


def shrink_image(image_path: str, target_size: tuple[int, int]) -> pygame.Surface:
    image: pygame.Surface = pygame.image.load(image_path).convert_alpha()
    bounding_rect: pygame.Rect = image.get_bounding_rect()
    cropped_image: pygame.Surface = image.subsurface(bounding_rect)
    scaled_image: pygame.Surface = pygame.transform.smoothscale(cropped_image, target_size)
    return scaled_image

def scale_image(dir_path: str, target_size: tuple[int, int]) -> pygame.Surface:
    image = pygame.image.load(dir_path).convert_alpha()
    orig_w, orig_h = image.get_size()
    target_w, target_h = target_size

    scale_factor = min(target_w / orig_w, target_h / orig_h)

    new_w = int(orig_w * scale_factor)
    new_h = int(orig_h * scale_factor)

    scaled_image = pygame.transform.smoothscale(image, (new_w, new_h))

    return scaled_image

def play_music(track: str, loop: bool = True) -> None:
    if track in MUSIC:
        try:
            # Initialize the mixer if not already initialized
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            pygame.mixer.music.load(MUSIC.get(track))
            pygame.mixer.music.play(-1 if loop else 0)
            pygame.mixer.music.set_volume(1.0)
        except pygame.error as e:
            print(f"Error playing music: {e}")

def pause_music():
    pygame.mixer.music.pause()

def resume_music():
    pygame.mixer.music.unpause()

def stop_music():
    pygame.mixer.music.stop()


def load_sfx() -> dict[str, pygame.mixer.Sound]:
    pygame.mixer.init()
    loaded_sfx = {name: pygame.mixer.Sound(path) for name, path in SFX_DIR_PATH.items()}
    return loaded_sfx

def load_block_textures() -> dict[int, pygame.Surface]:
    loaded_texture = {key: shrink_image(path, (TILE_SIZE, TILE_SIZE)) for key, path in BLOCK_TEXTURE_DIR_PATH.items()}
    return loaded_texture

import pygame

def create_tiled_background(screen: pygame.Surface, tile: pygame.Surface) -> pygame.Surface:
    screen_width, screen_height = screen.get_size()
    tile_width, tile_height = tile.get_size()

    background = pygame.Surface((screen_width, screen_height))
    
    for x in range(0, screen_width, tile_width):
        for y in range(0, screen_height, tile_height):
            background.blit(tile, (x, y))

    return background

def draw_tiled_background(screen: pygame.Surface, tiled_bg: pygame.Surface):
    screen.blit(tiled_bg, (0, 0))




SFX: dict[str, pygame.mixer.Sound] = load_sfx()
BLOCK_TEXTURE: dict[int, pygame.Surface] = load_block_textures()
