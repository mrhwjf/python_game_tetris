import sys
import pygame

from cursor_manager import CursorManager
from settings import FONT_DIR_PATH


def pause_game(screen, cursor_manager: CursorManager) -> str:
    """Hiển thị và xử lý menu tạm dừng.
    Trả về:
    - "resume" nếu chọn tiếp tục
    - "settings" nếu chọn cài đặt
    - "mainmenu" nếu chọn về menu chính
    """

    title_font = pygame.font.Font(FONT_DIR_PATH, 50)
    base_font = pygame.font.Font(FONT_DIR_PATH, 20)
    enlarged_font = pygame.font.Font(FONT_DIR_PATH, 30)

    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    screen_rect = screen.get_rect()

    # Title
    title_text = title_font.render("PAUSED", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen_rect.centerx, screen_rect.top + 100))

    # Buttons
    labels = [("Resume", "resume"), ("Settings", "settings"), ("Main Menu", "mainmenu")]
    button_spacing = 40
    total_height = len(labels) * (base_font.get_height() + button_spacing) - button_spacing
    start_y = screen_rect.centery - total_height // 2

    buttons = []
    for i, (text, action) in enumerate(labels):
        pos = (screen_rect.centerx, start_y + i * (base_font.get_height() + button_spacing))
        buttons.append((pos, text, action))

    selected_index = 0
    clock = pygame.time.Clock()

    while True:
        screen.blit(overlay, (0, 0))
        screen.blit(title_text, title_rect)

        for i, (pos, label, _) in enumerate(buttons):
            if i == selected_index:
                font = enlarged_font
                color = (255, 255, 0)
            else:
                font = base_font
                color = (255, 255, 255)
            txt = font.render(label, True, color)
            txt_rect = txt.get_rect(center=pos)
            screen.blit(txt, txt_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(buttons)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    return buttons[selected_index][2]

            elif event.type == pygame.MOUSEMOTION:
                for i, (pos, _, _) in enumerate(buttons):
                    font = enlarged_font if i == selected_index else base_font
                    txt_rect = font.render(labels[i][0], True, (0, 0, 0)).get_rect(center=pos)
                    if txt_rect.collidepoint(event.pos):
                        selected_index = i
                        cursor_manager.set_cursor("hand")
                        break
                else:
                    cursor_manager.set_cursor("arrow")

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos, _, action = buttons[selected_index]
                font = enlarged_font
                txt_rect = font.render(labels[selected_index][0], True, (0, 0, 0)).get_rect(center=pos)
                if txt_rect.collidepoint(event.pos):
                    return action

        clock.tick(30)
