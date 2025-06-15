import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ['SDL_VIDEODRIVER'] = 'dummy'
import pygame
pygame.init()
pygame.display.set_mode((1, 1))

from asteroid import Asteroid
from shot import Shot
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


def test_asteroid_wraps():
    a = Asteroid(SCREEN_WIDTH + 5, SCREEN_HEIGHT + 5, 20)
    a.velocity = pygame.Vector2(0, 0)
    a.update(0)
    assert a.position.x == 0
    assert a.position.y == 0


def test_shot_wraps():
    s = Shot(-5, -5)
    s.velocity = pygame.Vector2(0, 0)
    s.update(0)
    assert s.position.x == SCREEN_WIDTH
    assert s.position.y == SCREEN_HEIGHT
