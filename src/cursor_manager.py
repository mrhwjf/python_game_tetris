import pygame

class CursorManager:
    CURSOR_MAP = {
        "arrow": pygame.SYSTEM_CURSOR_ARROW,
        "hand": pygame.SYSTEM_CURSOR_HAND,
        "wait": pygame.SYSTEM_CURSOR_WAIT,
        "crosshair": pygame.SYSTEM_CURSOR_CROSSHAIR,
        "ibeam": pygame.SYSTEM_CURSOR_IBEAM,
        "sizeall": pygame.SYSTEM_CURSOR_SIZEALL,
    }

    def __init__(self):
        self.current_cursor = None

    def set_cursor(self, name: str):
        name = name.lower()
        if name in self.CURSOR_MAP:
            cursor_type = self.CURSOR_MAP[name]
            if cursor_type != self.current_cursor:
                pygame.mouse.set_cursor(cursor_type)
                self.current_cursor = cursor_type
