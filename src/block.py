import pygame.draw
from position import Position
from settings import TILE_SIZE
from assets_utils import BLOCK_TEXTURE, shrink_image

class Block:
	def __init__(self, id: int):
		self.id: int = id
		self.cells: dict[int, list[Position]] = {}
		self.row_offset: int = 0
		self.column_offset: int = 0
		self.rotation_state: int = 0
		self.texture = BLOCK_TEXTURE.get(id)

	def move(self, rows: int, columns: int):
		self.row_offset += rows
		self.column_offset += columns

	def get_cell_positions(self) -> list[Position]:
		tiles = self.cells[self.rotation_state]
		moved_tiles: list[Position] = []
		for position in tiles:
			position = Position(position.row + self.row_offset, position.column + self.column_offset)
			moved_tiles.append(position)
		return moved_tiles

	def rotate(self):
		self.rotation_state += 1
		if self.rotation_state == len(self.cells):
			self.rotation_state = 0

	def undo_rotation(self):
		self.rotation_state -= 1
		if self.rotation_state == -1:
			self.rotation_state = len(self.cells) - 1

	def draw(self, screen: pygame.Surface, offset_x: int, offset_y: int):
		tiles = self.get_cell_positions()
		for tile in tiles:
			tile_rect = pygame.Rect(offset_x + tile.column * TILE_SIZE, 
				offset_y + tile.row * TILE_SIZE, TILE_SIZE -1, TILE_SIZE -1)
			screen.blit(self.texture, tile_rect)
