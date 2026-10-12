import circleshape, random
import pygame
from constants import SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT, SHOT_SPEED_MULTIPLIER, PLAYER_SHOOT_SPEED

class Shot(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float = SHOT_RADIUS) -> None:
        super().__init__(x, y, radius)
        self.lifetime = 2.0 # seconds

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, "aquamarine2", (int(self.position.x), int(self.position.y)), self.radius)
        pygame.draw.circle(surface, "magenta", (int(self.position.x), int(self.position.y)), self.radius - 2)

    def update(self, dt: float) -> None:
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        self.position += self.velocity * SHOT_SPEED_MULTIPLIER * dt
        self.boundary_check(SCREEN_WIDTH, SCREEN_HEIGHT)

class Shrapnel(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float = SHOT_RADIUS - 2) -> None:
        super().__init__(x, y, radius)
        self.lifetime = 1.0 # seconds

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, "crimson", (int(self.position.x), int(self.position.y)), self.radius)
        pygame.draw.circle(surface, "purple", (int(self.position.x), int(self.position.y)), self.radius - 2)

    def update(self, dt: float) -> None:
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        self.position += self.velocity * SHOT_SPEED_MULTIPLIER * dt
        self.boundary_check(SCREEN_WIDTH, SCREEN_HEIGHT)

class Bolt(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float = (SHOT_RADIUS - 2)) -> None:
        super().__init__(x, y, radius)
        self.rotation = 180
        self.lifetime = 10.0 # seconds
        self.splinter = False

    def draw(self, surface: pygame.Surface) -> None:
        direction = self.velocity.normalize()
        side = direction.rotate(90)
        length = self.radius * 4
        width = self.radius * 0.6
        front = self.position + direction * length
        back = self.position - direction * length

        a = front + side * width
        b = front - side * width
        c = back - side * width
        d = back + side * width

        pygame.draw.polygon(surface, "orangered", [a,b,c,d], int(self.radius) + 2)
        pygame.draw.polygon(surface, "silver", [a,b,c,d], 0)

    def update(self, dt: float) -> None:
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        if self.splinter:
            self.splinter = False
            for i in range(0, random.randint(0, 3)):
                shrapnel = Shrapnel(self.position.x, self.position.y)
                shrapnel.lifetime = 0.5
                shrapnel.velocity = pygame.Vector2(0, 1).rotate(self.rotation + random.randint(0, 360)) * PLAYER_SHOOT_SPEED * (random.randint(10, 30)/100)
        self.position += self.velocity * SHOT_SPEED_MULTIPLIER * dt
        self.boundary_check(SCREEN_WIDTH, SCREEN_HEIGHT)

class Flak(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float = SHOT_RADIUS * 2) -> None:
        super().__init__(x, y, radius)
        self.rotation = 180
        self.lifetime = 0.8 # seconds

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, "crimson", (int(self.position.x), int(self.position.y)), self.radius)
        pygame.draw.circle(surface, "purple", (int(self.position.x), int(self.position.y)), self.radius - 2)

    def update(self, dt: float) -> None:
        self.lifetime -= dt
        if self.lifetime <= 0:
            for i in range(1, random.randint(12, 19)):
                shrapnel = Shrapnel(self.position.x, self.position.y)
                shrapnel.velocity = pygame.Vector2(0, 1).rotate(self.rotation + i * random.randint(20, 30)) * PLAYER_SHOOT_SPEED * (random.randint(75, 125)/100)
            self.kill()
        self.position += self.velocity * SHOT_SPEED_MULTIPLIER * dt
        self.boundary_check(SCREEN_WIDTH, SCREEN_HEIGHT)