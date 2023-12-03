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

        # 4. set timer event - create enemy plane 1s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

def start_game(self):
    print("Game start")
    while True:
        # 1. set FPS
        self.clock.tick(FRAME_PER_SEC)
        # 2. event listening
        self.__event_handler()
        # 3. collision detection
        self.__check_collide()
        # 4. update and draw sprites
        self.__update_sprites()
        # 5. update display
        pygame.display.update()

def __create_sprites(self):
    # create background sprite and sprite group
    bg1 = Background()
    bg2 = Background(True)
    self.back_group = pygame.sprite.Group(bg1, bg2)

    # create enemy plane sprite and sprite group
    self.enemy_group = pygame.sprite.Group()

    # create hero plane sprite and sprite group
    self.hero = Hero()
    self.hero_group = pygame.sprite.Group(self.hero)

def __event_handler(self):
    for event in pygame.event.get():
        # check if quit
        if event.type == pygame.QUIT:
            SpaceShooter.__game_over()
        elif event.type == CREATE_ENEMY_EVENT:
            # create enemy plane sprite
            self.enemy = Enemy()
            # add enemy plane sprite to enemy plane sprite group
            self.enemy_group.add(self.enemy)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.hero.fire()
    
    # get pressed key
    key_pressed = pygame.key.get_pressed()
    # check if pressed key is a tuple
    if key_pressed[pygame.K_RIGHT]:
        self.hero.speed = 3
    elif key_pressed[pygame.K_LEFT]:
        self.hero.speed = -3
    elif key_pressed[pygame.K_UP]:
        self.hero.speed2 = -3
    elif key_pressed[pygame.K_DOWN]:
        self.hero.speed2 = 3
    else:
        self.hero.speed = 0
        self.hero.speed2 = 0

def __check_collide(self):
    bomb.enemies = pygame.sprite.groupcollide(self.enemy_group, self.hero.bullets, False, True)
    self.bomb_group.add(bomb_enemies)

    # print bomb enemies
    print(self.bomb_group)
    for enemy1 in self.bomb_group:
        print(enemy1.explode_index)
        if enemy1.explode_index == 0:
            enemy1.explode_index = 1
        elif enemy1.explode_index == 5:
            self.enemy_group.remove_internal(enemy1)
            self.bomb_group.remove_internal(enemy1)