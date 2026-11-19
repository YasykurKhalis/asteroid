import pygame
import circleshape
import constants

class PowerUp(circleshape.CircleShape):
    COLORS = {"shield": "cyan", "speed": "yellow"}

    def __init__(self, x: float, y: float, kind: str) -> None:
        super().__init__(x, y, constants.POWERUP_RADIUS)
        self.kind = kind
        self.life = constants.POWERUP_LIFETIME_SECONDS

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.COLORS[self.kind], self.position, self.radius, constants.LINE_WIDTH)
        pygame.draw.circle(screen, self.COLORS[self.kind], self.position, self.radius / 3)

    def update(self, dt: float):
        self.life -= dt
        if self.life <= 0:
            self.kill()
