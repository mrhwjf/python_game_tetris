import pygame, sys
from pause_menu import pause_game
from settings import FONT_DIR_PATH
from settings_screen import show_settings
from assets_utils import COLORS, GRID_IMG_DIR_PATH, BORDER_IMG_DIR_PATH
from name_input_screen import show_name_input

def start_single_player(screen, sound_manager, cursor_manager):
    sound_manager.play_music("game")
    pygame.display.set_caption("Tetris - Single Player")
    paused = False

    cursor_manager.set_cursor("arrow")

    from game import Game

    # Fonts & labels
    game_font = pygame.font.Font(FONT_DIR_PATH, 23)
    hiscore_font = pygame.font.Font(FONT_DIR_PATH, 20)
    score_surface = game_font.render("Score", True, COLORS.get("white"))
    high_score_surface = hiscore_font.render("HiScore", True, COLORS.get("white"))
    next_surface = game_font.render("Next", True, COLORS.get("white"))
    game_over_surface = game_font.render("GAME OVER", True, COLORS.get("red"))
    restart_surf = hiscore_font.render("Press R to Restart", True, COLORS.get("white"))
    new_high_score_surface = game_font.render("New High Score!", True, COLORS.get("green"))

    # Load images
    grid_surface = pygame.image.load(GRID_IMG_DIR_PATH)
    border_surface = pygame.image.load(BORDER_IMG_DIR_PATH)

    # Layout
    screen_width = screen.get_width() # Now 1000
    screen_height = screen.get_height() # Now 800
    grid_width = 400
    side_width = 180
    padding = 10
    total_width = grid_width + padding + side_width
    start_x = (screen_width - total_width) // 2
    grid_x = start_x
    side_x = grid_x + grid_width + padding

    # Center the entire block vertically (optional, but often looks good)
    total_height = 600 # Approximate total height of the main elements
    start_y = (screen_height - total_height) // 2

    score_rect = pygame.Rect(side_x, start_y + 50, 180, 60)
    high_score_rect = pygame.Rect(side_x, start_y + 370, 180, 60)
    next_rect = pygame.Rect(side_x, start_y + 150, 180, 180)

    score_rect = pygame.Rect(side_x, 50, 180, 60)
    high_score_rect = pygame.Rect(side_x, 370, 180, 60)
    next_rect = pygame.Rect(side_x, 150, 180, 180)

    GAME_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(GAME_UPDATE, 1000)

    clock = pygame.time.Clock()
    player = Game(sound_manager, screen, GAME_UPDATE, mode="single_player")
    game_over_music_played = False
    high_score_updated = False


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Handle ESC key
                if event.key == pygame.K_ESCAPE:
                    if player.game_over:
                        return "back_to_menu"  # Return to main menu on ESC during game over
                    elif not paused:
                        paused = True
                        result = pause_game(screen, cursor_manager)
                        if result == "resume":
                            paused = False
                        elif result == "settings":
                            res = show_settings(screen, sound_manager)
                            if res == "back_to_menu":
                                paused = False
                        elif result == "mainmenu":
                            return "back_to_menu"
                    continue

                # Restart on space if game over
                if player.game_over and event.key == pygame.K_r:
                    player.reset()
                    paused = False
                    sound_manager.play_music("game")
                    game_over_music_played = False
                    high_score_updated = False

                # In-game controls if not paused
                if not player.game_over and not paused:
                    if event.key == pygame.K_LEFT:
                        player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        player.move_right()
                    elif event.key == pygame.K_DOWN:
                        player.hard_drop()
                    elif event.key == pygame.K_UP:
                        player.rotate()
                    elif event.key == pygame.K_SPACE:
                        player.rotate()

            # Automatic drop
            if event.type == GAME_UPDATE and not paused and not player.game_over:
                player.move_down()

        # Draw game
        screen.fill(COLORS.get("black"))
        screen.blit(grid_surface, (grid_x, 0))
        screen.blit(border_surface, (grid_x, 0))
        player.draw(screen, offset_x=grid_x)

        # Side panel UI
        high_scores = player.high_score_manager.get_high_scores()
        hs_val = str(high_scores[0]["score"] if high_scores else 0)
        score_val_surf = game_font.render(str(player.score), True, COLORS.get("black"))
        hs_val_surf = game_font.render(hs_val, True, COLORS.get("black"))
        screen.blit(score_surface, (side_x + 20, 20))
        screen.blit(high_score_surface, (side_x + 20, 340))
        screen.blit(next_surface, (side_x + 20, 120))
        pygame.draw.rect(screen, COLORS.get("white"), score_rect, 0, 10)
        pygame.draw.rect(screen, COLORS.get("cyan"), score_rect, 3, 10)
        pygame.draw.rect(screen, COLORS.get("white"), high_score_rect, 0, 10)
        pygame.draw.rect(screen, COLORS.get("cyan"), high_score_rect, 3, 10)
        pygame.draw.rect(screen, COLORS.get("white"), next_rect, 0, 10)
        pygame.draw.rect(screen, COLORS.get("cyan"), next_rect, 3, 10)
        screen.blit(score_val_surf, score_val_surf.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))
        screen.blit(hs_val_surf, hs_val_surf.get_rect(centerx=high_score_rect.centerx, centery=high_score_rect.centery))
        player.draw_next_block(screen, next_rect)

        # Handle game over GUI
        if player.game_over:
            if not game_over_music_played:
                sound_manager.stop_music()
                sound_manager.play_music("after-game")
                game_over_music_played = True

            # Prepare surfaces
            go_surf = game_over_surface
            nhs_surf = new_high_score_surface if getattr(player, "new_high_score", False) else None
            restart_surf = restart_surf

            # Create a list of texts to draw
            texts_to_draw = [go_surf]
            if nhs_surf:
                texts_to_draw.append(nhs_surf)
            texts_to_draw.append(restart_surf)

            # Set starting y position
            center_x = grid_x + 200
            # Approximate total height of the game over texts
            total_height_go = sum([surf.get_height() for surf in texts_to_draw]) + 20 * (len(texts_to_draw) - 1)
            start_y_go = (screen_height - total_height_go) // 2 # Center vertically

            current_y = start_y_go

            # Draw each with spacing and background
            for surf in texts_to_draw:
                rect = surf.get_rect(center=(center_x, current_y + surf.get_height() // 2))
                pygame.draw.rect(screen, COLORS.get("black"), rect.inflate(20, 10), border_radius=5)
                pygame.draw.rect(screen, COLORS.get("white"), rect.inflate(20, 10), width=2, border_radius=5)
                screen.blit(surf, rect.topleft)
                current_y = rect.bottom + 20

            # Handle new high score input after drawing
            if getattr(player, "new_high_score", False) and not high_score_updated:
                name = show_name_input(screen, player.score)
                player.high_score_manager.update_high_score(
                    player.score,
                    name=name
                )
                high_score_updated = True


        pygame.display.flip()
        clock.tick(30)