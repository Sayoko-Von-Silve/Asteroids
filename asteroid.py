import circleshape, pygame
from constants import LINE_WIDTH

class Asteroid(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, surface: pygame.Surface, color = "white") -> None:
        pygame.draw.circle(surface, color, (int(self.position.x), int(self.position.y)), self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt