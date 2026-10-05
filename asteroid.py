import circleshape, pygame, random
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event

class Asteroid(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, surface: pygame.Surface, color = "white") -> None:
        pygame.draw.circle(surface, color, (int(self.position.x), int(self.position.y)), self.radius, LINE_WIDTH)

    def split(self) -> None:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            ast1 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
            ast2 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
            ast1.velocity = self.velocity.rotate(random.uniform(20, 50) * 1.2)
            ast2.velocity = self.velocity.rotate(random.uniform(20, -50) * 1.2)
            return


    def update(self, dt: float) -> None:
        self.position += self.velocity * dt