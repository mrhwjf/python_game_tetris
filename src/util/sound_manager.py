import pygame
from util.assets_utils import MUSIC, SFX_DIR_PATH

class SoundManager:
    def __init__(self):
        # trạng thái chung
        self.music_enabled = True
        self.sfx_enabled = True
        self.current_music = None

        pygame.mixer.init()
        print("SoundManager initialized. Music:", self.music_enabled, "SFX:", self.sfx_enabled)

        # Tải SFX
        self.sfx = {}
        for name, path in SFX_DIR_PATH.items():
            try:
                self.sfx[name] = pygame.mixer.Sound(path)
                print(f"Loaded SFX: {name} from {path}")
            except pygame.error as e:
                print(f"Error loading SFX {name} from {path}: {e}")

    def play_music(self, track: str, loop: bool = True):
        if not self.music_enabled:
            print(f"Music disabled, cannot play: {track}")
            return
        if track in MUSIC:
            try:
                if self.current_music != track:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(MUSIC[track])
                    pygame.mixer.music.play(-1 if loop else 0)
                    pygame.mixer.music.set_volume(1.0)
                    self.current_music = track
                    print(f"Playing music: {track}, loop={loop}")
            except pygame.error as e:
                print(f"Error playing music {track}: {e}")

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None
        print("Music stopped")

    def pause_music(self):
        pygame.mixer.music.pause()
        print("Music paused")

    def resume_music(self):
        if not self.music_enabled:
            print(f"Current music: ${self.current_music}. Music is disabled")
            return
        pygame.mixer.music.unpause()
        print("Music resumed")

    def play_sfx(self, sfx_name: str):
        if not self.sfx_enabled:
            print(f"SFX disabled, cannot play: {sfx_name}")
            return
        if sfx_name in self.sfx:
            try:
                self.sfx[sfx_name].play()
                print(f"Playing SFX: {sfx_name}")
            except pygame.error as e:
                print(f"Error playing SFX {sfx_name}: {e}")

    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        print("Music toggled to:", self.music_enabled)
        if not self.music_enabled and self.current_music:
            pygame.mixer.music.stop()
        elif self.music_enabled and self.current_music:
            pygame.mixer.music.play()

    def toggle_sfx(self):
        self.sfx_enabled = not self.sfx_enabled
        print("SFX toggled to:", self.sfx_enabled)
