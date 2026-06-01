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
    basic_paddle_surf, ball_surf, crack,
    test_level,
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

        # sprite groups - persists across resets
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()
        self.ball_sprites = pygame.sprite.Group()
        self.brick_sprites = pygame.sprite.Group()
        self.powerup_sprites = pygame.sprite.Group()

        # initialise game state
        self.reset()
        self.current_state = "splash"

    def reset(self):
        # gameplay
        self.cur_score = 0
        self.final_score = 0
        self.last_countdown = None
        self.point_start = pygame.time.get_ticks()
        self.current_state = "get_ready"

        # leaderboard
        self.entering_name = False
        self.pending_name = ""

        # sprites
        self.all_sprites.empty()
        self.paddle_sprites.empty()
        self.ball_sprites.empty()
        self.powerup_sprites.empty()
        self.brick_sprites.empty()
        self.ball = None
        self.paddle = None
        #self.score = ScoreTracker()

    def state(self, dt):
        # splash state active
        if self.current_state == "splash":
            self.current_state = "get_ready"
            self.paddle = Paddle(self, self.all_sprites, self.paddle_sprites)
            self.ball = Ball(self, self.all_sprites, self.ball_sprites)
            build_level(self)

        # get_ready state active
        elif self.current_state == "get_ready":
            if not self.paddle:
                self.paddle = Paddle(self, self.all_sprites, self.paddle_sprites)
            if not self.ball:
                self.ball = Ball(self, self.all_sprites, self.ball_sprites)
            
            self.paddle.update()
            self.ball.update(self, dt)

        # in_play state active
        elif self.current_state == "in_play":
            self.paddle.update()
            # self.score.update()
            self.ball.update(self, dt)
            handle_collisions()
            # for p in list(self.active_powerup):
            #     p.update(game, dt)
            # self.powerup_sprites.update(game, dt)
            pass

        # game_over state active
        elif self.current_state == "game_over":
            display_leaderboard(game, font, window, WINDOW_WIDTH, WINDOW_HEIGHT)
            prompt_surf = font.render("Press R to play again, or Q to quit", True, (240, 240, 240))
            prompt_rect = prompt_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 150))
            show_prompt = (pygame.time.get_ticks() // 500) % 2 == 0
            if show_prompt and not self.entering_name:
                window.blit(prompt_surf, prompt_rect)

# sprite classes

class Paddle(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        self.image = basic_paddle_surf
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 60))
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        mouse_x = pygame.mouse.get_pos()[0]
        self.rect.centerx = mouse_x
        self.rect.clamp_ip(clamp)

