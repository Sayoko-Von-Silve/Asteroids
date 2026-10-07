import pygame
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_SPEED, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, SCREEN_HEIGHT, SCREEN_WIDTH
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 180
        self.shoot_cooldown = 0
        self.invuln_timer = 3

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
        self.boundary_check(SCREEN_WIDTH, SCREEN_HEIGHT)

    def shoot(self):
        if self.shoot_cooldown > 0:
            return
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def draw(self, screen: pygame.Surface):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shield_center = self.position - forward * (self.radius * 0.1)
        pygame.draw.polygon(screen, "teal", self.triangle(), LINE_WIDTH)
        if self.invuln_timer > 0 and int(self.invuln_timer * 5) % 2 == 0:
            pygame.draw.circle(screen, "purple", (int(shield_center.x), int(shield_center.y)), self.radius + 6, LINE_WIDTH)
        elif self.invuln_timer > 0:
            pygame.draw.circle(screen, "magenta", (int(shield_center.x), int(shield_center.y)), self.radius + 7, LINE_WIDTH)

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        if self.shoot_cooldown < 0:
            self.shoot_cooldown = 0
        if self.invuln_timer > 0:
            self.invuln_timer -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()