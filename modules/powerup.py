"""

=============================================================
powerup.py
=============================================================
Powerup system for P0N6 FL1P!

-------------------------------------------------------------
CLASSES
-------------------------------------------------------------
PowerUp             Base sprite class. Handles the shared
                    duration timer for both uncollected
                    (despawn after timeout) and active
                    (expire after duration) states.



-------------------------------------------------------------
FUNCTIONS
-------------------------------------------------------------
spawn_powerups(game, WINDOW_WIDTH, WINDOW_HEIGHT)
    Spawns a random powerup icon on the centre line,
    excluding any type already active or on screen.
    Called from handle_collisions in main.py with a
    1 in 10 chance per face paddle hit.

handle_powerup_collisions(i, game)
    Called when the ball collides with a powerup sprite.
    Adds the powerup to game.active_powerup, kills the
    icon sprite, and calls apply().

-------------------------------------------------------------
DEPENDENCIES
-------------------------------------------------------------
Assets imported locally inside __init__ and apply methods
to avoid initialisation order issues with modules/assets.py.
game is passed as a parameter throughout to avoid circular
imports with main.py.

"""

import pygame
from random import randint, choice

# -------------------------------------------------------------
# classes
# -------------------------------------------------------------

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)