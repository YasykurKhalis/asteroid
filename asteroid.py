import pygame
import circleshape
import constants
from explosion import explode
from logger import log_event
import random

class Asteroid(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.lumps = [random.uniform(0.75, 1.15) for _ in range(constants.ASTEROID_LUMP_POINTS)]
    
    def draw(self, screen: pygame.Surface):
        step = 360 / len(self.lumps)
        points = [self.position + pygame.Vector2(0, self.radius * lump).rotate(i * step) for i, lump in enumerate(self.lumps)]
        pygame.draw.polygon(screen, "white", points, constants.LINE_WIDTH)

    def points(self) -> int:
        return constants.ASTEROID_POINTS[round(self.radius / constants.ASTEROID_MIN_RADIUS) - 1]
    
    def split(self):
        self.kill()
        explode(self.position, int(self.radius))
        if self.radius <= constants.ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")

        random_angle = random.uniform(20,50)
        new_asteroids_clockwise_movement = self.velocity.rotate(random_angle)
        new_asteroids_counterclockwise_movement = self.velocity.rotate(-random_angle)
        new_asteroids_radius = self.radius - constants.ASTEROID_MIN_RADIUS

        asteroid_one = Asteroid(self.position.x, self.position.y, new_asteroids_radius)
        asteroid_one.velocity = new_asteroids_clockwise_movement * 1.2
        asteroid_two = Asteroid(self.position.x, self.position.y, new_asteroids_radius)
        asteroid_two.velocity = new_asteroids_counterclockwise_movement * 1.2
    
    def update(self, dt: float):
        self.position += self.velocity * dt
        self.wrap()
