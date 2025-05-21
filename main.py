import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import sys
from pause_menu import PauseMenu


def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initilize the "control pobjects"
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    ateroid_field = AsteroidField()
    pause_menu = PauseMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
    resume_rect = None
    quit_rect = None

    # Initilize the clock and delta time (for proper rendering)
    clock = pygame.time.Clock()
    dt = 0
    paused = False

    # Main game loop
    while True:
        # Allows to actually interact and exit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if not paused: # Reset rects when unpausing
                        resume_rect, quit_rect = None, None
                elif paused: # Only process these if already paused
                    if event.key == pygame.K_r:
                        paused = False
                        resume_rect, quit_rect = None, None # Reset rects
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit() # Quit game
            
            if paused and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if resume_rect and resume_rect.collidepoint(mouse_pos):
                        paused = False
                        resume_rect, quit_rect = None, None # Reset rects
                    elif quit_rect and quit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

        # Fill the background
        screen.fill("#000000")

        if not paused:
            for asteroid in asteroids:
                if asteroid.check_collision(player):
                    print("Game over!")
                    pygame.quit()
                    sys.exit()
                for shot in shots:
                    if asteroid.check_collision(shot):
                        shot.kill()
                        asteroid.split()
            for sprite in updatable:
                sprite.update(dt)
        
        for sprite in drawable:
            sprite.draw(screen)

        if paused:
            # Create a semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Black with 50% alpha (0-255)
            screen.blit(overlay, (0, 0))
            resume_rect, quit_rect = pause_menu.draw(screen)

        # Actually render the screen (limit 60 FPS)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
