import pygame
from circleshape import CircleShape # Assuming this is the correct path
# from player import Player # Avoiding direct import for now to prevent circular dependency

class PowerUp(pygame.sprite.Sprite, CircleShape):
    containers = None # Will be set in main.py

    def __init__(self, x, y, radius, color, powerup_type, duration):
        pygame.sprite.Sprite.__init__(self) # Initialize Sprite part
        CircleShape.__init__(self, x, y, radius) # Initialize CircleShape part
        
        self.image = pygame.Surface([radius*2, radius*2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x,y))
        
        self.color = color # Kept for potential direct drawing or reference
        self.powerup_type = powerup_type
        self.duration = duration

        # Add to groups if containers are set
        if PowerUp.containers:
            self.add(PowerUp.containers)

    def draw(self, screen):
        # This method might be redundant if self.image is used by a sprite group's draw method.
        # However, CircleShape's draw method might be different or more detailed.
        # For now, relying on group.draw() using self.image and self.rect.
        # If specific drawing is needed, this can be uncommented or Group.draw can be replaced.
        # pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)
        pass


    def apply_effect(self, player):
        # player argument will be an instance of the Player class
        raise NotImplementedError("Subclasses must implement this method.")

    def update(self, dt):
        # Keep rect synced with position if position can change (e.g., moving power-ups)
        self.rect.center = (int(self.position.x), int(self.position.y))
        # Other update logic for the power-up item itself (e.g., animation, lifetime) can go here.

class RapidFirePowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, radius=10, color=(0, 255, 0), powerup_type="rapid_fire", duration=5.0) # Green, 5 seconds

    def apply_effect(self, player):
        # This method will be called when the player collects the power-up.
        # It directly modifies the player object passed to it.
        # The Player class will need 'shoot_cooldown_multiplier' and 'powerup_timer' attributes.
        print(f"Applying {self.powerup_type} to player for {self.duration}s. Current player cooldown multiplier: {getattr(player, 'shoot_cooldown_multiplier', 'N/A')}")
        player.shoot_cooldown_multiplier = 0.5 # Example: Halves the cooldown
        player.powerup_timer = self.duration # Player needs to handle this timer
        player.active_powerup_type = self.powerup_type
        player.active_powerup_color = self.color # Set player's active color
        print(f"Set player.shoot_cooldown_multiplier to 0.5, player.powerup_timer to {self.duration}, player.active_powerup_type to {self.powerup_type}, player.active_powerup_color to {self.color}")


class ShieldPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            radius=12,
            color=(0, 0, 255),
            powerup_type="shield",
            duration=5.0,
        )

    def apply_effect(self, player):
        print(f"Applying {self.powerup_type} to player for {self.duration}s.")
        player.shield_active = True
        player.powerup_timer = self.duration
        player.active_powerup_type = self.powerup_type
        player.active_powerup_color = self.color


class SpreadShotPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            radius=12,
            color=(255, 165, 0),
            powerup_type="spread_shot",
            duration=5.0,
        )

    def apply_effect(self, player):
        print(f"Applying {self.powerup_type} to player for {self.duration}s.")
        player.spread_shot_active = True
        player.powerup_timer = self.duration
        player.active_powerup_type = self.powerup_type
        player.active_powerup_color = self.color
