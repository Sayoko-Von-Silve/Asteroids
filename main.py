import sys
import pygame
from constants import *
from player import Player
from logger import log_state, log_event
from asteroid import *
from asteroidfield import AsteroidField
from shot import Shot, Bolt, Flak, Shrapnel
from powerups import PowerUp

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}, Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = pygame.image.load("assets/modified_nebula.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0.0
    game_time = 0.0
    minutes, seconds = 0, 0
    score = 0
    lives = 3
    score_font = pygame.font.SysFont("Arial", 24)
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    asteroidfield = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)
    Bolt.containers = (shots, updatable, drawable)
    Flak.containers = (shots, updatable, drawable)
    Shrapnel.containers = (shots, updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                player.toggle_god_mode()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F2:
                player.toggle_infinite_ammo()

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
                if player.infinite_ammo == True:
                    carryover_inf = 1
                    carryover_gun = player.weapon_mode
                player.kill()
                score -= asteroid.split() * 10
                player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_RADIUS)
                if carryover_inf == 1:
                    player.infinite_ammo = True
                    carryover_inf = 0
                    player.weapon_mode = carryover_gun
                break
            if asteroid.collides_with(player) and player.invuln_timer > 0 and player.god_mode == False:
                score += asteroid.split()
                break
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    if shot.__class__ == Shot:
                        shot.kill()
                        score += asteroid.split()
                    elif shot.__class__ == Bolt:
                        shot.lifetime -= 1.2
                        shot.splinter = True
                        score += asteroid.split()
                    elif shot.__class__ == Flak:
                        shot.lifetime = 0
                        score += asteroid.split()
                    elif shot.__class__ == Shrapnel:
                        shot.kill()
                        score += asteroid.split()
                    break

        for powerup in powerups:
            if powerup.collides_with(player):
                if powerup.type == "Life":
                    powerup.kill()
                    lives += 1
                    break
                elif powerup.type == "Shield":
                    powerup.kill()
                    player.invuln_timer += 10
                    break
                elif powerup.type == "Ammo":
                    powerup.kill()
                    player.weapon_ammo += 100
                    pass

        # update graphic state
        screen.blit(background, (0, 0))
        for obj in drawable:
            if obj != player:
                obj.draw(screen)
        player.draw(screen)


        # draw score, lives, and time
        score_text = score_font.render(f"SCORE: [{score}]", True, "firebrick2")
        lives_text = score_font.render(f"[{lives}] :LIVES", True, "firebrick2")
        time_text = score_font.render(f"[{minutes:02}:{seconds:02}]", True, "firebrick3")
        if player.weapon_mode[1] == 0:
            weapon_text = score_font.render(f"WEAPON: {player.weapon_mode[0]}", True, "firebrick3")
        else:
            weapon_text = score_font.render(f"WEAPON: {player.weapon_mode[0]}, AMMO: {player.weapon_ammo}", True, "firebrick3")
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))
        screen.blit(time_text, ((SCREEN_WIDTH - time_text.get_width()) // 2, 10))
        screen.blit(weapon_text, (SCREEN_WIDTH - weapon_text.get_width() - 10, SCREEN_HEIGHT - weapon_text.get_height() - 10))

        pygame.display.flip()

        dt = clock.tick(60) / 1000
        game_time += dt
        minutes, seconds = divmod(int(game_time), 60)



if __name__ == "__main__":
    main()