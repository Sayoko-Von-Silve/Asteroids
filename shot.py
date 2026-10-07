import circleshape
import pygame
from constants import SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT, SHOT_SPEED_MULTIPLIER

class Shot(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float = SHOT_RADIUS) -> None:
        super().__init__(x, y, radius)
        self.lifetime = 2.0 # seconds

    def draw(self, surface: pygame.Surface, color = "magenta") -> None:
        pygame.draw.circle(surface, color, (int(self.position.x), int(self.position.y)), self.radius)

    def update(self, dt: float) -> None:
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        self.position += self.velocity * SHOT_SPEED_MULTIPLIER * dt
        self.boundary_check(SCREEN_WIDTH, SCREEN_HEIGHT)