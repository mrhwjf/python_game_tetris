# game.py
from grid import Grid
from tetromino import *
import random
import pygame.draw
from settings import BLOCK_OFFSET_X, BLOCK_OFFSET_Y, TILE_SIZE
from highscore import HighScoreManager
from sound_manager import SoundManager

class Game:
    def __init__(self, sound_manager: SoundManager, screen: pygame.display, user_event: int, mode="single_player"):
        self.grid: Grid = Grid()
        self.blocks: list[Block] = [IBlock, JBlock, LBlock, OBlock, SBlock, TBlock, ZBlock]
        self.current_block: Block = self.get_random_block()
        self.next_block: Block = self.get_random_block()
        self.game_over: bool = False
        self.score: int = 0
        self.sound_manager: SoundManager = sound_manager
        self.high_score_manager: HighScoreManager = HighScoreManager()
        self.mode: str = mode
        self.screen: pygame.display = screen
        self.paused: bool = False  # Trạng thái tạm dừng
        self.new_high_score: bool = False  # Thêm thuộc tính để tránh lỗi
        self.user_event: int = user_event
        self.game_speed: int = 1000 # Milliseconds
        self.lines_cleared: int = 0

    def update_score(self, lines_cleared: int, move_down_points: int):
        if lines_cleared > 0:
            self.score += int(100 * (2 ** (lines_cleared - 1)))
        self.score += move_down_points

    def get_random_block(self) -> Block:
        block_class = random.choice(self.blocks)
        block_instance = block_class()
        return block_instance

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def hard_drop(self):
        points = 0
        while True:
            self.current_block.move(1, 0)
            if not self.block_inside() or not self.block_fits():
                self.current_block.move(-1, 0)
                self.lock_block()
                self.update_score(0, points)
                break
            points += 1
        
        self.sound_manager.play_sfx("hard-landing")


    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id

        self.current_block = self.next_block
        self.next_block = self.get_random_block()

        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.sound_manager.play_sfx("line-clear")
            self.update_score(rows_cleared, 0)
            self.lines_cleared += rows_cleared
            self.adjust_game_speed()

        if not self.block_fits():
            self.game_over = True
            # Cập nhật new_high_score và lưu kết quả (dành cho 1 người chơi)
            if self.mode == "single_player":
                self.new_high_score = self.high_score_manager.qualifies(self.score)

    def reset(self):
        self.grid.reset()
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.new_high_score = False  # Reset lại trạng thái high score mới

    def block_fits(self) -> bool:
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()

    def block_inside(self) -> bool:
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True

    def draw(self, screen: pygame.Surface, offset_x=0):
        self.grid.draw(screen, offset_x)
        self.grid.draw_ghost_block(screen, self.current_block, offset_x)
        self.current_block.draw(screen, BLOCK_OFFSET_X + offset_x, BLOCK_OFFSET_Y)

    def draw_next_block(self, screen: pygame.Surface, rect: pygame.Rect):
        tiles = self.next_block.get_cell_positions()
        min_row = min(tile.row for tile in tiles)
        max_row = max(tile.row for tile in tiles)
        min_col = min(tile.column for tile in tiles)
        max_col = max(tile.column for tile in tiles)
        block_width = (max_col - min_col + 1) * TILE_SIZE
        block_height = (max_row - min_row + 1) * TILE_SIZE
        start_x = rect.x + (rect.width - block_width) // 2
        start_y = rect.y + (rect.height - block_height) // 2
        self.next_block.draw(screen, start_x - min_col * TILE_SIZE, start_y - min_row * TILE_SIZE)

    def toggle_pause(self):
        """Bật/tắt trạng thái tạm dừng."""
        self.paused = not self.paused
        if self.paused:
            self.sound_manager.pause_music()
        elif not self.game_over:
            self.sound_manager.resume_music()
    
    def adjust_game_speed(self):
        """Dynamically adjust speed as lines are cleared."""
        new_speed = max(100, 1000 - (self.lines_cleared // 5) * 50)
        if new_speed != self.game_speed:
            self.game_speed = new_speed
            pygame.time.set_timer(self.user_event, self.game_speed)

