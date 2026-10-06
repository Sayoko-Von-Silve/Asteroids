import sys
import pygame
from constants import *
from player import Player
from logger import log_state, log_event
from asteroid import *
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}, Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0
    score = 0
    lives = 3
    score_font = pygame.font.SysFont("Arial", 24)
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable)
    astfield = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)

    while True:
        log_state()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # update game state
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player) and player.invuln_timer <= 0:
                log_event("player_hit")
                player.kill()
                score -= asteroid.split() * 10
                lives -= 1
                if lives <= 0:
                    print("Game Over!")
                    if score < 0:
                        score = 0
                    print(f"Final Score: {score}")
                    sys.exit()
                player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)
                break
            if asteroid.collides_with(player) and player.invuln_timer > 0:
                score += asteroid.split()
                break
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    score += asteroid.split()
                    shot.kill()
                    break

        # update graphic state
        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)


        # draw score
        score_text = score_font.render(f"SCORE: [{score}]", True, "lightcoral")
        lives_text = score_font.render(f"[{lives}] :LIVES", True, "lightcoral")
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

        pygame.display.flip()

        dt = clock.tick(60) / 1000







if __name__ == "__main__":
    main()