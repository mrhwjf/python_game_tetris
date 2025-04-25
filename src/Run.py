import pygame
import sys
from util.settings import FRAME_RES
from util.cursor_manager import CursorManager
from control.App import App
from control.main import start_single_player
from control.main2 import start_two_player
from gui.help_screen import show_help
from gui.settings_screen import show_settings
from gui.highscore_screen import show_high_scores
from util.sound_manager import SoundManager
from util.assets_utils import load_block_textures, draw_loading_bar

class Run:
    def __init__(self):
        self.default_res = FRAME_RES
        self.screen = pygame.display.set_mode(self.default_res, pygame.NOFRAME)
        pygame.display.set_caption("Tetris Menu")
        
        self.sound_manager = SoundManager()
        self.sound_manager.play_music("start-up", loop=False)
        
        load_block_textures()
        draw_loading_bar(self.screen, duration=1000)

        self.app = App(self.default_res[0], self.default_res[1])
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"

        self.cursor_manager = CursorManager()
        self.cursor_manager.set_cursor("arrow")

        self.sound_manager.play_music("menu")
    
    def run(self):
        while self.running:
            if self.state == "menu":
                self.run_menu()
            elif self.state == "single_player":
                self.run_single_player()
            elif self.state == "two_players":
                self.run_two_player()
            elif self.state == "help":
                self.run_help()
            elif self.state == "settings":
                self.run_settings()
            elif self.state == "high_scores":
                self.run_high_scores()
        
        pygame.quit()
        sys.exit()
    
    def run_menu(self):
        pygame.display.set_caption("Tetris - Menu")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            action = self.app.handle_event(event, self.cursor_manager, self.sound_manager)
            if action:
                self.handle_action(action)
                self.sound_manager.play_sfx("select")
        
        self.app.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)
    
    def run_single_player(self):
        result = start_single_player(self.screen, self.sound_manager, self.cursor_manager)
        if result == "back_to_menu":
            self.state = "menu"
            self.sound_manager.play_music("menu")
    
    def run_two_player(self):
        result = start_two_player(self.screen, self.sound_manager, self.cursor_manager)
        if result == "back_to_menu":
            print("Back to menu from two players")
            self.state = "menu"
            self.sound_manager.play_music("menu")
            # self.screen = set_window_mode("single_player")
    
    def run_help(self):
        result = show_help(self.screen, self.sound_manager)
        if result == "back_to_menu":
            self.state = "menu"
    
    def run_settings(self):
        result = show_settings(self.screen, self.sound_manager, self.cursor_manager)
        if result == "back_to_menu":    
            self.state = "menu"
    
    def run_high_scores(self):
        result = show_high_scores(self.screen)
        if result == "back_to_menu":
            self.state = "menu"
    
    def handle_action(self, action):
        print(f"Selected action: {action}")
        
        if action == "play":
            print("Starting single player game...")
            self.state = "single_player"
            
        elif action == "2players":
            print("Starting two players game...")
            self.state = "two_players"
            
        elif action == "settings":
            print("Opening settings...")
            self.state = "settings"
            
        elif action == "help":
            print("Showing help...")
            self.state = "help"
            
        elif action == "high_scores":
            print("Showing high scores...")
            self.state = "high_scores"
            
        elif action == "quit":
            self.running = False
            print("Sayonara!~~~")

def main():
    pygame.init()
    game = Run()    
    game.run()

if __name__ == "__main__":
    main()