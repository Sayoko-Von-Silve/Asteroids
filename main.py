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
    background = pygame.image.load("assets/modified_nebula.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0
    score = 0
    lives = 3
    score_font = pygame.font.SysFont("Arial", 24)
    shots = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    asteroidfield = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (asteroidfield)
    astfield = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)

    while True:
        log_state()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP1:
                player.toggle_god_mode()

        # update game state
        asteroidfield.update(dt, score, len(asteroids))
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player) and player.invuln_timer <= 0 and player.god_mode == False:
                log_event("player_hit")
                lives -= 1
                if lives <= 0:
                    print("Game Over!")
                    if score < 0:
                        score = 0
                    print(f"Final Score: {score}")
                    sys.exit()
                player.kill()
                score -= asteroid.split() * 10
                player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)
                break
            if asteroid.collides_with(player) and player.invuln_timer > 0 and player.god_mode == False:
                score += asteroid.split()
                break
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    score += asteroid.split()
                    break

        # update graphic state
        screen.blit(background, (0, 0))
        for obj in drawable:
            if obj != player:
                obj.draw(screen)
        player.draw(screen)


        # draw score
        score_text = score_font.render(f"SCORE: [{score}]", True, "lightcoral")
        lives_text = score_font.render(f"[{lives}] :LIVES", True, "lightcoral")
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

        pygame.display.flip()

        dt = clock.tick(60) / 1000







if __name__ == "__main__":
    main()