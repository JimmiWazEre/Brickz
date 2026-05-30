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

# setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), vsync=1)
pygame.display.set_caption("Brickz")

# -------------------------------------------------------------
# classes
# -------------------------------------------------------------

class GameState():
    def __init__(self):
        pass

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
        
        """
        Purple > Blue > Green > Yellow > Orange > Red > [breaks]
        """

class MetalBrick(Brick):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass

class ExplosiveBrick(Brick):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass

class ImpactParticle(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass

class ExplodeParticle(pygame.sprite.Sprite):
    def __init__(self, game, *groups):
        super().__init__(*groups)
        pass

# -------------------------------------------------------------
# functions
# -------------------------------------------------------------