import pygame
import circleshape
import constants

class Shot(circleshape.CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, constants.SHOT_RADIUS)
        self.life = constants.SHOT_LIFETIME_SECONDS
    
    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, "white", self.position, self.radius, constants.LINE_WIDTH)
    
    def update(self, dt: float):
        self.position += self.velocity * dt
        self.wrap()
        self.life -= dt
        if self.life <= 0:
            self.kill()
