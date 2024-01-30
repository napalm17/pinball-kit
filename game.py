import math
import pygame
from pathlib import Path
from ball import Ball, Electron
from level import Level
from triangle import Triangle
from flipper import Flipper
from math import pi, radians


class Game:
    """ Implements a Pinball game. """

    # We define our class variables.
    s_width = 600
    s_height = 800
    OMEGA = 1
    GRAVITY_X = 0.0
    GRAVITY_Y = 20
    GRAVITY = GRAVITY_X, GRAVITY_Y
    DT = 0.01 # ms (discretization of time)

    def __init__(self):
        # Initialize PyGame
        pygame.init()

        # Initial window size
        self.screen = pygame.display.set_mode((Game.s_width, Game.s_height), pygame.RESIZABLE)
        self.background = pygame.image.load(Path(__file__).parents[0] / Path("bl.jpg")).convert()
        self.clock = pygame.time.Clock()
        self.running = True
        self.ball = None
        self.level = Level(atomic_number=1)
        self.leveled_up = False
        self.triangles = None
        self.flippers = None
        self.flippers_pressed = [False, False]
        self.flipper_rotating = False
        self.just_collided = False


    # You could declare components (the initial ball, the other items, ...) here
    def run(self):
        """ Main event loop for the pinball game. """

        while self.running:

            """ Collect player input for the flippers. """
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.flippers[0].is_flipped = True
                    if event.key == pygame.K_RIGHT:
                        self.flippers[1].is_flipped = True

            # Adjust screen
            bg = pygame.transform.scale(self.background, (Game.s_width, Game.s_height))
            self.screen.blit(bg, (0, 0)) # redraws background image
            self.update_triangles()
            self.update_flippers()
            self.update_ball()
            self.update_level()


            pygame.display.flip() # Update the display of the full screen

        # Done! Time to quit.
    def update_ball(self):
        """ Updates the state of the game ball. """
        if self.ball is None:
            self.ball = Ball(radius=30, velocity=(-5, 5))

        self.collide_with_walls(self.ball)
        self.collide_with_flippers(self.ball)
        self.collide_with_triangles(self.ball)
        self.collide_with_particles(self.ball)

        self.move_ball(self.ball)
        pygame.draw.circle(self.screen, (35, 161, 224), self.ball.position, self.ball.radius)

    def update_level(self):
        """ Update the state of the particles in game, level up if certain conditions met. """
        if self.leveled_up:
            self.level = Level(self.level.atomic_number + 1)

        for particle_subgroup in self.level.particles:
            for particle in particle_subgroup:
                if type(particle) is type(Electron()):
                    self.move_electron(particle)
                pygame.draw.circle(self.screen, (35, 161, 224), particle.position, particle.radius)

    def move_electron(self, particle):
        """ Rotates the electron around the nucleus. """
        omega = particle.velocity.magnitude() / 200
        particle.velocity.rotate_ip_rad(omega*Game.DT)
        particle.position.xy += particle.velocity.xy * Game.DT

    def move_ball(self, object):
        """ Calculates the ball's trajectory in a constant gravity field. """
        object.velocity.y += Game.GRAVITY_Y * Game.DT
        object.position.xy += object.velocity.xy * Game.DT

    def collide_with_walls(self, object):
        """ Bounces the ball back if it comes into contact with the edges of the screen. """
        inside_screen_y = 0 + object.radius < object.position.y
        if not inside_screen_y:
            object.velocity.y *= -1
        inside_screen_x = 0 + object.radius < object.position.x < self.screen.get_width() - object.radius
        if not inside_screen_x:
            object.velocity.x *= -1

    def collide_with_triangles(self, object):
        """ Bounces the ball back if collides with the triangles. """
        if not self.just_collided:
            for triangle in self.triangles:
                if triangle.is_inside_triangle(object.position):
                    self.just_collided = True
                    alpha = pi - 2 * radians(object.velocity.angle_to(triangle.line))   # rotate ball velocity according to
                    object.velocity.rotate_ip_rad(alpha)
                    self.move_ball(object)
        else:
            self.just_collided = False

    def collide_with_flippers(self, object:Ball):
        """ Bounces the ball back if it collides with the flippers. """
        if not self.just_collided:
            for flipper in self.flippers:
                if flipper.is_inside_line(object.position):
                    self.just_collided = True
                    alpha = pi - 2 * radians(object.velocity.angle_to(flipper.line))
                    object.velocity.rotate_ip_rad(alpha)
                    self.move_ball(object)
        else:
            self.just_collided = False


    def collide_with_particles(self, object:Ball):
        if not self.just_collided:
            for particle_subgroup in self.level.particles:
                for particle in particle_subgroup:
                    if particle.position.distance_to(object.position) <= (particle.radius + object.radius):
                        self.just_collided = True
                        print("collision!!!!")
                        alpha = 2 * radians(object.velocity.angle_to(object.position - particle.position))
                        object.velocity.rotate_ip_rad(alpha)

        else:
            self.just_collided = False

    def update_triangles(self):
        """ Draws the triangles in the corners. """
        triangle_length = 150
        if self.triangles is None:
            self.triangles = (Triangle(((0, Game.s_height), (0, Game.s_height - triangle_length), (triangle_length, Game.s_height))),
                              Triangle(((Game.s_width, Game.s_height), (Game.s_width, Game.s_height - triangle_length), (Game.s_width-triangle_length, Game.s_height))))
        for triangle in self.triangles:
            pygame.draw.polygon(self.screen, (200, 200, 200), triangle.edges)

    def update_flippers(self):
        """ Activates the flippers according to player input. """
        flipper_length = 120
        if self.flippers is None:  # Create flippers.
            self.flippers = (Flipper((150, Game.s_height), (150 + flipper_length, Game.s_height)),
                             Flipper((Game.s_width-150, Game.s_height), (Game.s_width-150-flipper_length, Game.s_height)))

        for i, flipper in zip(range(2), self.flippers): # Iterate over two flippers
            if flipper.is_flipped:  # If activated, give the flipper an initial velocity.
                flipper.is_rotating = True
                flipper.angular_velocity = -0.5
            if flipper.is_rotating:  # Let the flipper rotate under the force of gravity until it comes down.
                angular_acceleration = Game.GRAVITY_Y / flipper.length**2 * (Game.s_height - flipper.end.y)
                flipper.angular_velocity += angular_acceleration * Game.DT
                flipper.rotate_around_base(flipper.angular_velocity*Game.DT*(-1)**i)
                if flipper.end.y > Game.s_height:
                    flipper.is_rotating = False
            flipper.is_flipped = False
            pygame.draw.line(self.screen, (100, 200, 200), flipper.base, flipper.end, width=20)
