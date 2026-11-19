import pygame
import circleshape
import constants
import shot
import bomb

class Player(circleshape.CircleShape):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.weapon = "blaster"
        self.bombs = constants.BOMB_COUNT
        self.invulnerable_timer = 0
        self.shield_timer = 0
        self.speed_timer = 0
    
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        if self.shield_timer > 0:
            pygame.draw.circle(screen, "cyan", self.position, self.radius * 1.6, constants.LINE_WIDTH)
        # blink while invulnerable after respawning
        if self.invulnerable_timer > 0 and int(self.invulnerable_timer * 10) % 2:
            return
        color = "yellow" if self.speed_timer > 0 else "white"
        pygame.draw.polygon(screen, color, self.triangle(), constants.LINE_WIDTH)

    def collides_with(self, other) -> bool:
        # triangle hitbox vs circle: center inside the triangle, or an edge within the radius
        a, b, c = self.triangle()
        p = other.position
        sides = [(v - u).cross(p - u) for u, v in ((a, b), (b, c), (c, a))]
        if all(s >= 0 for s in sides) or all(s <= 0 for s in sides):
            return True
        for u, v in ((a, b), (b, c), (c, a)):
            t = max(0, min(1, (p - u).dot(v - u) / (v - u).length_squared()))
            if p.distance_to(u + (v - u) * t) <= other.radius:
                return True
        return False

    def is_protected(self) -> bool:
        return self.invulnerable_timer > 0 or self.shield_timer > 0

    def respawn(self):
        self.position = pygame.Vector2(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.invulnerable_timer = constants.PLAYER_RESPAWN_INVULNERABLE_SECONDS

    def apply_powerup(self, kind: str):
        if kind == "shield":
            self.shield_timer = constants.POWERUP_DURATION_SECONDS
        elif kind == "speed":
            self.speed_timer = constants.POWERUP_DURATION_SECONDS
        
    def rotate(self, dt: float) -> float:
        self.rotation += constants.PLAYER_TURN_SPEED * dt
    
    def move(self, dt: float):
        boost = constants.SPEED_POWERUP_MULTIPLIER if self.speed_timer > 0 else 1
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * constants.PLAYER_ACCELERATION * boost * dt

    def shoot(self, dt: float):
        if self.shoot_timer > 0:
            return
        cooldown, speed, angles = constants.WEAPONS[self.weapon]
        self.shoot_timer = cooldown

        for angle in angles:
            plr_shot = shot.Shot(self.position.x, self.position.y)
            plr_shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation + angle) * speed

    def drop_bomb(self):
        if self.bombs > 0:
            self.bombs -= 1
            bomb.Bomb(self.position.x, self.position.y)

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)

        for key, name in zip((pygame.K_1, pygame.K_2, pygame.K_3), constants.WEAPONS):
            if keys[key]:
                self.weapon = name

        self.shoot_timer -= dt
        self.invulnerable_timer -= dt
        self.shield_timer -= dt
        self.speed_timer -= dt
        if keys[pygame.K_SPACE]:
            self.shoot(dt)

        self.velocity *= constants.PLAYER_DRAG ** dt
        max_speed = constants.PLAYER_MAX_SPEED * (constants.SPEED_POWERUP_MULTIPLIER if self.speed_timer > 0 else 1)
        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)
        self.position += self.velocity * dt
        self.wrap()
