"""

=============================================================
Brickz
=============================================================


-------------------------------------------------------------
STRUCTURE
-------------------------------------------------------------
GameState           Central game state machine. Owns all
                    sprite groups, scores, powerup state,
                    and the state dispatcher that drives
                    each frame.

PlayerPaddle        Player-controlled paddle. Reads keyboard
                    input each frame via get_pressed().

AiPaddle            AI paddle. Tracks ball Y position with
                    variable speed to avoid perfect play.

Ball                The ball. Handles its own movement,
                    wall bounces, shield bounces, and
                    scoring boundary detection.

ScoreTracker        Lightweight class that blits the current
                    score to screen each frame.

-------------------------------------------------------------
CONTROLS
-------------------------------------------------------------


-------------------------------------------------------------
REFERENCES
-------------------------------------------------------------
pygame-ce docs      https://pyga.me/docs/

"""

import pygame
from os.path import dirname, abspath
from random import uniform, choice, randint

from modules.leaderboard import load_scores, insert_high_score, display_leaderboard, enter_name
# from modules.powerup import spawn_powerups, handle_powerup_collisions

# setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), vsync=1)
pygame.display.set_caption("Brickz")

# assets
from modules.assets import init_assets
init_assets()
from modules.assets import (
    splash_surf,
    basic_paddle_surf, ball_surf,
    font, font_large,
    game_music
)
game_music.play(loops=-1)

# -------------------------------------------------------------
# classes
# -------------------------------------------------------------

class GameState():
    def __init__(self):
        # app
        self.app_running = True

        # initialise game state
        self.reset()
        self.current_state = "splash"

    def reset(self):
        pass

    def state(self):
        pass

        """
        splash_screen
        new_level
        in_play
        game_over
        """

# sprite classes

class Paddle(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass

class Ball(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass

class Brick(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass

class ColourBrick(Brick):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass

    def apply_crack():
        pass
        # play crack sound

    def break_brick():
        pass
        # play break sound

class MetalBrick(Brick):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass

    def ting():
        pass
        # play ting sound
        # play ting animation (white wave)

    def break_brick():
        pass
        # play break sound

class ExplosiveBrick(Brick):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass
    
    def explode_brick():
        pass
        # play explode sound

# particle sprite classes

class Particle(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass

class ImpactParticle(Particle):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass
        # only for when brick transforms to cracked
        # colour palette based upon parent brick
        # small impact point puff

class ExplodeParticle(Particle):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass
        # only for explosive bricks
        # red/orange colour palette
        # big explosion, centrally sourced

class BreakParticle(Particle):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass
        # only coloured bricks and metal bricks
        # larger particles
        # colour palette based upon parent brick
        # TBC origin source

# -------------------------------------------------------------
# draw functions
# -------------------------------------------------------------

def draw_splash():
    # the background image
    scaled_splash = pygame.transform.scale(splash_surf, (WINDOW_WIDTH, WINDOW_HEIGHT))
    window.blit(scaled_splash, (0, 0))

    # start game instructions
    prompt_surf = font.render("Press any key", True, (240, 240, 240))
    prompt_rect = prompt_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 150))
    show_prompt = (pygame.time.get_ticks() // 500) % 2 == 0 # flips between True and False every half second
    if show_prompt:
        window.blit(prompt_surf, prompt_rect)

def draw_background():
    pass

def draw_sprites():
    game.all_sprites.draw(window)

# -------------------------------------------------------------
# game functions
# -------------------------------------------------------------

def handle_collisions():
    pass

def handle_input(event, dt):
    # splash state - any key pressed
    if event.type == pygame.KEYDOWN and game.current_state == "splash":
        game.state(dt)

    # Q or window close - quit (unless a prior state has intercepted the keypress)
    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_q) or event.type == pygame.QUIT:
        game.app_running = False

    # game_over state - enter name, then restart game
    elif event.type == pygame.KEYDOWN and game.current_state == "game_over":
        if game.entering_name:
            enter_name(event, game)
        elif event.key == pygame.K_r:
            game.reset()
    
    # ESC pressed - pause/unpause (checked independently of other conditions)
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        if not game.current_state == "paused":
            game.previous_state = game.current_state
            game.current_state = "paused"
        else:
            game.current_state = game.previous_state

# -------------------------------------------------------------
# game running
# -------------------------------------------------------------

game = GameState()
game.window = window
game.WINDOW_WIDTH = WINDOW_WIDTH
game.WINDOW_HEIGHT = WINDOW_HEIGHT
clock = pygame.time.Clock()
clamp = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

# -------------------------------------------------------------
# game loop
# -------------------------------------------------------------

while game.app_running:
    dt = clock.tick(60) / 1000
    game.current_time = pygame.time.get_ticks()
    window.fill("black")

    for event in pygame.event.get(): # if input events happen (keyboard, mouse etc)
        handle_input(event, dt)

    if game.current_state == "splash":
        draw_splash()
    elif game.current_state == "new_level":
        game.state(dt)
        draw_sprites()
    elif game.current_state == "in_play":
        game.state(dt)
        draw_sprites()
        draw_background()
    elif game.current_state == "paused":
        draw_sprites()
        draw_background()
    elif game.current_state == "game_over":
        game.state(dt)

    pygame.display.update()

pygame.quit()