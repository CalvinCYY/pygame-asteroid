from enum import Enum, auto


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_RADIUS = 20
LINE_WIDTH = 2

PLAYER_TURN_SPEED = 300
PLAYER_ACCELERATION = 300        # How fast player speeds up
PLAYER_MAX_SPEED = 400           # Maximum velocity
PLAYER_DRAG = 0.98               # Friction multiplier per frame (1.0 = no drag)

ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = 0.8
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_SPLIT_SPEED = 1.2
ASTEROID_VERTICES = 10           # Number of vertices in asteroid shape
ASTEROID_JAGGEDNESS = 0.4        # How lumpy (0 = circle, 1 = very jagged)
ASTEROID_ROTATION_SPEED = 40     # Degrees per second

SHOT_RADIUS = 5
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN_SECONDS = 0.3

# Scoring - smaller asteroids are worth more points
ASTEROID_SCORE = {
    ASTEROID_MIN_RADIUS * 3: 20,   # Large asteroid
    ASTEROID_MIN_RADIUS * 2: 50,   # Medium asteroid
    ASTEROID_MIN_RADIUS: 100,      # Small asteroid
}

# HUD
HUD_FONT_SIZE = 36
HUD_PADDING = 20

# Lives
PLAYER_STARTING_LIVES = 3
PLAYER_INVULNERABILITY_SECONDS = 2.0
PLAYER_BLINK_RATE = 0.1  # How fast player blinks when invulnerable

# Waves
WAVE_BASE_ASTEROIDS = 4          # Asteroids in wave 1
WAVE_ASTEROIDS_INCREMENT = 2     # Additional asteroids per wave
WAVE_DELAY_SECONDS = 2.0         # Pause between waves
WAVE_SPEED_MULTIPLIER = 1.1      # Speed increase per wave (compounding)

# Particles
PARTICLE_COUNT = 8               # Particles per explosion
PARTICLE_SPEED_MIN = 50
PARTICLE_SPEED_MAX = 150
PARTICLE_LIFETIME = 0.6          # Seconds before particle disappears
PARTICLE_SIZE = 3