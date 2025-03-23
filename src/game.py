from grid import Grid
from tetromino import *
import random
import pygame.mixer, pygame.draw
from settings import BLOCK_OFFSET_X, BLOCK_OFFSET_Y
from assets_utils import SFX, MUSIC, play_music

class Game:
	def __init__(self):
		self.grid: Grid = Grid()
		self.blocks: list[Block] = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block: Block = self.get_random_block()
		self.next_block: Block = self.get_random_block()
		self.game_over: bool = False
		self.score: int = 0
		self.clear_sound: pygame.mixer.Sound = SFX.get("line-clear")
		play_music(MUSIC.get("game"))

	def update_score(self, lines_cleared: int, move_down_points: int):
		if lines_cleared > 0:
			self.score += int(100 * (2 ** (lines_cleared - 1)))
		self.score += move_down_points

	def get_random_block(self) -> Block:
		if len(self.blocks) == 0:
			self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		block = random.choice(self.blocks)
		self.blocks.remove(block)
		return block

	def move_left(self):
		self.current_block.move(0, -1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, 1)

	def move_right(self):
		self.current_block.move(0, 1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, -1)

	def move_down(self):
		self.current_block.move(1, 0)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(-1, 0)
			self.lock_block()

	def lock_block(self):
		tiles = self.current_block.get_cell_positions()
		for position in tiles:
			self.grid.grid[position.row][position.column] = self.current_block.id
		self.current_block = self.next_block
		self.next_block = self.get_random_block()
		rows_cleared = self.grid.clear_full_rows()
		if rows_cleared > 0:
			self.clear_sound.play()
			self.update_score(rows_cleared, 0)
		if self.block_fits() == False:
			self.game_over = True

	def reset(self):
		self.grid.reset()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.score = 0

	def block_fits(self) -> bool:
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_empty(tile.row, tile.column) == False:
				return False
		return True

	def rotate(self):
		self.current_block.rotate()
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.undo_rotation()

	def block_inside(self) -> bool:
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_inside(tile.row, tile.column) == False:
				return False
		return True

	def draw(self, screen: pygame.Surface):
		self.grid.draw(screen)
		self.current_block.draw(screen, BLOCK_OFFSET_X, BLOCK_OFFSET_Y)
		
		if self.next_block.id == 3:
			self.next_block.draw(screen, 350, 300)
		elif self.next_block.id == 4:
			self.next_block.draw(screen, 350, 280)
		else:
			self.next_block.draw(screen, 360, 280)