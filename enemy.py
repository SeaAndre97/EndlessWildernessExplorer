

from utils import *
from config import *
import pygame
import random
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # Properly initialize Sprite
        # Setting up the surface and rectangle of the enemy
        self.image = pygame.Surface((enemy_size, enemy_size))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        # Positioning
        self.rect.x = random.randint(0, width - enemy_size)
        self.rect.y = random.randint(0, height - enemy_size)
        # Random speed
        self.speed = random.randint(2, 3)
        # Health
        self.health = 10

    def update(self, player):
        direction = math.atan2(
            player.rect.y - self.rect.y, player.rect.x - self.rect.x
        )
        self.rect.x += self.speed * math.cos(direction)
        self.rect.y += self.speed * math.sin(direction)
        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)