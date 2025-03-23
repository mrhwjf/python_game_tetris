from settings import *
from assets_utils import shrink_image
import pygame

pygame.init()

screen = pygame.display.set_mode((600,800))
pygame.display.set_caption("TEST")


board = pygame.image.load("assets/Grid.png")
border = pygame.image.load("assets/Border.png")
block = shrink_image("assets/block/Tetromino_block1_2.png", (TILE_SIZE,TILE_SIZE))
grid = pygame.Rect(50,100,300,600)

clock = pygame.time.Clock()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	#Drawing
	screen.blit(board, (0,0))
	screen.blit(block, BLOCK_OFFSET)
	screen.blit(border, (0,0))
	pygame.draw.rect(screen, (255, 0, 0), grid, 3)

	pygame.display.update()
	clock.tick(60)