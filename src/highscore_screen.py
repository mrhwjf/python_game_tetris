import pygame
import sys
from settings import FONT_DIR_PATH
from assets_utils import COLORS
from highscore import HighScoreManager

def show_high_scores(screen):
    pygame.display.set_caption("Tetris - High Scores")
    title_font = pygame.font.Font(FONT_DIR_PATH, 24)
    text_font = pygame.font.Font(FONT_DIR_PATH, 16)
    bg = COLORS["black"]
    fg = COLORS["white"]
    hl = COLORS["yellow"]

    w, h = screen.get_size()
    manager = HighScoreManager()

    title = title_font.render("High Scores", True, hl)
    single_title = text_font.render("Single Player Top 10:", True, fg)
    back_text = text_font.render("Press ESC to return to Menu", True, fg)

    title_rect = title.get_rect(center=(w//2, 80))
    single_rect = single_title.get_rect(topleft=(w//4, 140))
    back_rect = back_text.get_rect(center=(w//2, h - 40))

    # Lấy top 10
    scores = manager.get_high_scores()
    score_texts = [
        text_font.render(f"{i+1}. {e['name']}: {e['score']}", True, fg)
        for i, e in enumerate(scores)
    ]

    clock = pygame.time.Clock()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                return "back_to_menu"

        screen.fill(bg)
        screen.blit(title, title_rect)
        screen.blit(single_title, single_rect)
        for i, txt in enumerate(score_texts):
            screen.blit(txt, (w//4, 180 + i * 28))
        screen.blit(back_text, back_rect)
        pygame.display.flip()
        clock.tick(60)
