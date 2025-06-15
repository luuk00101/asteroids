import pygame
from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN,
    PLAYER_SHOOT_SPEED,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from shot import Shot


class Player(pygame.sprite.Sprite, CircleShape):
    containers = None # Will be set in main.py

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        CircleShape.__init__(self, x, y, PLAYER_RADIUS)
        
        self.image = pygame.Surface([self.radius*2, self.radius*2], pygame.SRCALPHA)
        # The actual drawing of the triangle for display will be handled by the draw() method
        # For sprite collision, a circle matching PLAYER_RADIUS is appropriate.
        # We can draw a visible circle on self.image for debugging or use a transparent one.
        pygame.draw.circle(self.image, (255, 255, 255, 0), (self.radius, self.radius), self.radius) # Transparent for collision
        self.rect = self.image.get_rect(center=(x,y))
        
        self.rotation = 0
        self.timer = 0 # For shooting cooldown

        self.shoot_cooldown_multiplier = 1.0 # 1.0 means normal cooldown
        self.powerup_timer = 0.0 # Duration for active power-up
        self.active_powerup_type = None
        self.active_powerup_color = None # For visual indicator
        self.shield_active = False
        self.spread_shot_active = False

        # Add to groups if containers are set
        if Player.containers:
            self.add(Player.containers)

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius  # type: ignore
        b = self.position - forward * self.radius - right  # type: ignore
        c = self.position - forward * self.radius + right  #  type: ignore
        return [a, b, c]

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        current_shoot_cooldown = PLAYER_SHOOT_COOLDOWN * self.shoot_cooldown_multiplier
        if self.timer <= 0:
            angles = [0]
            if self.spread_shot_active:
                angles = [-15, 0, 15]
            for a in angles:
                new_shot = Shot(self.position.x, self.position.y)
                new_shot.velocity = (
                    pygame.Vector2(0, 1).rotate(self.rotation + a) * PLAYER_SHOOT_SPEED
                )
            self.timer = current_shoot_cooldown

    def draw(self, screen):
        # This manual draw is for the triangle.
        # The self.image for sprite group drawing is just a circle for collision.
        # If we wanted the triangle to be on self.image, we'd render it there.
        current_draw_color = self.active_powerup_color if self.active_powerup_color else "white"
        pygame.draw.polygon(screen, current_draw_color, self.triangle(), 2)
        if self.shield_active:
            pygame.draw.circle(screen, "blue", (int(self.position.x), int(self.position.y)), self.radius + 5, 1)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        self.timer -= dt

        # Screen wrap-around
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT

        self.rect.center = (int(self.position.x), int(self.position.y))  # Keep rect synced

        # Power-up timer update
        if self.powerup_timer > 0:
            self.powerup_timer -= dt
            if self.powerup_timer <= 0:
                print(f"Power-up {self.active_powerup_type} expired.")
                if self.active_powerup_type == "rapid_fire":
                    self.shoot_cooldown_multiplier = 1.0
                elif self.active_powerup_type == "shield":
                    self.shield_active = False
                elif self.active_powerup_type == "spread_shot":
                    self.spread_shot_active = False
                self.active_powerup_type = None
                self.active_powerup_color = None
                self.powerup_timer = 0.0
