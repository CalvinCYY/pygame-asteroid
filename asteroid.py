from circleshape import CircleShape
from constants import LINE_WIDTH
from logger import log_event
from constants import ASTEROID_MIN_RADIUS, ASTEROID_SPLIT_SPEED
import random
import pygame

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, width=LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
    
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        angle =random.uniform(20, 50)
        angle1 = self.velocity.rotate(angle)
        angle2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        Asteroid(self.position.x, self.position.y, new_radius).velocity = angle1 * ASTEROID_SPLIT_SPEED
        Asteroid(self.position.x, self.position.y, new_radius).velocity = angle2 * ASTEROID_SPLIT_SPEED