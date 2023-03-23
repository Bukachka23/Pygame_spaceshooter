import pygame

from models import Spaceship, Asteroid
from utils import load_sprite, get_random_position, print_text, load_sound

# The main game class
class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    # The constructor is needed to initialize the game objects
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("galaxy", scale_factor=0.3)
        self.theme_sound = load_sound("space")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        self.theme_sound.play()

        # Create the asteroids
        for _ in range(8):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    # Draws the game objects on the screen
    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        # The spaceship is drawn last so it appears on top of the other objects
        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects

    # The main loop of the game
    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    # Initializes pygame and sets the window caption
    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    # Handles the user input and updates the game objects
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()

            elif (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_r
            ):
                self.reset_game()
            elif (
                    self.spaceship
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        # Rotate the spaceship if the left or right arrow key is pressed
        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
            elif is_key_pressed[pygame.K_DOWN]:
                self.spaceship.slow_down()

    # Process the game logic and update the game objects
    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        # Check if the spaceship collides with an asteroid
        if self.spaceship:
            for asteroid in self.asteroids:
                if self.spaceship.collides_with(asteroid):
                    if self.spaceship.shield:
                        self.spaceship.shield = False
                        asteroid.split()
                        self.asteroids.remove(asteroid)
                    else:
                        self.spaceship = None
                        self.message = "Game Over"
                        self.theme_sound.stop()
                    break

        # Check if a bullet collides with an asteroid
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        # Remove bullets and asteroids that are outside the screen
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        # Check if all asteroids are destroyed
        if not self.asteroids and self.spaceship:
            self.message = "You Win!"

    # Draws the game objects on the screen
    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        # Draw the game objects
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        # Draw the message
        if self.message:
            print_text(self.screen, self.message, self.font)

        # Update the display
        pygame.display.flip()
        self.clock.tick(60)

    # Resets the game
    def reset_game(self):
        self.asteroids.clear()
        self.bullets.clear()
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        self.message = ""
        self.theme_sound.play()

        # Create the asteroids
        for _ in range(8):
            while True:
                position = get_random_position(self.screen)
                if (
                        position.distance_to(self.spaceship.position)
                        > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))























