import pygame
import random
from plane_sprite import *

class SpaceShooter(object):
    # spaceshoot main program
    def __init__(self):
        print("Game init")
        # 1. create game window
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2. create game clock
        self.clock = pygame.time.Clock()
        # 3. call private method, create sprites and sprite group
        self.__create_sprites()