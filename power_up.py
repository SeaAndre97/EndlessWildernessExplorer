# power_up.py

import pygame
import random
from abc import ABC, abstractmethod

class PowerUp(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y, image, duration):
        pygame.sprite.Sprite.__init__(self)  # Properly initialize Sprite
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.duration = duration  # Duration in milliseconds
        self.start_time = None
        self.active = False

    @abstractmethod
    def affect_player(self, player):
        pass

    @abstractmethod
    def affect_game(self, game):
        pass

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = None

class InvincibilityPowerUp(PowerUp):
    def __init__(self, x, y, image, duration):
        super().__init__(x, y, image, duration)

    def affect_player(self, player):
        if self.active:
           player.set_invincibility_on()
        else:
            player.set_invincibility_off()

    def affect_game(self, game):
        pass  # No effect on the game state

class DeSpawnerPowerUp(PowerUp):
    def __init__(self, x, y, image, duration, spawn_reduction_factor=0.5):
        super().__init__(x, y, image, duration)
        self.spawn_reduction_factor = spawn_reduction_factor
        self.original_spawn_interval = None

    def affect_player(self, player):
        pass  # No effect on the player

    def affect_game(self, game):
        if self.active:
            if self.original_spawn_interval is None:
                # Reduce spawn rate
                self.original_spawn_interval = game.enemy_spawn_interval
                game.enemy_spawn_interval *= self.spawn_reduction_factor
                # Remove enemies probabilistically
                for enemy in game.enemies.sprites():
                    if random.random() < 0.5:
                        enemy.kill()
        else:
            if self.original_spawn_interval is not None:
                # Restore original spawn rate
                game.enemy_spawn_interval = self.original_spawn_interval
                self.original_spawn_interval = None