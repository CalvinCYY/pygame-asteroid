import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    ASTEROID_SCORE, HUD_FONT_SIZE, HUD_PADDING,
    PLAYER_STARTING_LIVES, WAVE_DELAY_SECONDS
)
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from particle import Particle, spawn_explosion
from sounds import init_sounds

import sys


def draw_hud(screen, font, score, lives, wave):
    score_text = font.render(f"Score: {score}", True, "white")
    lives_text = font.render(f"Lives: {lives}", True, "white")
    wave_text = font.render(f"Wave: {wave}", True, "white")
    screen.blit(score_text, (HUD_PADDING, HUD_PADDING))
    screen.blit(wave_text, (SCREEN_WIDTH // 2 - wave_text.get_width() // 2, HUD_PADDING))
    screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - HUD_PADDING, HUD_PADDING))


def main():
    print(f"Starting Asteroids with pygame version: {pygame.__version__}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    sounds = init_sounds()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    lives = PLAYER_STARTING_LIVES
    wave = 1
    wave_delay_timer = 0.0

    font = pygame.font.Font(None, HUD_FONT_SIZE)
    wave_font = pygame.font.Font(None, 72)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = [updatable, drawable]
    Asteroid.containers = [asteroids, updatable, drawable]
    AsteroidField.containers = [updatable]
    Shot.containers = [shots, updatable, drawable]
    Particle.containers = [updatable, drawable]

    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroidfield = AsteroidField()
    asteroidfield.spawn_wave(wave)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        for sprite in drawable:
            sprite.draw(screen)
    
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    score += ASTEROID_SCORE.get(asteroid.radius, 10)
                    spawn_explosion(asteroid.position.x, asteroid.position.y)
                    sounds.play_explosion()
                    asteroid.split()
                    shot.kill()
                    break
            if asteroid.collides_with(player) and not player.is_invulnerable():
                log_event("player_hit")
                spawn_explosion(player.position.x, player.position.y)
                sounds.play_player_hit()
                lives -= 1
                if lives <= 0:
                    print(f'Game over! Final score: {score}')
                    sys.exit()
                player.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        # Wave transition logic
        if len(asteroids) == 0:
            if wave_delay_timer <= 0:
                wave_delay_timer = WAVE_DELAY_SECONDS
            else:
                wave_delay_timer -= dt
                wave_announce = wave_font.render(f"Wave {wave + 1}", True, "white")
                screen.blit(wave_announce, (
                    SCREEN_WIDTH // 2 - wave_announce.get_width() // 2,
                    SCREEN_HEIGHT // 2 - wave_announce.get_height() // 2
                ))
                if wave_delay_timer <= 0:
                    wave += 1
                    asteroidfield.spawn_wave(wave)

        draw_hud(screen, font, score, lives, wave)
        time_delta = clock.tick(60)
        dt = time_delta/1000
        pygame.display.flip()

if __name__ == "__main__":
    main()
