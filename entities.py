import random
from abc import ABC, abstractmethod
import pygame
from config import *
import math

class Entity(pygame.sprite.Sprite, ABC):

    def __init__(self,spawn_probability,spawn_location, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.spawn_probability = spawn_probability
        self.spawn_location = spawn_location
        self.is_spawned = False

    @abstractmethod
    def spawn(self):
        if random.random <= self.spawn_probability:
            self.is_spawned = True
            print(f"{self.__class__.__name__} is spawned at {self.spawn_location}." )
    @abstractmethod
    def despawn(self):
        if self.is_spawned:
            self.is_spawned = False
            print(f"{self.__class__.__name__} despawned." )
        else:
            print(f"{self.__class__.__name__} is not currently spawned. ")

class PowerUpEntity(Entity):

    def __init__(self,spawn_probability,spawn_location,effect,duration):
        super().__init__(spawn_probability, spawn_location)
        self.duration = duration
class TreasureChest(Entity):
    def __init__(self, spawn_probability, spawn_location, rewards):
        super().__init__(spawn_probability, spawn_location)
        self.rewards = rewards

    def open(self):
        if self.is_spawned:
            print(f"{self.__class__.__name__} opened and you received: {', '.join(self.rewards)}")
            self.despawn()
class Enemy(Entity):
    def __init__(self,spawn_probability, spawn_location, speed, hp):
        super().__init__(spawn_probability, spawn_location)
        self.image = pygame.Surface((enemy_size, enemy_size))
        self.image.fill(red)
        self.speed = speed
        self.hp = hp
    @abstractmethod
    def _move(self, player):
        direction = math.atan2(
            player.rect.y - self.rect.y, player.rect.x - self.rect.x
        )
        self.rect.x += self.speed * math.cos(direction)
        self.rect.y += self.speed * math.sin(direction)
        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)
    @abstractmethod
    def take_damage(self,damage):
        if self.is_spawned:
            self.hp -= damage
            print(f"{self.__class__.__name__} took {damage}, {self.hp} HP remaining.")
            if self.hp <= 0:
                print(f"{self.__class__.__name__} is defeated.")
                self.despawn()


    def update(self, player):
        self._move(self, player)





