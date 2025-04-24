import pygame
import sys
from settings import FONT_DIR_PATH
from assets_utils import COLORS

def show_name_input(screen, score) -> str:
    pygame.display.set_caption("Tetris - Enter Your Name")
    title_font = pygame.font.Font(FONT_DIR_PATH, 24)
    text_font = pygame.font.Font(FONT_DIR_PATH, 16)
    background_color = COLORS.get("black")
    text_color = COLORS.get("white")
    highlight_color = COLORS.get("green")

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    title_text = title_font.render("New High Score!", True, highlight_color)
    prompt_text = text_font.render(f"Score: {score}. Enter your name:", True, text_color)
    instruction_text = text_font.render("Press ENTER to submit", True, text_color)

    title_rect = title_text.get_rect(center=(screen_width // 2, 100))
    prompt_rect = prompt_text.get_rect(center=(screen_width // 2, 200))
    name_rect = pygame.Rect(screen_width // 2 - 100, 250, 200, 40)
    instruction_rect = instruction_text.get_rect(center=(screen_width // 2, 350))

    name = ""
    max_name_length = 10
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return "Player"  # Tên mặc định nếu thoát
                elif len(name) < max_name_length and event.unicode.isprintable():
                    name += event.unicode

        screen.fill(background_color)
        screen.blit(title_text, title_rect)
        screen.blit(prompt_text, prompt_rect)
        screen.blit(instruction_text, instruction_rect)

        name_surface = text_font.render(name, True, text_color)
        pygame.draw.rect(screen, text_color, name_rect, 2)
        screen.blit(name_surface, (name_rect.x + 5, name_rect.y + 5))

        pygame.display.flip()
        clock.tick(60)