"""

=============================================================
assets.py
=============================================================
Centralised asset loading for Brickz

All images, fonts, and sounds are declared as module-level
None values and populated by init_assets(), which must be
called after pygame.init() in main.py.

-------------------------------------------------------------
USAGE
-------------------------------------------------------------
Call init_assets() once after pygame.init(), then import
the named assets you need:

    from modules.assets import font, beep_sound

"""

import pygame
from os.path import dirname, abspath, join

BASE_DIR = dirname(abspath(__file__))
ASSETS_DIR = dirname(BASE_DIR)  # points to project root, not modules/

# -------------------------------------------------------------
# module-level declarations
# -------------------------------------------------------------

# images
splash_surf = None
basic_paddle_surf = None
ball_surf = None


# fonts
font = None
font_large = None

# sounds
game_music = None

# -------------------------------------------------------------
# init
# -------------------------------------------------------------

def make_powerup_surf(colour, label):
    surf = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.rect(surf, colour, pygame.Rect(0, 0, 60, 60), border_radius=6)
    pygame.draw.rect(surf, "white", pygame.Rect(0, 0, 60, 60), 2, border_radius=6)
    text = font.render(label, True, "white")
    text_rect = text.get_frect(center=(30, 30))
    surf.blit(text, text_rect)
    return surf

def init_assets():
    global splash_surf
    global basic_paddle_surf, ball_surf
    global font, font_large
    global game_music

    # fonts
    font = pygame.font.Font(join(ASSETS_DIR, "PressStart2P-Regular.ttf"), 20)
    font_large = pygame.font.Font(join(ASSETS_DIR, "PressStart2P-Regular.ttf"), 60)

    # images
    splash_surf = pygame.image.load(join(ASSETS_DIR, "images", "splash.png")).convert()
    basic_paddle_surf = pygame.image.load(join(ASSETS_DIR, "images", "paddle.png")).convert_alpha()
    ball_surf = pygame.image.load(join(ASSETS_DIR, "images", "ball.png")).convert_alpha()

    # sounds
    game_music = pygame.mixer.Sound(join(ASSETS_DIR, "audio", "midnight_drive.ogg"))
    game_music.set_volume(0.2)
    game_music.play(loops=-1)