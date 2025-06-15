import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # Add to sprite groups only if containers are set
        containers = getattr(self, "containers", None)
        if containers:
            super().__init__(containers)  # type: ignore
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def check_collision(self, other):
        distance = self.position.distance_to(other.position)
        return distance <= (self.radius + other.radius)
