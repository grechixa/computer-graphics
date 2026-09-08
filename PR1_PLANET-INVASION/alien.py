import pygame


class Alien(pygame.sprite.Sprite):
    """Один пришелец."""

    def __init__(self, ai_game):
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen

        width = self.settings.alien_width
        height = self.settings.alien_height

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        # Простой пиксельный силуэт пришельца.
        body = self.settings.alien_color
        pygame.draw.rect(self.image, body, (6, 5, width - 12, height - 10), border_radius=6)
        pygame.draw.circle(self.image, body, (12, 8), 7)
        pygame.draw.circle(self.image, body, (width - 12, 8), 7)
        pygame.draw.circle(self.image, (20, 30, 35), (16, 14), 3)
        pygame.draw.circle(self.image, (20, 30, 35), (width - 16, 14), 3)
        pygame.draw.line(self.image, body, (10, height - 5), (4, height), 4)
        pygame.draw.line(self.image, body, (width - 10, height - 5), (width - 4, height), 4)

        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = int(self.x)
