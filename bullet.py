

from utils import *
from config import *
import math
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: float):
        pygame.sprite.Sprite.__init__(self)  # Properly initialize Sprite
        self.radius = bullet_size
        self.color = yellow
        self.rect = pygame.Rect(
            x - self.radius, y - self.radius, self.radius * 2, self.radius * 2
        )
        self.speed = 7
        self.direction = direction

    def update(self):
        self.rect.x += int(self.speed * math.cos(self.direction))
        self.rect.y += int(self.speed * math.sin(self.direction))
        if (
            self.rect.x < 0
            or self.rect.x > width
            or self.rect.y < 0
            or self.rect.y > height
        ):
            self.kill()

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)