import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import sys
import random # For power-up spawning chance
from pause_menu import PauseMenu
from powerup import RapidFirePowerUp, PowerUp # Import PowerUp for containers
import json
import os

SCORES_FILE = "scores.json"


def load_high_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_high_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)


def update_high_scores(scores, new_score, limit=5):
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:limit]
    save_high_scores(scores)
    return scores


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
    powerups_group = pygame.sprite.Group() # Power-ups group

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable # AsteroidField itself is updatable
    Shot.containers = (shots, updatable, drawable)
    PowerUp.containers = (powerups_group, updatable, drawable) # Assign containers for PowerUp

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField() # Creates initial asteroids which get added to groups
    pause_menu = PauseMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
    resume_rect = None
    quit_rect = None

    high_scores = load_high_scores()

    score = 0
    score_font = pygame.font.Font(None, 36)
    game_over_font = pygame.font.Font(None, 74)
    options_font = pygame.font.Font(None, 50)

    game_state = "PLAYING"

    # Initilize the clock and delta time (for proper rendering)
    clock = pygame.time.Clock()
    dt = 0
    paused = False

    # Main game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                        if not paused:
                            resume_rect, quit_rect = None, None
                    elif paused:
                        if event.key == pygame.K_r:
                            paused = False
                            resume_rect, quit_rect = None, None
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                if paused and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        if resume_rect and resume_rect.collidepoint(mouse_pos):
                            paused = False
                            resume_rect, quit_rect = None, None
                        elif quit_rect and quit_rect.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()
            
            elif game_state == "GAME_OVER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset game
                        score = 0
                        player.kill()
                        for a in asteroids: a.kill()
                        for s in shots: s.kill()
                        for p in powerups_group: p.kill() # Clear existing power-ups

                        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # Re-creates and adds to groups
                        asteroid_field.kill()  # Remove old asteroid field before creating a new one
                        asteroid_field = AsteroidField() # Re-creates and adds asteroids to groups
                        
                        paused = False
                        game_state = "PLAYING"
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        # Game logic and rendering
        screen.fill("#000000") # Fill background once

        if game_state == "PLAYING":
            if not paused:
                for asteroid in asteroids:
                    if asteroid.check_collision(player):
                        game_state = "GAME_OVER" # Change state instead of exiting
                        high_scores = update_high_scores(high_scores, score)
                        break # Exit collision check loop for this frame
                if game_state == "GAME_OVER": # Check again if collision changed state
                    continue # Skip rest of PLAYING logic for this frame

                for shot in shots: # This loop should not run if game_state became GAME_OVER
                    for asteroid in asteroids: # Need to iterate asteroids again for shot collision
                        if asteroid.check_collision(shot):
                            shot.kill()
                            asteroid.split()
                            score += 10
                            # Spawn power-up chance
                            if random.random() < 0.2: # 20% chance
                                # PowerUp class handles adding to groups via PowerUp.containers
                                RapidFirePowerUp(asteroid.position.x, asteroid.position.y)
                                print(f"Spawned RapidFirePowerUp at ({asteroid.position.x}, {asteroid.position.y})")
                            break # Assume one shot hits one asteroid part
                
                # Player-powerup collision
                collected_powerups = pygame.sprite.spritecollide(player, powerups_group, True, pygame.sprite.collide_circle)
                for powerup_obj in collected_powerups:
                    powerup_obj.apply_effect(player)
                    print(f"Collected {powerup_obj.powerup_type} power-up! Player cooldown multiplier: {player.shoot_cooldown_multiplier}, Timer: {player.powerup_timer}")

                for sprite in updatable:
                    sprite.update(dt)
            
            # Drawing is done for all sprites in drawable group, including powerups if added
            for sprite in drawable:
                sprite.draw(screen) # Player, Asteroids, Shots, PowerUps use their own draw if defined, or rely on self.image

            score_text_surface = score_font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text_surface, (10, 10))

            if paused:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))
                screen.blit(overlay, (0, 0))
                resume_rect, quit_rect = pause_menu.draw(screen)

        elif game_state == "GAME_OVER":
            # Game Over Screen
            title_surf = game_over_font.render("Game Over", True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
            screen.blit(title_surf, title_rect)

            final_score_surf = score_font.render(f"Final Score: {score}", True, (255, 255, 255))
            final_score_rect = final_score_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(final_score_surf, final_score_rect)

            # High Scores
            hs_start_y = SCREEN_HEIGHT / 2 + 40
            hs_title_surf = score_font.render("High Scores:", True, (255, 255, 255))
            hs_title_rect = hs_title_surf.get_rect(center=(SCREEN_WIDTH / 2, hs_start_y))
            screen.blit(hs_title_surf, hs_title_rect)
            for idx, hs in enumerate(high_scores):
                hs_surf = score_font.render(f"{idx + 1}. {hs}", True, (255, 255, 255))
                hs_rect = hs_surf.get_rect(center=(SCREEN_WIDTH / 2, hs_start_y + 30 * (idx + 1)))
                screen.blit(hs_surf, hs_rect)

            option_start_y = hs_start_y + 30 * (len(high_scores) + 1)
            restart_surf = options_font.render("R - Restart", True, (255, 255, 255))
            restart_rect = restart_surf.get_rect(center=(SCREEN_WIDTH / 2, option_start_y))
            screen.blit(restart_surf, restart_rect)

            quit_surf = options_font.render("Q - Quit", True, (255, 255, 255))
            quit_rect_go = quit_surf.get_rect(center=(SCREEN_WIDTH / 2, option_start_y + 60))
            screen.blit(quit_surf, quit_rect_go)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
