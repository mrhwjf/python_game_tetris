import pygame
import sys
from util.settings import FONT_DIR_PATH
from util.assets_utils import COLORS

def show_settings(screen, sound_manager, cursor_manager) -> str:
    pygame.display.set_caption("Tetris - Settings")
    title_font = pygame.font.Font(FONT_DIR_PATH, 24)
    text_font  = pygame.font.Font(FONT_DIR_PATH, 16)
    bg = COLORS.get("black")
    fg = COLORS.get("white")
    hl = COLORS.get("yellow")

    w, h = screen.get_size()
    options = ["music", "sfx", "back"]
    selected = 0

    def render_texts():
        title_surf = title_font.render("Settings", True, hl)
        music_surf = text_font.render(f"Music: {'ON' if sound_manager.music_enabled else 'OFF'}", True, hl if selected==0 else fg)
        sfx_surf   = text_font.render(f"SFX: {'ON' if sound_manager.sfx_enabled else 'OFF'}", True, hl if selected==1 else fg)
        back_surf  = text_font.render("Back", True, hl if selected==2 else fg)
        return title_surf, music_surf, sfx_surf, back_surf

    clock = pygame.time.Clock()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif ev.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif ev.key == pygame.K_RETURN:
                    sound_manager.play_sfx("select")
                    if options[selected] == "music":
                        sound_manager.toggle_music()
                    elif options[selected] == "sfx":
                        sound_manager.toggle_sfx()
                    else:
                        return "back_to_menu"
            if ev.type == pygame.MOUSEMOTION:
                mx, my = ev.pos
                rects = [
                    pygame.Rect(w//2-100, 200, 200, 30),
                    pygame.Rect(w//2-100, 260, 200, 30),
                    pygame.Rect(w//2-100, 320, 200, 30),
                ]
                for i, r in enumerate(rects):
                    if r.collidepoint(mx, my):
                        selected = i
                        cursor_manager.set_cursor("hand")
                        break
                    else:
                        cursor_manager.set_cursor("arrow")
                        
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button==1:
                if selected==0:
                    sound_manager.toggle_music()
                elif selected==1:
                    sound_manager.toggle_sfx()
                else:
                    return "back_to_menu"

        title_s, music_s, sfx_s, back_s = render_texts()
        screen.fill(bg)
        screen.blit(title_s, title_s.get_rect(center=(w//2, 140)))
        screen.blit(music_s, music_s.get_rect(center=(w//2, 220)))
        screen.blit(sfx_s,   sfx_s.get_rect(center=(w//2, 300)))
        screen.blit(back_s,  back_s.get_rect(center=(w//2, 380)))
        pygame.display.flip()
        clock.tick(60)
