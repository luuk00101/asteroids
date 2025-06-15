import pygame

class PauseMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.title_font = pygame.font.Font(None, 74)
        self.item_font = pygame.font.Font(None, 50)
        self.text_color = (255, 255, 255)  # White

        self.title_text = "Paused"
        self.resume_text = "R - Resume"
        self.quit_text = "Q - Quit"

        self.resume_rect = None
        self.quit_rect = None

    def draw(self, screen):
        # Render "Paused" text
        title_surf = self.title_font.render(self.title_text, True, self.text_color)
        title_rect = title_surf.get_rect(center=(self.screen_width / 2, self.screen_height / 3))
        screen.blit(title_surf, title_rect)

        # Render "R - Resume" text
        resume_surf = self.item_font.render(self.resume_text, True, self.text_color)
        self.resume_rect = resume_surf.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        screen.blit(resume_surf, self.resume_rect)

        # Render "Q - Quit" text
        quit_surf = self.item_font.render(self.quit_text, True, self.text_color)
        self.quit_rect = quit_surf.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + 60))
        screen.blit(quit_surf, self.quit_rect)

        return self.resume_rect, self.quit_rect
