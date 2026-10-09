import pygame, random
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_SPEED, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS, SCREEN_HEIGHT, SCREEN_WIDTH
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 180
        self.shoot_cooldown = 0
        self.invuln_timer = 3
        self.god_mode = False
        self.inputdelay = 0
        self.pylon_gun_switch = 1
        self.rng_flame = 0
        self.rng_timer = 0

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def triangle_cockpit(self, scale: float = 0.3) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shift = forward * (self.radius * 0.1)
        return [(self.position + (point - self.position) * scale ) + shift for point in self.triangle()]
    
    def triangle_pylonright(self, scale: float = 0.35) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation + 45)
        shift = forward * (self.radius * 0.55)
        return [(self.position + (point - self.position) * scale ) + shift for point in self.triangle()]

    def triangle_pylonleft(self, scale: float = 0.35) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation - 45)
        shift = forward * (self.radius * 0.55)
        return [(self.position + (point - self.position) * scale ) + shift for point in self.triangle()]
    
    def triangle_wingright(self, scale: float = 0.55) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = forward.rotate(90)
        side_shift = forward * (self.radius * -1) + right * (self.radius * 0.7)
        return [self.position + (-(point - self.position) * scale).rotate(-45) + side_shift for point in self.triangle()]
    
    def triangle_wingleft(self, scale: float = 0.55) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = forward.rotate(90)
        side_shift = forward * (self.radius * -1) - right * (self.radius * 0.7)
        return [self.position + (-(point - self.position) * scale).rotate(45) + side_shift for point in self.triangle()]
    
    def triangle_forward_flame(self, scale: float = 0.5) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shift = forward * (self.radius * -1.7)
        return [(self.position - (point - self.position) * scale ) + shift for point in self.triangle()]

    def triangle_right_flame(self, scale: float = 0.25) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = forward.rotate(90)
        side_shift = forward * (self.radius * 0.2) + right * (self.radius * 0.7)
        return [self.position + (-(point - self.position) * scale).rotate(-60) + side_shift for point in self.triangle()]
    
    def triangle_left_flame(self, scale: float = 0.25) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = forward.rotate(90)
        side_shift = forward * (self.radius * 0.2) - right * (self.radius * 0.7)
        return [self.position + (-(point - self.position) * scale).rotate(60) + side_shift for point in self.triangle()]
    
    def triangle_godmode_overlay(self, scale: float = 1.15) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shift = forward * (self.radius * 0.07)

        return ([(self.position + (point - self.position) * scale ) + shift for point in self.triangle()])

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
        if self.pylon_gun_switch == 1:
            muzzle = self.triangle_pylonright()[0]
            self.pylon_gun_switch = 0
        else:
            muzzle = self.triangle_pylonleft()[0]
            self.pylon_gun_switch = 1
        shot = Shot(muzzle.x, muzzle.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def draw(self, screen: pygame.Surface):
        keys = pygame.key.get_pressed()
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shield_center = self.position - forward * (self.radius * 0.4)

        # when godmode is on, draw godmode overlay.
        if self.god_mode:
            pygame.draw.polygon(screen, "goldenrod2", self.triangle_godmode_overlay(), LINE_WIDTH + 3)
            pygame.draw.polygon(screen, "goldenrod1", self.triangle_pylonright(0.55), LINE_WIDTH * 2)
            pygame.draw.polygon(screen, "goldenrod1", self.triangle_pylonleft(0.55), LINE_WIDTH * 2)
            pygame.draw.polygon(screen, "goldenrod2", self.triangle_wingright(0.75), LINE_WIDTH * 2)
            pygame.draw.polygon(screen, "goldenrod2", self.triangle_wingleft(0.75), LINE_WIDTH * 2)

        # when reverseing, draw both reverse flames.
        if keys [pygame.K_s]:
            pygame.draw.polygon(screen, "crimson", self.triangle_left_flame(), 0)
            pygame.draw.polygon(screen, "crimson", self.triangle_right_flame(), 0)

        # when turning left, draw right flame.
        if keys [pygame.K_a]:
            pygame.draw.polygon(screen, "crimson", self.triangle_right_flame(), 0)

        # when turning right, draw left flame.
        if keys [pygame.K_d]:
            pygame.draw.polygon(screen, "crimson", self.triangle_left_flame(), 0)

        #draw ship thruster/gun pylons, then right wing and its boarder, then left wing and its boarder,
        #then ship on top of wings, then cockpit on top of ship, then apply a silver boarder around the ship.
        pygame.draw.polygon(screen, "aquamarine4", self.triangle_pylonright(0.5), 0)
        pygame.draw.polygon(screen, "aquamarine4", self.triangle_pylonleft(0.5), 0)
        pygame.draw.polygon(screen, "aquamarine3", self.triangle_pylonright(), 0)
        pygame.draw.polygon(screen, "aquamarine3", self.triangle_pylonleft(), 0)
        pygame.draw.polygon(screen, "slategray4", self.triangle_wingright(), 0)
        pygame.draw.polygon(screen, "silver", self.triangle_wingright(), LINE_WIDTH + 1)
        pygame.draw.polygon(screen, "slategray4", self.triangle_wingleft(), 0)
        pygame.draw.polygon(screen, "silver", self.triangle_wingleft(), LINE_WIDTH + 1)
        pygame.draw.polygon(screen, "slategray4", self.triangle(), 0)
        pygame.draw.polygon(screen, "magenta", self.triangle_cockpit(), 0)
        pygame.draw.polygon(screen, "silver", self.triangle(), LINE_WIDTH + 1)

        # when moving forward, draw rear flame tail.
        if keys[pygame.K_w]:
            pygame.draw.polygon(screen, "crimson", self.triangle_forward_flame(), 0)
            if self.rng_flame == 1:
                pygame.draw.polygon(screen, "tomato1", self.triangle_forward_flame(), LINE_WIDTH)
            elif self.rng_flame == 2:
                pygame.draw.polygon(screen, "orangered1", self.triangle_forward_flame(), LINE_WIDTH)
            elif self.rng_flame == 3:
                pygame.draw.polygon(screen, "darkorange", self.triangle_forward_flame(), LINE_WIDTH)
            else:
                pygame.draw.polygon(screen, "gray10", self.triangle_forward_flame(), LINE_WIDTH + 1)


        if self.invuln_timer > 0 and int(self.invuln_timer * 5) % 2 == 0:
            pygame.draw.circle(screen, "purple", (int(shield_center.x), int(shield_center.y)), self.radius + 12, LINE_WIDTH)
        elif self.invuln_timer > 0:
            pygame.draw.circle(screen, "magenta", (int(shield_center.x), int(shield_center.y)), self.radius + 13, LINE_WIDTH)

    def toggle_god_mode(self):
        if self.god_mode == False:
            self.god_mode = True
        else:
            self.god_mode = False


    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        if self.shoot_cooldown < 0:
            self.shoot_cooldown = 0
        if self.invuln_timer > 0:
            self.invuln_timer -= dt
        if self.inputdelay > 0:
            self.inputdelay -= 1
        if self.rng_timer > 0:
            self.rng_timer -= 1
        if self.rng_timer == 0:
            self.rng_flame = random.choices([1, 2, 3, 4], weights=[1, 1, 1, 4], k=1)[0]
            self.rng_timer = 3



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