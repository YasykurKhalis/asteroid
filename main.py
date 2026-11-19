import pygame
import constants
from logger import log_state, log_event
import player
import asteroid
import asteroidfield
import sys
import shot

def main():
    pygame.init()

    print(f"Starting Asteroids")
    print(f"Screen width: {constants.SCREEN_WIDTH}")
    print(f"Screen height: {constants.SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0.0

    updatable = pygame.sprite.Group() 
    drawable = pygame.sprite.Group()

    player.Player.containers = {updatable, drawable}
    plr = player.Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)

    asteroids = pygame.sprite.Group()
    asteroid.Asteroid.containers = {asteroids, updatable, drawable}
    
    asteroidfield.AsteroidField.containers = {updatable}
    asteroidfield.AsteroidField()

    shots = pygame.sprite.Group()
    shot.Shot.containers = {shots, drawable, updatable}

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")

        updatable.update(dt)
        for asteroid_thing in asteroids:
            if asteroid_thing.collides_with(plr):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
        for draw_thing in drawable:
            draw_thing.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
