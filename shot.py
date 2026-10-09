import circleshape
import pygame
from constants import SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT, SHOT_SPEED_MULTIPLIER

class Shot(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float = SHOT_RADIUS) -> None:
        super().__init__(x, y, radius)
        self.lifetime = 2.0 # seconds

    def draw(self, surface: pygame.Surface, color = "white") -> None:
        pygame.draw.circle(surface, "aquamarine2", (int(self.position.x), int(self.position.y)), self.radius)
        pygame.draw.circle(surface, "magenta", (int(self.position.x), int(self.position.y)), self.radius - 2)

    def update(self, dt: float) -> None:
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        self.position += self.velocity * SHOT_SPEED_MULTIPLIER * dt
        self.boundary_check(SCREEN_WIDTH, SCREEN_HEIGHT)