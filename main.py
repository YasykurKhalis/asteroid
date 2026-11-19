import random
import pygame
import constants
from logger import log_state, log_event
import player
import asteroid
import asteroidfield
import sys
import shot
import bomb
import powerup
import explosion

def make_background() -> pygame.Surface:
    size = (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    try:
        return pygame.transform.scale(pygame.image.load("background.png").convert(), size)
    except (FileNotFoundError, pygame.error):
        # no image provided, draw a starfield instead
        background = pygame.Surface(size)
        for _ in range(200):
            shade = random.randint(60, 200)
            background.set_at((random.randrange(size[0]), random.randrange(size[1])), (shade, shade, shade))
        return background

def main():
    pygame.init()

    print(f"Starting Asteroids")
    print(f"Screen width: {constants.SCREEN_WIDTH}")
    print(f"Screen height: {constants.SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    background = make_background()
    font = pygame.font.Font(None, 32)

    clock = pygame.time.Clock()
    dt = 0.0
    score = 0
    lives = constants.PLAYER_LIVES
    powerup_timer = 0.0

    updatable = pygame.sprite.Group() 
    drawable = pygame.sprite.Group()

    player.Player.containers = {updatable, drawable}
    plr = player.Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)

    asteroids = pygame.sprite.Group()
    asteroid.Asteroid.containers = {asteroids, updatable, drawable}
    
    asteroidfield.AsteroidField.containers = {updatable}
    asteroidfield.AsteroidField(asteroids)

    shots = pygame.sprite.Group()
    shot.Shot.containers = {shots, drawable, updatable}

    bombs = pygame.sprite.Group()
    bomb.Bomb.containers = {bombs, drawable, updatable}

    powerups = pygame.sprite.Group()
    powerup.PowerUp.containers = {powerups, drawable, updatable}

    explosion.Particle.containers = {drawable, updatable}

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                plr.drop_bomb()

        screen.blit(background, (0, 0))

        updatable.update(dt)

        powerup_timer += dt
        if powerup_timer > constants.POWERUP_SPAWN_RATE_SECONDS:
            powerup_timer = 0
            powerup.PowerUp(
                random.uniform(50, constants.SCREEN_WIDTH - 50),
                random.uniform(50, constants.SCREEN_HEIGHT - 50),
                random.choice(list(powerup.PowerUp.COLORS)),
            )

        for item in powerups:
            if plr.collides_with(item):
                log_event("powerup", kind=item.kind)
                plr.apply_powerup(item.kind)
                item.kill()

        if not plr.is_protected():
            for asteroid_thing in asteroids:
                if plr.collides_with(asteroid_thing):
                    log_event("player_hit")
                    lives -= 1
                    if lives == 0:
                        print(f"Game over! Score: {score}")
                        sys.exit()
                    explosion.explode(plr.position, 30)
                    plr.respawn()
                    break

        for asteroid_thing in asteroids:
            for one_shot in shots:
                if one_shot.collides_with(asteroid_thing):
                    log_event("asteroid_shot")
                    score += asteroid_thing.points()
                    asteroid_thing.split()
                    one_shot.kill()
                    break

        for one_bomb in bombs:
            if one_bomb.fuse <= 0:
                log_event("bomb_exploded")
                one_bomb.radius = constants.BOMB_BLAST_RADIUS
                explosion.explode(one_bomb.position, 60)
                for asteroid_thing in asteroids:
                    if one_bomb.collides_with(asteroid_thing):
                        score += asteroid_thing.points()
                        asteroid_thing.kill()
                one_bomb.kill()

        for draw_thing in drawable:
            draw_thing.draw(screen)

        hud = f"Score {score}   Lives {lives}   Bombs {plr.bombs}   Weapon {plr.weapon} (1-3)"
        screen.blit(font.render(hud, True, "white"), (10, 10))

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
