import pygame
import random
import math
from constants import (
    PARTICLE_COUNT, PARTICLE_SPEED_MIN, PARTICLE_SPEED_MAX,
    PARTICLE_LIFETIME, PARTICLE_SIZE
)


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        speed = random.uniform(PARTICLE_SPEED_MIN, PARTICLE_SPEED_MAX)
        self.velocity = pygame.Vector2(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        )
        self.lifetime = PARTICLE_LIFETIME
        self.max_lifetime = PARTICLE_LIFETIME

    def draw(self, screen):
        alpha = self.lifetime / self.max_lifetime
        color = (int(255 * alpha), int(255 * alpha), int(255 * alpha))
        pygame.draw.circle(screen, color, self.position, PARTICLE_SIZE)

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()


def spawn_explosion(x, y):
    for i in range(PARTICLE_COUNT):
        angle = (2 * math.pi / PARTICLE_COUNT) * i
        angle += random.uniform(-0.3, 0.3)
        Particle(x, y, angle)

