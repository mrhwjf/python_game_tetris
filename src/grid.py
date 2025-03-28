import pygame.draw
from settings import TILE_SIZE, BLOCK_OFFSET_X, BLOCK_OFFSET_Y
from assets_utils import BLOCK_TEXTURE, shrink_image

class Grid:
	def __init__(self):
		self.num_rows: int = 20
		self.num_cols: int = 10
		self.cell_size: int = TILE_SIZE
		self.grid: list[list[int]] = [[0] * self.num_cols for _ in range(self.num_rows)]
		self.texture: dict[int, str] = BLOCK_TEXTURE

	def is_inside(self, row: int, column: int) -> bool:
		if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
			return True
		return False

	def is_empty(self, row: int, column: int) -> bool:
		if self.grid[row][column] == 0:
			return True
		return False

	def is_row_full(self, row: int) -> bool:
		for column in range(self.num_cols):
			if self.grid[row][column] == 0:
				return False
		return True

	def clear_row(self, row: int):
		for column in range(self.num_cols):
			self.grid[row][column] = 0

	def move_row_down(self, row: int, num_rows: int):
		for column in range(self.num_cols):
			self.grid[row + num_rows][column] = self.grid[row][column]
			self.grid[row][column] = 0

	def clear_full_rows(self) -> int:
		completed: int = 0
		for row in range(self.num_rows - 1, 0, -1):
			if self.is_row_full(row):
				self.clear_row(row)
				completed += 1
			elif completed > 0:
				self.move_row_down(row, completed)
		return completed
	
	def reset(self):
		self.grid = [[0] * self.num_cols for _ in range(self.num_rows)]

	def draw(self, screen: pygame.Surface):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				cell_value: int = self.grid[row][column]
				cell_rect: pygame.Rect = pygame.Rect(column * self.cell_size + BLOCK_OFFSET_X, row * self.cell_size + BLOCK_OFFSET_Y,
					self.cell_size, self.cell_size)
				if cell_value != 0:
					screen.blit(self.texture.get(cell_value), cell_rect)
