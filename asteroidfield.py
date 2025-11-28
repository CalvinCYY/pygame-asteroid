import pygame
import random
from asteroid import Asteroid
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_MAX_RADIUS, ASTEROID_MIN_RADIUS,
    ASTEROID_KINDS, WAVE_BASE_ASTEROIDS, WAVE_ASTEROIDS_INCREMENT,
    WAVE_SPEED_MULTIPLIER
)


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def spawn_wave(self, wave_number):
        asteroid_count = WAVE_BASE_ASTEROIDS + (wave_number - 1) * WAVE_ASTEROIDS_INCREMENT
        speed_multiplier = WAVE_SPEED_MULTIPLIER ** (wave_number - 1)

        for _ in range(asteroid_count):
            edge = random.choice(self.edges)
            base_speed = random.randint(40, 100)
            speed = base_speed * speed_multiplier
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)

    def update(self, dt):
        pass