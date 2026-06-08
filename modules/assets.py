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
crack = None
threedee = None
tnt_surf = None
metal_surf = None

# levels
test_level = None

# fonts
font = None
font_large = None

# sounds
game_music = None
bounce_sound = None
break_sound = None
crack_sound = None
explode_sound = None
ting_sound = None

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
    global basic_paddle_surf, ball_surf, crack, threedee, tnt_surf, metal_surf
    global test_level
    global font, font_large
    global game_music
    global bounce_sound, break_sound, crack_sound, explode_sound, ting_sound

    # fonts
    font = pygame.font.Font(join(ASSETS_DIR, "PressStart2P-Regular.ttf"), 20)
    font_large = pygame.font.Font(join(ASSETS_DIR, "PressStart2P-Regular.ttf"), 60)

    # images
    splash_surf = pygame.image.load(join(ASSETS_DIR, "images", "splash.png")).convert()
    basic_paddle_surf = pygame.transform.scale_by(pygame.image.load(join(ASSETS_DIR, "images", "paddle.png")).convert_alpha(), 1.5)
    ball_surf = pygame.transform.scale_by(pygame.image.load(join(ASSETS_DIR, "images", "ball.png")).convert_alpha(), 1.5)
    crack = pygame.image.load(join(ASSETS_DIR, "images", "cracked_brick.png")).convert_alpha()
    threedee = pygame.image.load(join(ASSETS_DIR, "images", "3d_brick.png")).convert_alpha()
    tnt_surf = pygame.image.load(join(ASSETS_DIR, "images", "tnt_brick.png")).convert()
    metal_surf = pygame.image.load(join(ASSETS_DIR, "images", "metal_brick.png")).convert()

    # levels
    test_level = pygame.image.load(join(ASSETS_DIR, "images", "levels", "test.png")).convert_alpha()

    # sounds
    bounce_sound = pygame.mixer.Sound(join(ASSETS_DIR, "audio", "bounce.ogg"))
    bounce_sound.set_volume(0.3)

    break_sound = pygame.mixer.Sound(join(ASSETS_DIR, "audio", "break.ogg"))
    break_sound.set_volume(0.3)

    crack_sound = pygame.mixer.Sound(join(ASSETS_DIR, "audio", "crack.ogg"))
    crack_sound.set_volume(0.3)

    explode_sound = pygame.mixer.Sound(join(ASSETS_DIR, "audio", "explode.wav"))
    explode_sound.set_volume(0.3)

    ting_sound = pygame.mixer.Sound(join(ASSETS_DIR, "audio", "ting.ogg"))
    ting_sound.set_volume(0.3)

    # music

    game_music = pygame.mixer.Sound(join(ASSETS_DIR, "audio", "midnight_drive.ogg"))
    game_music.set_volume(0.2)