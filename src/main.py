import pygame, sys

pygame.init()
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Tetris")

from game import Game
from settings import *
from assets_utils import COLORS, GRID_IMG_DIR_PATH, BORDER_IMG_DIR_PATH, draw_tiled_background, create_tiled_background

screen.fill(COLORS.get("black"))
title_font = pygame.font.Font(FONT_DIR_PATH, 25)
score_surface = title_font.render("Score", True, COLORS.get("white"))
next_surface = title_font.render("Next", True, COLORS.get("white"))
game_over_surface = title_font.render("GAME OVER", True, COLORS.get("white"))

# tile_surface = create_tiled_background(screen, pygame.image.load(TILING_DIR_PATH))
grid_surface = pygame.image.load(GRID_IMG_DIR_PATH)
border_surface = pygame.image.load(BORDER_IMG_DIR_PATH)

score_rect = pygame.Rect(410, 50, 180, 60)
next_rect = pygame.Rect(410, 220, 180, 180)

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)
screen.blit(grid_surface, (0,0))
screen.blit(border_surface, (0,0))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if game.game_over == True:
				game.game_over = False
				game.reset()
			if event.key == pygame.K_LEFT and game.game_over == False:
				game.move_left()
			if event.key == pygame.K_RIGHT and game.game_over == False:
				game.move_right()
			if event.key == pygame.K_DOWN and game.game_over == False:
				game.move_down()
				game.update_score(0, 1)
			if event.key == pygame.K_UP and game.game_over == False:
				game.rotate()
		if event.type == GAME_UPDATE and game.game_over == False:
			game.move_down()

		# Clear the screen
		screen.fill(COLORS.get("black"))

		# Draw static elements
		# draw_tiled_background(screen, tile_surface)
		screen.blit(grid_surface, (0, 0))
		screen.blit(border_surface, (0, 0))

		# Draw dynamic elements
		score_value_surface = title_font.render(str(game.score), True, COLORS.get("black"))
		screen.blit(score_surface, (430, 20, 50, 50))
		screen.blit(next_surface, (440, 180, 50, 50))

		if game.game_over:
			screen.blit(game_over_surface, (320, 450, 50, 50))


		pygame.draw.rect(screen, COLORS.get("white"), score_rect, 0, 10)  
		pygame.draw.rect(screen, COLORS.get("green"), score_rect, 3, 10)  
		pygame.draw.rect(screen, COLORS.get("white"), next_rect, 0, 10)  
		pygame.draw.rect(screen, COLORS.get("green"), next_rect, 3, 10)  

		screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))

		game.draw(screen)
		pygame.display.flip()
		clock.tick(30)