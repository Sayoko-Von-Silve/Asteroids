import circleshape, pygame, random
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_event

class Asteroid(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.asteroid_shape = self.asteroid_shape_constructor()
        self.crater_shape = self.crater_shape_constructor()
        palette = [("#71858A", "#394C52"),  ("#807B72", "#494640"), ("#A9A9A9", "#5C5C5C"), ("#B0B0B0", "#4D4D4D"), ("#C0C0C0", "#3F3F3F"),]
        self.fill_color, self.outline_color = random.choice(palette)
        self.rotation = random.uniform(0, 360)
        self.spin_speed = random.uniform(-90, 90)  # degrees per second

    def asteroid_shape_constructor(self) -> list[pygame.Vector2]:
        point_count = 15
        shape = []
        for index in range(point_count):
            spacing = 360 / point_count
            angle = index * spacing + random.uniform(-4, 4)
            offset = pygame.Vector2(1, 0).rotate(angle) * self.radius * random.uniform(0.5, 1.0)
            shape.append(offset)
        return shape

    def crater_shape_constructor(self) -> list[list[pygame.Vector2]]:
        craters = []
        crater_count = random.choices([0, 1, 2, 3, 4, 5], weights=[6, 5, 3, 2, 1, 1], k=1)[0]
        starting_angle = random.uniform(0, 360)
        for index in range(0, crater_count):
            angle = starting_angle + index * (360 / crater_count) + random.uniform(-30, 30)
            distance = random.uniform(0.05, 0.5) * self.radius
            crater_radius = random.uniform(self.radius * 0.05, self.radius * 0.25)
            crater_offset = pygame.Vector2(distance, 0).rotate(angle)

            point_count = random.randint(5, 7)
            shape = []
            for index2 in range(point_count):
                spacing = 360 / point_count
                angle = index2 * spacing + random.uniform(-4, 4)
                point = crater_offset + pygame.Vector2(1, 0).rotate(angle) * crater_radius * random.uniform(0.65, 1.0)
                shape.append(point)

            if crater_offset.length() + crater_radius < self.radius:
                craters.append(shape)
        return craters

    def draw(self, surface: pygame.Surface) -> None:
        rotated_shape = [point.rotate(self.rotation) for point in self.asteroid_shape]
        pygame.draw.polygon(surface, self.fill_color, [point + self.position for point in rotated_shape], 0)

        for crater_points in self.crater_shape:
            rotated_crater_shape = [point.rotate(self.rotation) for point in crater_points]
            pygame.draw.polygon(surface, self.outline_color, [point + self.position for point in rotated_crater_shape], 0)

        pygame.draw.polygon(surface, self.outline_color, [point + self.position for point in rotated_shape], LINE_WIDTH + 1)

    def split(self) -> int:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return 3
        elif self.radius <= ASTEROID_MIN_RADIUS * 2:
            log_event("asteroid_split")
            ast1 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
            ast2 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
            ast1.velocity = self.velocity.rotate(random.uniform(20, 50) * 1.2) * random.uniform(0.9, 1.5)
            ast2.velocity = self.velocity.rotate(random.uniform(20, -50) * 1.2) * random.uniform(0.9, 1.5)
            return 2
        else:
            log_event("asteroid_split")
            ast1 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
            ast2 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
            ast1.velocity = self.velocity.rotate(random.uniform(20, 50) * 1.2) * random.uniform(0.9, 1.5)
            ast2.velocity = self.velocity.rotate(random.uniform(20, -50) * 1.2) * random.uniform(0.9, 1.5)
            return 1


    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.rotation += self.spin_speed * dt
        self.boundary_check(SCREEN_WIDTH, SCREEN_HEIGHT)