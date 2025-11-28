import pygame
import array
import math

SAMPLE_RATE = 22050


def generate_sound(frequency, duration, volume=0.3, wave_type="square"):
    """Generate a simple sound wave."""
    num_samples = int(SAMPLE_RATE * duration)
    samples = array.array('h')

    for i in range(num_samples):
        t = i / SAMPLE_RATE
        
        if wave_type == "square":
            value = 1 if math.sin(2 * math.pi * frequency * t) > 0 else -1
        elif wave_type == "sine":
            value = math.sin(2 * math.pi * frequency * t)
        elif wave_type == "noise":
            import random
            value = random.uniform(-1, 1)
        else:
            value = math.sin(2 * math.pi * frequency * t)

        # Apply envelope (fade out)
        envelope = 1 - (i / num_samples)
        value *= envelope * volume

        samples.append(int(value * 32767))

    sound = pygame.mixer.Sound(buffer=samples)
    return sound


def generate_explosion_sound():
    """Low rumbling explosion sound."""
    num_samples = int(SAMPLE_RATE * 0.3)
    samples = array.array('h')
    import random

    for i in range(num_samples):
        t = i / num_samples
        # Mix of low frequency sine and noise
        freq = 80 * (1 - t * 0.5)  # Descending frequency
        sine = math.sin(2 * math.pi * freq * (i / SAMPLE_RATE))
        noise = random.uniform(-1, 1)
        value = sine * 0.6 + noise * 0.4
        
        # Envelope
        envelope = 1 - t
        value *= envelope * 0.4

        samples.append(int(value * 32767))

    return pygame.mixer.Sound(buffer=samples)


def generate_shoot_sound():
    """High pitched laser pew sound."""
    num_samples = int(SAMPLE_RATE * 0.1)
    samples = array.array('h')

    for i in range(num_samples):
        t = i / num_samples
        # Descending frequency for pew effect
        freq = 800 - 600 * t
        value = math.sin(2 * math.pi * freq * (i / SAMPLE_RATE))
        
        # Quick envelope
        envelope = 1 - t
        value *= envelope * 0.25

        samples.append(int(value * 32767))

    return pygame.mixer.Sound(buffer=samples)


def generate_player_hit_sound():
    """Harsh buzz for player damage."""
    num_samples = int(SAMPLE_RATE * 0.4)
    samples = array.array('h')
    import random

    for i in range(num_samples):
        t = i / num_samples
        # Distorted low frequency
        freq = 120
        square = 1 if math.sin(2 * math.pi * freq * (i / SAMPLE_RATE)) > 0 else -1
        noise = random.uniform(-0.5, 0.5)
        value = square * 0.7 + noise * 0.3
        
        # Pulsing envelope
        pulse = abs(math.sin(math.pi * t * 4))
        envelope = (1 - t) * pulse
        value *= envelope * 0.35

        samples.append(int(value * 32767))

    return pygame.mixer.Sound(buffer=samples)


class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=512)
        self.shoot = generate_shoot_sound()
        self.explosion = generate_explosion_sound()
        self.player_hit = generate_player_hit_sound()

    def play_shoot(self):
        self.shoot.play()

    def play_explosion(self):
        self.explosion.play()

    def play_player_hit(self):
        self.player_hit.play()


# Global sound manager instance
sounds = None


def init_sounds():
    global sounds
    sounds = SoundManager()
    return sounds

