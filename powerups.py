import circleshape, pygame, random
from constants import LINE_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT

class PowerUp(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.lifetime = 10.0
        self.rotation = 180
        self.type = "default"
        self.color1 = "black"
        self.color2 = "white"

    def powerup_shape_constructor(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1)
        right = pygame.Vector2(1, 0) * self.radius
        a = -forward * self.radius - right
        b = -forward * self.radius + right
        c = forward * self.radius + right
        d = forward * self.radius - right
        return [a, b, c, d]

    def powerup_type(self) -> None:
        if self.type == "default":
            self.type = random.choices(["Life", "Shield", "Overshield", "Ammo"], weights=[1, 2, 2, 4], k=1)[0]
            if self.type == "Life":
                self.lifetime = 8.0
                self.color1 = "slategray4"
                self.color2 = "silver"
            elif self.type == "Shield":
                self.lifetime = 10.0
                self.color1 = "deepskyblue4"
                self.color2 = "deepskyblue2"
            elif self.type == "Overshield":
                self.lifetime = 10.0
                self.color1 = "purple"
                self.color2 = "magenta"
            elif self.type == "Ammo":
                self.lifetime = 14.0
                self.color1 = "aquamarine4"
                self.color2 = "aquamarine3"
    
    def draw(self, surface: pygame.Surface) -> None:
        rotated_shape = [point.rotate(self.rotation) for point in self.powerup_shape_constructor()]
        pygame.draw.polygon(surface, self.color1, [point + self.position for point in rotated_shape], 0)
        pygame.draw.polygon(surface, self.color2, [point + self.position for point in rotated_shape], LINE_WIDTH)
    
    def update(self, dt: float) -> None:
        if self.type == "default":
            self.powerup_type()
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        self.position += self.velocity * dt
        self.rotation += 250 * dt
        self.boundary_check(SCREEN_WIDTH, SCREEN_HEIGHT)