# main2.py
import pygame, sys
from settings import *
from settings_screen import show_settings
from pause_menu import pause_game

def start_two_player(screen, sound_manager, cursor_manager):
    sound_manager.play_music("game")
    pygame.display.set_caption("Tetris - Two Player")

    from game import Game
    from assets_utils import COLORS, GRID_IMG_DIR_PATH, BORDER_IMG_DIR_PATH

    # Fonts & labels
    title_font = pygame.font.Font(FONT_DIR_PATH, 21)
    score1_surface = title_font.render("P1 Score", True, COLORS.get("white"))
    score2_surface = title_font.render("P2 Score", True, COLORS.get("white"))
    next1_surface = title_font.render("P1 Next", True, COLORS.get("white"))
    next2_surface = title_font.render("P2 Next", True, COLORS.get("white"))
    win_surface = title_font.render("WIN", True, COLORS.get("cyan"))
    lose_surface = title_font.render("LOSE", True, COLORS.get("red"))
    draw_surface = title_font.render("DRAW", True, COLORS.get("white"))

    # Load images
    grid_surface = pygame.image.load(GRID_IMG_DIR_PATH)
    border_surface = pygame.image.load(BORDER_IMG_DIR_PATH)

    # Layout
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    grid_width = 400
    middle_width = 180
    padding = 10
    total_width = grid_width + padding + middle_width + padding + grid_width
    start_x = (screen_width - total_width) // 2

    grid1_x = start_x
    middle_x = grid1_x + grid_width + padding
    grid2_x = middle_x + middle_width + padding

    score1_rect = pygame.Rect(middle_x, 50, 180, 60)
    next1_rect = pygame.Rect(middle_x, 150, 180, 180)
    score2_rect = pygame.Rect(middle_x, 400, 180, 60)
    next2_rect = pygame.Rect(middle_x, 500, 180, 180)

    # Overlay - for when a player is game over
    overlay_surface_1 = pygame.Surface((grid_width, screen_height), pygame.SRCALPHA)
    overlay_surface_2 = pygame.Surface((grid_width, screen_height), pygame.SRCALPHA)
    overlay_color = (0, 0, 0, 128) # Semi-transparent black

    overlay_surface_1.fill(overlay_color)
    overlay_surface_2.fill(overlay_color)

    # user event ids and initial difficulty
    GAME_UPDATE_1 = pygame.USEREVENT + 1
    GAME_UPDATE_2 = pygame.USEREVENT + 2
    pygame.time.set_timer(GAME_UPDATE_1, 1000)
    pygame.time.set_timer(GAME_UPDATE_2, 1000)

    clock = pygame.time.Clock()
    player1 = Game(sound_manager, screen, GAME_UPDATE_1, mode="two_players")
    player2 = Game(sound_manager, screen, GAME_UPDATE_2, mode="two_players")
    game_over_music_played = False
    paused = False  # Track pause state

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle key presses for in-game control, pause, and game over
            if event.type == pygame.KEYDOWN:
                # Toggle pause with ESC if neither player is game over
                if event.key == pygame.K_ESCAPE:
                    if player1.game_over and player2.game_over:
                        return "back_to_menu"  # Return to main menu if both players are game over
                    elif not paused:
                        paused = True
                        player1.paused = True
                        player2.paused = True
                        result = pause_game(screen, cursor_manager)
                        if result == "resume":
                            paused = False
                            player1.paused = False
                            player2.paused = False
                        elif result == "settings":
                            res = show_settings(screen, sound_manager)
                            if res == "back_to_menu":
                                paused = False
                                player1.paused = False
                                player2.paused = False
                        elif result == "mainmenu":
                            return "back_to_menu"

                # Restart game if both players are game over and R is pressed
                if player1.game_over and player2.game_over and event.key == pygame.K_r:
                    player1.game_over = False
                    player1.reset()
                    player2.game_over = False
                    player2.reset()
                    paused = False
                    sound_manager.play_music("game")
                    game_over_music_played = False

                # Player 1 controls (if not paused and not game over)
                if not paused and not player1.game_over:
                    if event.key == pygame.K_a:
                        player1.move_left()
                    if event.key == pygame.K_d:
                        player1.move_right()
                    if event.key == pygame.K_s:
                        player1.hard_drop()
                    if event.key == pygame.K_w:
                        player1.rotate()

                # Player 2 controls (if not paused and not game over)
                if not paused and not player2.game_over:
                    if event.key == pygame.K_LEFT:
                        player2.move_left()
                    if event.key == pygame.K_RIGHT:
                        player2.move_right()
                    if event.key == pygame.K_DOWN:
                        player2.hard_drop()
                    if event.key == pygame.K_UP:
                        player2.rotate()

            # Handle automatic drop updates for each player
            if event.type == GAME_UPDATE_1 and not paused and not player1.game_over:
                    player1.move_down()

            if event.type == GAME_UPDATE_2 and not paused and not player2.game_over:
                    player2.move_down()


        # Draw game
        screen.fill(COLORS.get("black"))

        screen.blit(grid_surface, (grid1_x, 0))
        screen.blit(border_surface, (grid1_x, 0))
        player1.draw(screen, offset_x=grid1_x)

        screen.blit(grid_surface, (grid2_x, 0))
        screen.blit(border_surface, (grid2_x, 0))
        player2.draw(screen, offset_x=grid2_x)

        # Draw UI
        score1_value_surface = title_font.render(str(player1.score), True, COLORS.get("black"))
        score2_value_surface = title_font.render(str(player2.score), True, COLORS.get("black"))

        screen.blit(score1_surface, (middle_x, 20))
        screen.blit(next1_surface, (middle_x, 120))
        screen.blit(score2_surface, (middle_x, 370))
        screen.blit(next2_surface, (middle_x, 470))

        pygame.draw.rect(screen, COLORS.get("white"), score1_rect, 0, 10)
        pygame.draw.rect(screen, COLORS.get("cyan"), score1_rect, 3, 10)
        pygame.draw.rect(screen, COLORS.get("white"), next1_rect, 0, 10)
        pygame.draw.rect(screen, COLORS.get("cyan"), next1_rect, 3, 10)
        pygame.draw.rect(screen, COLORS.get("white"), score2_rect, 0, 10)
        pygame.draw.rect(screen, COLORS.get("cyan"), score2_rect, 3, 10)
        pygame.draw.rect(screen, COLORS.get("white"), next2_rect, 0, 10)
        pygame.draw.rect(screen, COLORS.get("cyan"), next2_rect, 3, 10)

        screen.blit(score1_value_surface, score1_value_surface.get_rect(centerx=score1_rect.centerx, centery=score1_rect.centery))
        screen.blit(score2_value_surface, score2_value_surface.get_rect(centerx=score2_rect.centerx, centery=score2_rect.centery))

        player1.draw_next_block(screen, next1_rect)
        player2.draw_next_block(screen, next2_rect)

        # Game over logic
        if player1.game_over and player2.game_over:
            if not game_over_music_played:
                sound_manager.stop_music()
                sound_manager.play_music("after-game")
                game_over_music_played = True
            
            # Flickering effect for Game Over and Restart prompt
            elapsed_time = pygame.time.get_ticks() // 1000
            if elapsed_time % 2 == 0:  # Every second, toggle visibility
                go_surf = title_font.render("Game Over", True, COLORS.get("red"))
                go_rect = go_surf.get_rect(topleft=(grid1_x + 400, 380))
                pygame.draw.rect(screen,
                                COLORS.get("black"),
                                go_rect.inflate(20, 10),
                                border_radius=5)
                pygame.draw.rect(screen,
                                COLORS.get("white"),
                                go_rect.inflate(20, 10),
                                width=2,
                                border_radius=5)
                screen.blit(go_surf, go_rect.topleft)
                
                restart_surf = title_font.render("Press R to Restart", True, COLORS.get("white"))
                restart_rect = restart_surf.get_rect(center=(grid1_x + 500, 480))
                pygame.draw.rect(screen,
                                COLORS.get("black"),
                                restart_rect.inflate(20, 10),
                                border_radius=5)
                pygame.draw.rect(screen,
                                COLORS.get("white"),
                                restart_rect.inflate(20, 10),
                                width=2,
                                border_radius=5)
                screen.blit(restart_surf, restart_rect.topleft)


            # Draw win/lose surfaces with black background and white border
            if player1.score > player2.score:
                # Player 1 wins
                win_rect = win_surface.get_rect(topleft=(grid1_x + 155, 450))
                pygame.draw.rect(screen, COLORS.get("black"), win_rect.inflate(20, 10), border_radius=5)
                pygame.draw.rect(screen, COLORS.get("white"), win_rect.inflate(20, 10), width=2, border_radius=5)
                screen.blit(win_surface, win_rect.topleft)
                
                # Player 2 loses
                lose_rect = lose_surface.get_rect(topleft=(grid2_x + 155, 450))
                pygame.draw.rect(screen, COLORS.get("black"), lose_rect.inflate(20, 10), border_radius=5)
                pygame.draw.rect(screen, COLORS.get("white"), lose_rect.inflate(20, 10), width=2, border_radius=5)
                screen.blit(lose_surface, lose_rect.topleft)
            
            elif player2.score > player1.score:
                # Player 1 loses
                lose_rect = lose_surface.get_rect(topleft=(grid1_x + 155, 450))
                pygame.draw.rect(screen, COLORS.get("black"), lose_rect.inflate(20, 10), border_radius=5)
                pygame.draw.rect(screen, COLORS.get("white"), lose_rect.inflate(20, 10), width=2, border_radius=5)
                screen.blit(lose_surface, lose_rect.topleft)
                
                # Player 2 wins
                win_rect = win_surface.get_rect(topleft=(grid2_x + 155, 450))
                pygame.draw.rect(screen, COLORS.get("black"), win_rect.inflate(20, 10), border_radius=5)
                pygame.draw.rect(screen, COLORS.get("white"), win_rect.inflate(20, 10), width=2, border_radius=5)
                screen.blit(win_surface, win_rect.topleft)
            
            else:
                # Both lose (tie)
                draw_rect1 = draw_surface.get_rect(topleft=(grid1_x + 155, 450))
                pygame.draw.rect(screen, COLORS.get("black"), draw_rect1.inflate(20, 10), border_radius=5)
                pygame.draw.rect(screen, COLORS.get("white"), draw_rect1.inflate(20, 10), width=2, border_radius=5)
                screen.blit(draw_surface, draw_rect1.topleft)
                
                draw_rect2 = draw_surface.get_rect(topleft=(grid2_x + 155, 450))
                pygame.draw.rect(screen, COLORS.get("black"), draw_rect2.inflate(20, 10), border_radius=5)
                pygame.draw.rect(screen, COLORS.get("white"), draw_rect2.inflate(20, 10), width=2, border_radius=5)
                screen.blit(draw_surface, draw_rect2.topleft)

        if player1.game_over and not player2.game_over:
            go1_surf = title_font.render("Game Over", True, COLORS.get("red"))
            go1_rect = go1_surf.get_rect(center=(grid1_x + 200, 300))
            pygame.draw.rect(screen, COLORS.get("black"), go1_rect.inflate(20, 10), border_radius=5)
            pygame.draw.rect(screen, COLORS.get("white"), go1_rect.inflate(20, 10), width=2, border_radius=5)
            screen.blit(overlay_surface_1, (grid1_x,0))
            screen.blit(go1_surf, go1_rect)

        if player2.game_over and not player1.game_over:
            go2_surf = title_font.render("Game Over", True, COLORS.get("red"))
            go2_rect = go2_surf.get_rect(center=(grid2_x + 200, 300))
            pygame.draw.rect(screen, COLORS.get("black"), go2_rect.inflate(20, 10), border_radius=5)
            pygame.draw.rect(screen, COLORS.get("white"), go2_rect.inflate(20, 10), width=2, border_radius=5)
            screen.blit(overlay_surface_2, (grid2_x, 0))
            screen.blit(go2_surf, go2_rect)

        pygame.display.flip()
        clock.tick(30)
