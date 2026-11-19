import pygame
import constants

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), constants.LINE_WIDTH)

    def update(self, dt: float) -> None:
        # must override
        pass

    def wrap(self) -> None:
        # once fully off one edge, reappear just off the opposite edge
        w, h, r = constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, self.radius
        if self.position.x < -r:
            self.position.x = w + r
        elif self.position.x > w + r:
            self.position.x = -r
        if self.position.y < -r:
            self.position.y = h + r
        elif self.position.y > h + r:
            self.position.y = -r

    def collides_with(self, other):
        if pygame.Vector2.distance_to(self.position, other.position) <= self.radius + other.radius:
            return True
        else:
            return False
