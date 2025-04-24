# App.py
import pygame
from cursor_manager import CursorManager
from settings import FONT_DIR_PATH
from sound_manager import SoundManager

class App:
    """Lớp quản lý giao diện menu chính."""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    HIGHLIGHT_COLOR = (255, 255, 0)

    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.init_fonts()
        self.title_image = pygame.image.load("assets/Title_No_BG.png").convert_alpha()
        self.title_image = pygame.transform.scale(self.title_image, (600, 100))
        self.buttons = [
            {"text": "PLAY", "rect": pygame.Rect(0, 0, 300, 70), "action": "play"},
            {"text": "2 PLAYERS", "rect": pygame.Rect(0, 0, 300, 70), "action": "2players"},
            {"text": "HIGH SCORES", "rect": pygame.Rect(0, 0, 300, 70), "action": "high_scores"},
            {"text": "SETTINGS", "rect": pygame.Rect(0, 0, 300, 70), "action": "settings"},
            {"text": "HELP", "rect": pygame.Rect(0, 0, 300, 70), "action": "help"},
            {"text": "QUIT", "rect": pygame.Rect(0, 0, 300, 70), "action": "quit"}
        ]
        self.selected_index = 0
        self.setup_buttons()

    def init_fonts(self):
        """Khởi tạo các font chữ."""
        self.font_large = pygame.font.Font(FONT_DIR_PATH, 35)
        self.font_medium = pygame.font.Font(FONT_DIR_PATH, 30)
        self.font_small = pygame.font.Font(FONT_DIR_PATH, 20)

    def setup_buttons(self):
        """Thiết lập vị trí các nút."""
        self.title_y = self.HEIGHT // 8
        start_y = self.title_y + 120
        for i, button in enumerate(self.buttons):
            button["rect"].x = (self.WIDTH - button["rect"].width) // 2
            button["rect"].y = start_y + i * 80

    def draw(self, screen):
        """Vẽ menu lên màn hình."""
        screen.fill(self.BLACK)
        title_rect = self.title_image.get_rect(center=(self.WIDTH // 2, self.title_y))
        screen.blit(self.title_image, title_rect)

        for i, button in enumerate(self.buttons):
            if i == self.selected_index:
                text = self.font_medium.render(button["text"], True, self.HIGHLIGHT_COLOR)
                rect = button["rect"].copy()
                rect.inflate_ip(10, 10)
            else:
                text = self.font_small.render(button["text"], True, self.WHITE)
                rect = button["rect"]

            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)


    def handle_event(self, event: pygame.event, cursor_manager: CursorManager, sound_manager: SoundManager) -> str | None:
        """Xử lý sự kiện cho menu."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                return self.buttons[self.selected_index]["action"]
        elif event.type == pygame.MOUSEMOTION:
            for i, button in enumerate(self.buttons):
                if button["rect"].collidepoint(event.pos):
                    cursor_manager.set_cursor("hand")
                    self.selected_index = i
                    break
                else:
                    cursor_manager.set_cursor("arrow")
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button["rect"].collidepoint(event.pos):
                    return button["action"]
        return None