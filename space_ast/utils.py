import random
from pygame.image import load
from pygame.transform import scale
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame import Color


# Loads a sprite from the assets folder
def load_sprite(name, with_alpha=True, scale_factor=1):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)

    # If the sprite has transparency, convert_alpha() should be used.
    if with_alpha:
        loaded_sprite = loaded_sprite.convert_alpha()
    else:
        loaded_sprite = loaded_sprite.convert()

    # Scale the sprite if needed
    if scale_factor != 1:
        width, height = loaded_sprite.get_size()
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        loaded_sprite = scale(loaded_sprite, (new_width, new_height))

    return loaded_sprite

# Wraps the position of an object around the screen
def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)

# Returns a random position on the screen
def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )

# Returns a random velocity vector
def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)

# Loads a sound from the assets folder
def load_sound(name):
    path = f"assets/sounds/{name}.wav"
    return Sound(path)

# Draws text on the screen
def print_text(surface, text, font, color=Color("white")):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) * 0.5
    surface.blit(text_surface, rect)
