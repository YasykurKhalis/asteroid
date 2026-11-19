import random
import pygame
import circleshape
import constants

class Particle(circleshape.CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, 2)
        self.velocity = pygame.Vector2(0, random.uniform(50, 200)).rotate(random.uniform(0, 360))
        self.life = constants.PARTICLE_LIFETIME_SECONDS

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, "orange", self.position, self.radius)

    def update(self, dt: float):
        self.position += self.velocity * dt
        self.life -= dt
        if self.life <= 0:
            self.kill()

def explode(position: pygame.Vector2, count: int):
    for _ in range(count):
        Particle(position.x, position.y)
