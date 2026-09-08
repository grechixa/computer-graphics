import pygame


class Bullet(pygame.sprite.Sprite):
    """Снаряд, летящий вверх."""

    def __init__(self, ai_game):
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen

        self.image = pygame.Surface(
            (self.settings.bullet_width, self.settings.bullet_height)
        )
        self.image.fill(self.settings.bullet_color)

        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = int(self.y)

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)