class Ball(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        self.image = ball_surf
        self.rect = self.image.get_frect(midbottom = (game.paddle.rect.centerx + 10, game.paddle.rect.top))
        self.rect.clamp_ip(clamp)
        self.stuck = True
        self.speed = None
        self.speed_multiplier = 1
        self.velocity = None
        self.mask = pygame.mask.from_surface(self.image)
        self.previous_rect = self.rect.copy()

    def launch(self, game):
        self.stuck = False
        game.current_state = "in_play"
        self.speed = 500
        offset = (game.ball.rect.centerx - game.paddle.rect.centerx) / 50
        self.velocity = pygame.Vector2(offset, -1)
        self.velocity = self.velocity.normalize() * self.speed

    def update(self, game, dt):
        if self.stuck:
            self.rect = self.image.get_frect(midbottom = (game.paddle.rect.centerx + 10, game.paddle.rect.top))
            if pygame.mouse.get_just_pressed()[0]:
                self.launch(game)
        else:# move the ball
            effective_multiplier = min(game.ball.speed_multiplier, 2.5)
            self.previous_rect = self.rect.copy()
            self.rect.center += self.velocity * effective_multiplier * dt
            if self.rect.top <= play_area.top:
                self.velocity.y *= -1
                self.rect.top = play_area.top
            elif self.rect.left <= play_area.left:
                self.velocity.x *= -1
                self.rect.left = play_area.left
            elif self.rect.right >= play_area.right:
                self.velocity.x *= -1
                self.rect.right = play_area.right
            elif self.rect.bottom >= play_area.bottom:
                game.current_state = "get_ready"
                game.ball = None
                self.kill()

class Brick(pygame.sprite.Sprite):
    def __init__(self, game, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((80, 27))
        self.rect = self.image.get_frect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

class ColourBrick(Brick):
    def __init__(self, game, x, y, colour, durability, *groups):
        super().__init__(game, x, y, *groups)   # hands position + groups to Brick
        self.image.fill(colour)
        self.durability = durability

    def apply_crack(self):
        self.image.blit(crack, (0, 0))
        # play crack sound

    def break_brick(self):
        pass
        # play break sound

class MetalBrick(Brick):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass

    def ting(self):
        pass
        # play ting sound
        # play ting animation (white wave)

    def break_brick(self):
        pass
        # play break sound

class ExplosiveBrick(Brick):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass
    
    def explode_brick(self):
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
    prompt_surf = font.render("Click to start", True, (240, 240, 240))
    prompt_rect = prompt_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 150))
    show_prompt = (pygame.time.get_ticks() // 500) % 2 == 0 # flips between True and False every half second
    if show_prompt:
        window.blit(prompt_surf, prompt_rect)

def draw_background():
    window.fill("#010523")
    pygame.draw.rect(window, "#CC00CC", play_area, 3)

def draw_sprites():
    game.all_sprites.draw(window)

def build_level(game):
    padding = 30.5
    gap = 3
    brick_width = 80
    brick_height = 27
    for row in range(10):
        for column in range (14):
            pixel = test_level.get_at((column, row))
            x = play_area.left + padding + column * (brick_width + gap)
            y = play_area.top + padding + row * (brick_height + gap)
            if pixel.a == 0:     
                continue
            else:
                durability = 1 if pixel.a == 255 else 2
            if pixel[:3] == (255, 255, 255):
                # metal
                continue
            elif pixel[:3] == (0, 0, 0):
                # explosive
                continue
            else:
                ColourBrick(game, x, y, pixel, durability, game.all_sprites, game.brick_sprites)

# -------------------------------------------------------------
# game functions
# -------------------------------------------------------------

def handle_collisions():
    if not game.ball:
        return
    collision_sprites = pygame.sprite.spritecollide(game.ball, game.brick_sprites, False, pygame.sprite.collide_mask)
    if collision_sprites:
        prev = game.ball.previous_rect
        flipped_x = False
        flipped_y = False
        for brick in collision_sprites:

            # ball going right
            if prev.right <= brick.rect.left:
                if not flipped_x:
                    game.ball.rect.right = brick.rect.left
                    game.ball.velocity.x *= -1
                    flipped_x = True

            # ball going left
            elif prev.left >= brick.rect.right:
                if not flipped_x:
                    game.ball.rect.left = brick.rect.right
                    game.ball.velocity.x *= -1
                    flipped_x = True

            # ball going down
            elif prev.bottom <= brick.rect.top:
                if not flipped_y:
                    game.ball.rect.bottom = brick.rect.top
                    game.ball.velocity.y *= -1
                    flipped_y = True

            # ball going up
            elif prev.top >= brick.rect.bottom:
                if not flipped_y:
                    game.ball.rect.top = brick.rect.bottom
                    game.ball.velocity.y *= -1
                    flipped_y = True

# Known limitation: perfect corner hits resolve as a vertical-face bounce.
# Deliberately unhandled - rare and visually acceptable.
            
            brick.durability -= 1
            if brick.durability <= 0:
                brick.kill()          # later: spawn break particles
            else:
                brick.apply_crack()   # only reached when it survived, i.e. dropped to 1

    collision_sprites = pygame.sprite.spritecollide(game.ball, game.paddle_sprites, False)
    if collision_sprites:
        prev = game.ball.previous_rect
        for paddle in collision_sprites:
            if prev.bottom >= paddle.rect.top:
                if game.ball.velocity.y > 0:
                    game.ball.rect.bottom = paddle.rect.top
                    game.ball.velocity.y *= -1
                    offset = (game.ball.rect.centerx - game.paddle.rect.centerx) / 50
                    game.ball.velocity = pygame.Vector2(offset, -1)
                    game.ball.velocity = game.ball.velocity.normalize() * game.ball.speed

def handle_input(event, dt):
    # splash state - any key pressed
    if event.type == pygame.MOUSEBUTTONDOWN and game.current_state == "splash":
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

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
game = GameState()
game.window = window
game.WINDOW_WIDTH = WINDOW_WIDTH
game.WINDOW_HEIGHT = WINDOW_HEIGHT
clock = pygame.time.Clock()
play_area = pygame.Rect(30, 100, 1220, 590)
clamp = play_area

# -------------------------------------------------------------
# game loop
# -------------------------------------------------------------

while game.app_running:
    dt = clock.tick(60) / 1000
    game.current_time = pygame.time.get_ticks()
    window.fill("#010523")

    for event in pygame.event.get(): # if input events happen (keyboard, mouse etc)
        handle_input(event, dt)

    if game.current_state == "splash":
        draw_splash()
    elif game.current_state == "get_ready":
        game.state(dt)
        draw_background()
        draw_sprites()
    elif game.current_state == "in_play":
        game.state(dt)
        draw_background()
        draw_sprites()
    elif game.current_state == "paused":
        draw_background()
        draw_sprites()
    elif game.current_state == "game_over":
        game.state(dt)

    pygame.display.update()

pygame.quit()