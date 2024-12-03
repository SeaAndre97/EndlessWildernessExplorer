# player.py

from bullet import Bullet
from config import *
import pygame
import math

# player.py

from bullet import Bullet
from config import *
import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # Properly initialize Sprite
        # Drawing variables
        self.image = pygame.Surface(player_size)
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        # Gameplay variables
        self.speed = 5
        self.health = 100
        self.bullet_cooldown = 0
        self.invincibility = False # Add invincible attribute


    #Setter for invincibility to On
    def set_invincibility_on(self):
        self.invincibility = True

    # Setter for invincibility to Off
    def set_invincibility_off(self):
        self.invincibility = False

    def update(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < height:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < width:
            self.rect.x += self.speed

    def shoot(self, bullets: pygame.sprite.Group):

        if self.bullet_cooldown <= 0:
            for angle in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:
                bullet = Bullet(
                    self.rect.center[0], self.rect.center[1], angle
                )
                bullets.add(bullet)
            self.bullet_cooldown = fps  # Frames until the next shot
        self.bullet_cooldown -= 1

    def draw(self, screen):

        if self.invincible:
            # Visual indication of invincibility
            invincible_image = pygame.Surface(player_size)
            invincible_image.fill((255, 255, 0))  # Yellow color
            screen.blit(invincible_image, self.rect)
        else:
            # Draw the normal player image
            screen.blit(self.image, self.rect)