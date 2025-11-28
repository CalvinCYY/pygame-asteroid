import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    ASTEROID_SCORE, HUD_FONT_SIZE, HUD_PADDING,
    PLAYER_STARTING_LIVES, WAVE_DELAY_SECONDS, GameState
)
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from particle import Particle, spawn_explosion
from sounds import init_sounds


def draw_hud(screen, font, score, lives, wave):
    score_text = font.render(f"Score: {score}", True, "white")
    lives_text = font.render(f"Lives: {lives}", True, "white")
    wave_text = font.render(f"Wave: {wave}", True, "white")
    screen.blit(score_text, (HUD_PADDING, HUD_PADDING))
    screen.blit(wave_text, (SCREEN_WIDTH // 2 - wave_text.get_width() // 2, HUD_PADDING))
    screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - HUD_PADDING, HUD_PADDING))


def draw_centered_text(screen, font, text, y_offset=0, color="white"):
    rendered = font.render(text, True, color)
    x = SCREEN_WIDTH // 2 - rendered.get_width() // 2
    y = SCREEN_HEIGHT // 2 - rendered.get_height() // 2 + y_offset
    screen.blit(rendered, (x, y))


def draw_menu(screen, title_font, font):
    draw_centered_text(screen, title_font, "ASTEROIDS", -80)
    draw_centered_text(screen, font, "Press ENTER to Start", 20)
    draw_centered_text(screen, font, "WASD to Move, SPACE to Shoot", 70, "gray")
    draw_centered_text(screen, font, "ESC to Pause", 110, "gray")


def draw_paused(screen, title_font, font):
    draw_centered_text(screen, title_font, "PAUSED", -40)
    draw_centered_text(screen, font, "Press ESC to Resume", 30)
    draw_centered_text(screen, font, "Press Q to Quit to Menu", 70)


def draw_game_over(screen, title_font, font, score, wave):
    draw_centered_text(screen, title_font, "GAME OVER", -80)
    draw_centered_text(screen, font, f"Final Score: {score}", 0)
    draw_centered_text(screen, font, f"Wave Reached: {wave}", 40)
    draw_centered_text(screen, font, "Press ENTER to Play Again", 100)
    draw_centered_text(screen, font, "Press Q to Quit to Menu", 140)


def reset_game(updatable, drawable, asteroids, shots):
    """Clear all game objects for a fresh start."""
    for sprite in updatable:
        sprite.kill()
    for sprite in drawable:
        sprite.kill()
    for sprite in asteroids:
        sprite.kill()
    for sprite in shots:
        sprite.kill()


def main():
    print(f"Starting Asteroids with pygame version: {pygame.__version__}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    sounds = init_sounds()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    # Fonts
    font = pygame.font.Font(None, HUD_FONT_SIZE)
    title_font = pygame.font.Font(None, 96)
    wave_font = pygame.font.Font(None, 72)

    # Sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = [updatable, drawable]
    Asteroid.containers = [asteroids, updatable, drawable]
    AsteroidField.containers = [updatable]
    Shot.containers = [shots, updatable, drawable]
    Particle.containers = [updatable, drawable]

    # Game state
    state = GameState.MENU
    dt = 0
    score = 0
    lives = PLAYER_STARTING_LIVES
    wave = 1
    wave_delay_timer = 0.0
    player = None
    asteroidfield = None

    def start_new_game():
        nonlocal score, lives, wave, wave_delay_timer, player, asteroidfield
        reset_game(updatable, drawable, asteroids, shots)
        score = 0
        lives = PLAYER_STARTING_LIVES
        wave = 1
        wave_delay_timer = 0.0
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        asteroidfield = AsteroidField()
        asteroidfield.spawn_wave(wave)

    while True:
        log_state()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if state == GameState.MENU:
                    if event.key == pygame.K_RETURN:
                        start_new_game()
                        state = GameState.PLAYING

                elif state == GameState.PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        state = GameState.PAUSED

                elif state == GameState.PAUSED:
                    if event.key == pygame.K_ESCAPE:
                        state = GameState.PLAYING
                    elif event.key == pygame.K_q:
                        reset_game(updatable, drawable, asteroids, shots)
                        state = GameState.MENU

                elif state == GameState.GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        start_new_game()
                        state = GameState.PLAYING
                    elif event.key == pygame.K_q:
                        reset_game(updatable, drawable, asteroids, shots)
                        state = GameState.MENU

        # Clear screen
        screen.fill("black")

        # State-specific logic
        if state == GameState.MENU:
            draw_menu(screen, title_font, font)

        elif state == GameState.PLAYING:
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
                if player.collides_with(asteroid) and not player.is_invulnerable():
                    log_event("player_hit")
                    spawn_explosion(player.position.x, player.position.y)
                    sounds.play_player_hit()
                    lives -= 1
                    if lives <= 0:
                        state = GameState.GAME_OVER
                        break
                    player.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

            # Wave transition logic
            if state == GameState.PLAYING and len(asteroids) == 0:
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

        elif state == GameState.PAUSED:
            # Draw game in background (frozen)
            for sprite in drawable:
                sprite.draw(screen)
            draw_hud(screen, font, score, lives, wave)
            # Draw pause overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill("black")
            overlay.set_alpha(150)
            screen.blit(overlay, (0, 0))
            draw_paused(screen, title_font, font)

        elif state == GameState.GAME_OVER:
            # Draw remaining particles
            updatable.update(dt)
            for sprite in drawable:
                sprite.draw(screen)
            draw_hud(screen, font, score, lives, wave)
            # Draw game over overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill("black")
            overlay.set_alpha(180)
            screen.blit(overlay, (0, 0))
            draw_game_over(screen, title_font, font, score, wave)

        time_delta = clock.tick(60)
        dt = time_delta / 1000
        pygame.display.flip()


if __name__ == "__main__":
    main()
