from circleshape import CircleShape
from constants import (
    LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_SPLIT_SPEED,
    ASTEROID_VERTICES, ASTEROID_JAGGEDNESS, ASTEROID_ROTATION_SPEED
)
from logger import log_event
import random
import math
import pygame


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-ASTEROID_ROTATION_SPEED, ASTEROID_ROTATION_SPEED)
        self.shape = self._generate_shape()

    def _generate_shape(self):
        """Generate random lumpy asteroid vertices as offsets from center."""
        vertices = []
        for i in range(ASTEROID_VERTICES):
            angle = (2 * math.pi / ASTEROID_VERTICES) * i
            # Randomize radius for each vertex
            offset = random.uniform(1 - ASTEROID_JAGGEDNESS, 1 + ASTEROID_JAGGEDNESS)
            vertices.append((angle, self.radius * offset))
        return vertices

    def _get_polygon_points(self):
        """Get current polygon points based on position and rotation."""
        points = []
        for angle, dist in self.shape:
            rotated_angle = angle + math.radians(self.rotation)
            x = self.position.x + math.cos(rotated_angle) * dist
            y = self.position.y + math.sin(rotated_angle) * dist
            points.append((x, y))
        return points

    def draw(self, screen):
        points = self._get_polygon_points()
        pygame.draw.polygon(screen, "white", points, width=LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt
        self.wrap_position()

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        angle1 = self.velocity.rotate(angle)
        angle2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        Asteroid(self.position.x, self.position.y, new_radius).velocity = angle1 * ASTEROID_SPLIT_SPEED
        Asteroid(self.position.x, self.position.y, new_radius).velocity = angle2 * ASTEROID_SPLIT_SPEED