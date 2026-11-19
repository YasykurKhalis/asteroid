import pygame
import circleshape
import constants

class Bomb(circleshape.CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, constants.BOMB_RADIUS)
        self.fuse = constants.BOMB_FUSE_SECONDS

    def draw(self, screen: pygame.Surface):
        if int(self.fuse * 10) % 2:
            pygame.draw.circle(screen, "red", self.position, self.radius)
        pygame.draw.circle(screen, "red", self.position, self.radius, constants.LINE_WIDTH)

    def update(self, dt: float):
        self.fuse -= dt
