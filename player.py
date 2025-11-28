from circleshape import CircleShape
from shot import Shot
from constants import (
    PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED,
    PLAYER_ACCELERATION, PLAYER_MAX_SPEED, PLAYER_DRAG,
    SHOT_RADIUS, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_INVULNERABILITY_SECONDS, PLAYER_BLINK_RATE
)
import sounds as sound_module
import pygame

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, radius=PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0.0
        self.invulnerable_timer = 0.0
        self.blink_timer = 0.0
        self.visible = True

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        if self.visible:
            pygame.draw.polygon(screen, "white", self.triangle(), width=LINE_WIDTH)

    def is_invulnerable(self):
        return self.invulnerable_timer > 0

    def respawn(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.invulnerable_timer = PLAYER_INVULNERABILITY_SECONDS
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shot_cooldown -= dt

        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt
            self.blink_timer -= dt
            if self.blink_timer <= 0:
                self.visible = not self.visible
                self.blink_timer = PLAYER_BLINK_RATE
        else:
            self.visible = True

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.accelerate(dt)
        if keys[pygame.K_s]:
            self.accelerate(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        # Apply velocity and drag
        self.velocity *= PLAYER_DRAG
        self.position += self.velocity * dt
        self.wrap_position()

    def accelerate(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * dt

        # Clamp to max speed
        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)
    
    def shoot(self):
        if self.shot_cooldown > 0:
            return
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        if sound_module.sounds:
            sound_module.sounds.play_shoot()