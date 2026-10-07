import circleshape, pygame, random
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_event

class Asteroid(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, surface: pygame.Surface, color = "slategray3") -> None:
        pygame.draw.circle(surface, color, (int(self.position.x), int(self.position.y)), self.radius, LINE_WIDTH)

    def split(self) -> int:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return 3
        elif self.radius <= ASTEROID_MIN_RADIUS * 2:
            log_event("asteroid_split")
            ast1 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
            ast2 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
            ast1.velocity = self.velocity.rotate(random.uniform(20, 50) * 1.2)
            ast2.velocity = self.velocity.rotate(random.uniform(20, -50) * 1.2)
            return 2
        else:
            log_event("asteroid_split")
            ast1 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
            ast2 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
            ast1.velocity = self.velocity.rotate(random.uniform(20, 50) * 1.2)
            ast2.velocity = self.velocity.rotate(random.uniform(20, -50) * 1.2)
            return 1


    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.boundary_check(SCREEN_WIDTH, SCREEN_HEIGHT)