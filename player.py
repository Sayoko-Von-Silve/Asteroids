import pygame, random
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_SPEED, PLAYER_TURN_SPEED, PLAYER_SHOOT_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH
from circleshape import CircleShape
from shot import Shot, Bolt, Flak

class Player(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 180
        self.shoot_cooldown = 0.0
        self.invuln_timer = 3
        self.god_mode = False
        self.infinite_ammo = False
        self.inputdelay = 0
        self.weapon_mode = ["Plasma Buster", 0]
        self.weapon_ammo = 0
        self.pylon_gun_switch = 1
        self.pylon_palette = [("aquamarine4", "aquamarine3"), #plasma_buster - Perfect.
                              ("turquoise4", "turquoise3"), #pulse_cannon - different color scheme for shots desired.
                              ("powderblue", "seagreen1"), #shard_blaster - Shot needs to be made different, to differentiate from standard.
                              ("silver", "orangered3"), #bolt_caster - Bolts are good, pylons need to be a little different in color.
                              ("darkred", "darkviolet"), #flak_pulsar - I'd like to overhaul the weapon more, give it some pulsating and longevity.
                              ("white", "fuschia"), #seeker_discs; not implemented yet, color scheme is to represent undecided in the future.
                              ]
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
    
    def triangle_godmode_outline(self, scale: float = 1.15) -> list[pygame.Vector2]:
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

    def use_weapon(self):
        if self.weapon_mode[1] == 0:
            self.plasma_buster()
        elif self.weapon_mode[1] == 1:
            self.pulse_cannon()
        elif self.weapon_mode[1] == 2:
            self.shard_blaster()
        elif self.weapon_mode[1] == 3:
            self.bolt_caster()
        elif self.weapon_mode[1] == 4:
            self.flak_pulsar()
        #elif self.weapon_mode == 5:
        #    self.seeker_discs()

    def plasma_buster(self):
        if self.shoot_cooldown > 0:
            return
        self.shoot_cooldown = 0.3
        if self.pylon_gun_switch == 1:
            muzzle = self.triangle_pylonright()[0]
            self.pylon_gun_switch = 0
        else:
            muzzle = self.triangle_pylonleft()[0]
            self.pylon_gun_switch = 1
        shot = Shot(muzzle.x, muzzle.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def pulse_cannon(self):
        if self.weapon_ammo < 1 and self.infinite_ammo == False:
            return
        if self.shoot_cooldown > 0:
            return
        self.shoot_cooldown = 0.05
        if not self.infinite_ammo:
            self.weapon_ammo -= 1
            if self.weapon_ammo < 0:
                self.weapon_ammo = 0
        if self.pylon_gun_switch == 1:
            muzzle = self.triangle_pylonright()[0]
            self.pylon_gun_switch = 0
        else:
            muzzle = self.triangle_pylonleft()[0]
            self.pylon_gun_switch = 1
        shot = Shot(muzzle.x, muzzle.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED * 1.2

    def shard_blaster(self):
        if self.weapon_ammo < 1 and self.infinite_ammo == False:
            return
        if self.shoot_cooldown > 0:
            return
        self.shoot_cooldown = 0.7
        if not self.infinite_ammo:
            self.weapon_ammo -= 2
            if self.weapon_ammo < 0:
                self.weapon_ammo = 0
        for i in range(0, 7):
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation - 15 + (i * 5)) * PLAYER_SHOOT_SPEED * (random.randint(70, 100)/100)

    def bolt_caster(self):
        if self.weapon_ammo < 1 and self.infinite_ammo == False:
            return
        if self.shoot_cooldown > 0:
            return
        self.shoot_cooldown = 0.8
        if not self.infinite_ammo:
            self.weapon_ammo -= 3
            if self.weapon_ammo < 0:
                self.weapon_ammo = 0
        shot = Bolt(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED * 1.5

    def flak_pulsar(self):
        if self.weapon_ammo < 1 and self.infinite_ammo == False:
            return
        if self.shoot_cooldown > 0:
            return
        self.shoot_cooldown = 1
        if not self.infinite_ammo:
            self.weapon_ammo -= 3
            if self.weapon_ammo < 0:
                self.weapon_ammo = 0
        shot = Flak(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED * 0.75

    #def seeker_discs(self):
    #    pass

    def draw(self, screen: pygame.Surface):
        keys = pygame.key.get_pressed()
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        shield_center = self.position - forward * (self.radius * 0.4)

        #when godmode is on, draw godmode outline.
        if self.god_mode:
            pygame.draw.polygon(screen, "goldenrod2", self.triangle_godmode_outline(), LINE_WIDTH + 3)
            pygame.draw.polygon(screen, "goldenrod1", self.triangle_pylonright(0.55), LINE_WIDTH * 2)
            pygame.draw.polygon(screen, "goldenrod1", self.triangle_pylonleft(0.55), LINE_WIDTH * 2)
            pygame.draw.polygon(screen, "goldenrod2", self.triangle_wingright(0.75), LINE_WIDTH * 2)
            pygame.draw.polygon(screen, "goldenrod2", self.triangle_wingleft(0.75), LINE_WIDTH * 2)

        #when reversing, draw both reverse flames.
        if keys [pygame.K_s]:
            pygame.draw.polygon(screen, "crimson", self.triangle_left_flame(), 0)
            pygame.draw.polygon(screen, "crimson", self.triangle_right_flame(), 0)

        #when turning left, draw right flame.
        if keys [pygame.K_a]:
            pygame.draw.polygon(screen, "crimson", self.triangle_right_flame(), 0)

        #when turning right, draw left flame.
        if keys [pygame.K_d]:
            pygame.draw.polygon(screen, "crimson", self.triangle_left_flame(), 0)

        #draw ship thruster/gun pylons
        wm = self.weapon_mode[1]
        color1, color2 = self.pylon_palette[wm][0], self.pylon_palette[wm][1]
        pygame.draw.polygon(screen, color1, self.triangle_pylonright(0.5), 0)
        pygame.draw.polygon(screen, color1, self.triangle_pylonleft(0.5), 0)
        pygame.draw.polygon(screen, color2, self.triangle_pylonright(), 0)
        pygame.draw.polygon(screen, color2, self.triangle_pylonleft(), 0)

        #Draw right wing and its boarder, then left wing and its boarder,
        #then ship on top of wings, then cockpit on top of the ship, 
        #then apply a silver boarder around the ship.
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

    def toggle_infinite_ammo(self):
        if self.infinite_ammo == False:
            self.infinite_ammo = True
        else:
            self.infinite_ammo = False


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
            self.use_weapon()

        #temporary???
        if keys[pygame.K_1]:
            self.weapon_mode = ["Plasma Buster", 0]
        if keys[pygame.K_2]:
            self.weapon_mode = ["Pulse Cannon", 1]
        if keys[pygame.K_3]:
            self.weapon_mode = ["Shard Blaster", 2]
        if keys[pygame.K_4]:
            self.weapon_mode = ["Bolt Caster", 3]
        if keys[pygame.K_5]:
            self.weapon_mode = ["Flak Pulsar", 4]
        #if keys[pygame.K_6]:
        #    self.weapon = 5