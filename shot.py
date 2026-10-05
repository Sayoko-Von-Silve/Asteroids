import circleshape
import pygame
from constants import SHOT_RADIUS

class Shot(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float = SHOT_RADIUS) -> None:
        super().__init__(x, y, radius)

    def draw(self, surface: pygame.Surface, color = "white"):
        pygame.draw.circle(surface, color, (int(self.position.x), int(self.position.y)), self.radius)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt