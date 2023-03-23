from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import get_random_velocity, load_sprite, wrap_position, load_sound



UP = Vector2(0, -1)                                                                                                     # The UP vector is used to rotate the spaceship sprite

# The base class for all game objects. It contains the common functionality for all game objects.
class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    # Draws the object on the screen
    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    # Updates the object's position
    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    # Checks if the object collides with another object
    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

# Spaceship class that inherits from GameObject
class Spaceship(GameObject):
    ACCERLATION = 0.2
    MANEUVERABILITY = 3
    BULLET_SPEED = 3

    # The constructor is needed to initialize the spaceship's sprite and velocity
    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("fire_sp")
        #self.acceleration_sound = load_sound("thrust")
        self.direction = Vector2(UP)
        self.shield = True
        self.shield_sprite = load_sprite("shield", scale_factor=0.1)
        self.shield_radius = self.shield_sprite.get_width() / 2
        super().__init__(position, load_sprite("ufo", scale_factor=0.1), Vector2(0))


    # Checks if the spaceship collides with another object
    def collides_with(self, other_obj):
        current_radius = self.shield_radius if self.shield else self.radius
        distance = self.position.distance_to(other_obj.position)
        return distance < current_radius + other_obj.radius

    # Shoots a bullet
    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

    # Rotates the spaceship
    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    # Draws the spaceship on the screen
    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
        if self.shield:
            surface.blit(self.shield_sprite, self.position - self.shield_sprite.get_rect().center)

    # Updates the spaceship's position
    def accelerate(self):
        self.velocity += self.direction * self.ACCERLATION
        #self.acceleration_sound.play()

    # Slows down the spaceship
    def slow_down(self):
        self.velocity *= 0.9


# Asteroid class that inherits from GameObject
class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        # The asteroid's sprite is scaled according to its size
        size_to_scale = {
            3: 1,
            2: 0.5,
            1: 0.25,
        }

        scale = size_to_scale[size]
        # The asteroid's sprite is scaled according to its size
        sprite = rotozoom(load_sprite("asteroid_s", scale_factor=0.1), 0, scale)

        super().__init__(
            position, sprite, get_random_velocity(1, 3)

        )

    # Updates the asteroid's position
    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    # Splits the asteroid into two smaller asteroids
    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                # Creates a new asteroid
                self.create_asteroid_callback(asteroid)


# Bullet class that inherits from GameObject
class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet", scale_factor=0.02), velocity)

    # Updates the bullet's position
    def move(self, surface):
        self.position = self.position + self.velocity