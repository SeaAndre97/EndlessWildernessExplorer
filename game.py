from config import *
import math
import pygame
import random

from enemy import Enemy
from player import Player
from power_up import InvincibilityPowerUp, DeSpawnerPowerUp


def execute_game():

    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    # setting up the background:
    screen = pygame.display.set_mode(resolution)
    background = pygame.image.load("img/grass.jpg")
    background = pygame.transform.scale(background, (width, height))

    # Player setup
    player = Player()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Initialize the bullet group
    bullets = pygame.sprite.Group()

    # Initialize the enemy group
    enemies = pygame.sprite.Group()
    enemy_spawn_timer = 0

    # Initialize the power-up group
    power_ups = pygame.sprite.Group()
    power_up_spawn_timer = 0
    active_power_ups = []

    # Create a simple game object to hold game variables
    class GameState:
        def __init__(self):
            self.enemy_spawn_interval = 2 * fps  # Default spawn interval
            self.enemies = enemies

    game = GameState()

    running = True
    while running:
        # Control frame rate
        clock.tick(fps)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

        # Shooting
        player.shoot(bullets)

        # Spawning the enemies
        if enemy_spawn_timer <= 0:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            enemy_spawn_timer = game.enemy_spawn_interval  # Use the game state's spawn interval

        # Spawning power-ups
        if power_up_spawn_timer <= 0:
            chance = random.random()
            if chance < power_up_spawn_chance:
                x = random.randint(0, width)
                y = random.randint(0, height)
                power_up_type = random.choice(['invincibility', 'de_spawner'])
                if power_up_type == 'invincibility':
                    power_up_image = pygame.image.load('img/invincibility.png').convert_alpha()
                    power_up_image = pygame.transform.scale(power_up_image, power_up_size)
                    power_up = InvincibilityPowerUp(x, y, power_up_image, invincibility_duration)
                else:
                    power_up_image = pygame.image.load('img/de_spawner.png').convert_alpha()
                    power_up_image = pygame.transform.scale(power_up_image, power_up_size)
                    power_up = DeSpawnerPowerUp(x, y, power_up_image, de_spawner_duration)
                power_ups.add(power_up)
            power_up_spawn_timer = 5 * fps  # Attempt to spawn a power-up every 5 seconds

        # Checking for collisions between player and power-ups
        collected_power_ups = pygame.sprite.spritecollide(player, power_ups, False)
        for power_up in collected_power_ups:
            power_up.activate()
            power_up.affect_player(player)
            power_up.affect_game(game)
            active_power_ups.append(power_up)
            power_up.kill()  # Remove from the power_ups group

        # Update active power-ups
        for power_up in active_power_ups[:]:  # Copy the list
            elapsed_time = pygame.time.get_ticks() - power_up.start_time
            if elapsed_time >= power_up.duration:
                power_up.deactivate()
                power_up.affect_player(player)
                power_up.affect_game(game)
                active_power_ups.remove(power_up)

        # Update the enemy spawn timer
        enemy_spawn_timer -= 1
        power_up_spawn_timer -= 1

        # Update positions
        player_group.update()
        bullets.update()
        enemies.update(player)
        power_ups.update()

        # Fill the background
        screen.blit(background, (0, 0))

        # Drawing the objects
        player.draw(screen)
        enemies.draw(screen)
        power_ups.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # Visual effects for active power-ups (optional)
        if player.invincible:
            # Optional: Visual indication of invincibility (already handled in player.draw())
            pass

        if any(isinstance(pu, DeSpawnerPowerUp) and pu.active for pu in active_power_ups):
            # Optional: Visual indication for De-spawner effect
            overlay = pygame.Surface((width, height))
            overlay.set_alpha(100)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

        # Check for collisions between player and enemies
        if not player.invincible:
            enemy_hit_list = pygame.sprite.spritecollide(player, enemies, False)
            if enemy_hit_list:
                player.health -= 10
                if player.health <= 0:
                    running = False  # Or handle player death

        pygame.display.flip()