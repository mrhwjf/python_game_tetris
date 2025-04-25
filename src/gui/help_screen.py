import pygame, sys
from util.settings import *
from util.assets_utils import COLORS

def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    """Hàm hỗ trợ tự động xuống dòng cho văn bản dài."""
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        test_surface = font.render(test_line, True, (255, 255, 255))
        if test_surface.get_width() <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())

    return lines

def show_help(screen, sound_manager) -> str:
    pygame.display.set_caption("Tetris - Help")

    # Fonts
    title_font = pygame.font.Font(FONT_DIR_PATH, 30)
    text_font = pygame.font.Font(FONT_DIR_PATH, 16)
    section_font = pygame.font.Font(FONT_DIR_PATH, 25)  

    # Colors
    background_color = COLORS.get("black")
    text_color = COLORS.get("white")
    highlight_color = COLORS.get("yellow")

    # Text content
    title_text = title_font.render("How to Play Tetris", True, highlight_color)
    rules_texts = [
        "Objective: Clear lines by filling them with blocks.",
        "1. Blocks fall from the top of the screen.",
        "2. Arrange blocks to fill a horizontal line.",
        "3. Filled lines will be cleared, earning you points.",
        "4. The game ends if blocks stack to the top."
    ]
    single_player_texts = [
        "Single Player Controls:",
        "Left Arrow: Move block left",
        "Right Arrow: Move block right",
        "Down Arrow: Immediately drop block",
        "Up Arrow/Space: Rotate block",
        "ESC: Pause/Resume",
        "R: Restart (when game over)"
    ]
    two_player_texts = [
        "Two Player Controls:",
        "Player 1: A (Left), D (Right), S (Down), W (Rotate)",
        "Player 2: Left Arrow, Right Arrow, Down Arrow, Up Arrow",
        "ESC: Pause/Resume",
        "R: Restart (when both players game over)"
    ]
    back_text = text_font.render("Press ESC to return to Menu", True, text_color)

    screen_width, screen_height = screen.get_size()
    max_text_width = screen_width - 40
    line_spacing = text_font.get_height() + 10
    section_spacing = 30

    help_surface = pygame.Surface(screen.get_size())
    help_surface.fill(background_color)

    title_rect = title_text.get_rect(center=(screen_width // 2, 40))
    help_surface.blit(title_text, title_rect)

    y_offset = 90

    for idx, line in enumerate(rules_texts):
        font = section_font if idx == 0 else text_font
        color = highlight_color if idx == 0 else text_color
        for wrapped in wrap_text(line, text_font, max_text_width):
            text_surface = text_font.render(wrapped, True, color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, y_offset))
            help_surface.blit(text_surface, text_rect)
            y_offset += line_spacing

    y_offset += section_spacing

    # Render Single Player Controls with larger font
    for idx, line in enumerate(single_player_texts):
        font = section_font if idx == 0 else text_font
        color = COLORS.get("green") if idx == 0 else text_color
        for wrapped in wrap_text(line, font, max_text_width):
            text_surface = font.render(wrapped, True, color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, y_offset))
            help_surface.blit(text_surface, text_rect)
            y_offset += line_spacing

    y_offset += section_spacing

    # Render Two Player Controls with larger font
    for idx, line in enumerate(two_player_texts):
        font = section_font if idx == 0 else text_font
        color = COLORS.get("red") if idx == 0 else text_color
        for wrapped in wrap_text(line, font, max_text_width):
            text_surface = font.render(wrapped, True, color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, y_offset))
            help_surface.blit(text_surface, text_rect)
            y_offset += line_spacing

    back_rect = back_text.get_rect(center=(screen_width // 2, screen_height - 40))
    help_surface.blit(back_text, back_rect)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sound_manager.play_sfx("selects")
                return "back_to_menu"

        screen.blit(help_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)