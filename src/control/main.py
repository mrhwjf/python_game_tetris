import pygame, sys
from gui.pause_menu import pause_game
from util.settings import FONT_DIR_PATH
from gui.settings_screen import show_settings
from util.assets_utils import COLORS, GRID_IMG_DIR_PATH, BORDER_IMG_DIR_PATH
from gui.name_input_screen import show_name_input

def start_single_player(screen, sound_manager, cursor_manager):
    sound_manager.play_music("game")
    pygame.display.set_caption("Tetris - Single Player")
    paused = False
    
    cursor_manager.set_cursor("arrow")

    from game.game import Game

    # Fonts & labels
    game_font = pygame.font.Font(FONT_DIR_PATH, 23)
    hiscore_font = pygame.font.Font(FONT_DIR_PATH, 20)
    score_surface = game_font.render("Score", True, COLORS.get("white"))
    high_score_surface = hiscore_font.render("HiScore", True, COLORS.get("white"))
    next_surface = game_font.render("Next", True, COLORS.get("white"))
    game_over_surface = game_font.render("GAME OVER", True, COLORS.get("red"))
    restart_surface = hiscore_font.render("Press R to Restart", True, COLORS.get("white"))
    new_high_score_surface = game_font.render("New High Score!", True, COLORS.get("green"))

    # Load images
    grid_surface = pygame.image.load(GRID_IMG_DIR_PATH)
    border_surface = pygame.image.load(BORDER_IMG_DIR_PATH)

    # Layout calculations
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    grid_width = 400
    side_width = 180
    padding = 10
    total_width = grid_width + padding + side_width
    start_x = (screen_width - total_width) // 2
    grid_x = start_x
    side_x = grid_x + grid_width + padding

    # Side panel rects
    score_rect = pygame.Rect(side_x, 50, 180, 60)
    high_score_rect = pygame.Rect(side_x, 370, 180, 60)
    next_rect = pygame.Rect(side_x, 150, 180, 180)

    # Timer event for automatic drop
    GAME_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(GAME_UPDATE, 1000)

    clock = pygame.time.Clock()
    player = Game(sound_manager, screen, GAME_UPDATE, mode="single_player")
    game_over_music_played = False
    high_score_updated = False

    # Flicker settings for Game Over & Restart texts
    FLICKER_INTERVAL = 500  # milliseconds
    last_flicker_time = pygame.time.get_ticks()
    show_flicker = True

    # Get high score list
    high_scores = player.high_score_manager.get_high_scores()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # ESC: pause or exit
                if event.key == pygame.K_ESCAPE:
                    if player.game_over:
                        return "back_to_menu"
                    elif not paused:
                        paused = True
                        result = pause_game(screen, cursor_manager, sound_manager)
                        if result == "resume":
                            paused = False
                        elif result == "settings":
                            res = show_settings(screen, sound_manager, cursor_manager)
                            if res == "back_to_menu":
                                paused = False
                        elif result == "mainmenu":
                            return "back_to_menu"
                    continue

                # Restart on R
                if player.game_over and event.key == pygame.K_r:
                    player.reset()
                    paused = False
                    sound_manager.play_music("game")
                    game_over_music_played = False
                    high_score_updated = False

                # In-game controls
                if not player.game_over and not paused:
                    if event.key == pygame.K_LEFT:
                        player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        player.move_right()
                    elif event.key == pygame.K_DOWN:
                        player.hard_drop()
                    elif event.key in (pygame.K_UP, pygame.K_SPACE):
                        player.rotate()

            # Automatic drop
            if event.type == GAME_UPDATE and not paused and not player.game_over:
                player.move_down()

        # Update flicker flag if game over
        if player.game_over:
            now = pygame.time.get_ticks()
            if now - last_flicker_time > FLICKER_INTERVAL:
                show_flicker = not show_flicker
                last_flicker_time = now

        # Draw game field
        screen.fill(COLORS.get("black"))
        screen.blit(grid_surface, (grid_x, 0))
        screen.blit(border_surface, (grid_x, 0))
        player.draw(screen, offset_x=grid_x)

        # Side panel UI
        target_score = player.high_score_manager.get_next_target_score(player.score, high_scores)
        hs_val = str(target_score) # Get point of the next top x player
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

        # Handle Game Over UI with flicker
        if player.game_over:
            if not game_over_music_played:
                sound_manager.stop_music()
                sound_manager.play_music("after-game")
                game_over_music_played = True

            # Only draw texts when show_flicker is True
            if show_flicker:
                center_x = grid_x + grid_width // 2
                texts = [game_over_surface]
                if getattr(player, "new_high_score", False):
                    texts.append(new_high_score_surface)
                texts.append(restart_surface)

                # Calculate vertical centering
                total_h = sum(s.get_height() for s in texts) + 20 * (len(texts) - 1)
                start_y = (screen_height - total_h) // 2
                y = start_y

                for surf in texts:
                    rect = surf.get_rect(center=(center_x, y + surf.get_height() // 2))
                    pygame.draw.rect(screen, COLORS.get("black"), rect.inflate(20, 10), border_radius=5)
                    pygame.draw.rect(screen, COLORS.get("white"), rect.inflate(20, 10), width=2, border_radius=5)
                    screen.blit(surf, rect.topleft)
                    y = rect.bottom + 20

            # Name input for new high score
            if getattr(player, "new_high_score", False) and not high_score_updated:
                rank = player.high_score_manager.get_player_rank(player.score)
                name = show_name_input(screen, player.score, rank)
                player.high_score_manager.update_high_score(player.score, name=name)
                high_score_updated = True

        pygame.display.flip()
        clock.tick(30)