import pygame


class Ship(pygame.sprite.Sprite):
    """Корабль игрока."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.width = 58
        self.height = 34

        # Рисуем корабль без внешнего изображения.
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.polygon(
            self.image,
            (80, 180, 255),
            [(self.width // 2, 0), (self.width, self.height), (0, self.height)],
        )
        pygame.draw.polygon(
            self.image,
            (220, 245, 255),
            [
                (self.width // 2, 8),
                (self.width // 2 + 8, self.height - 4),
                (self.width // 2 - 8, self.height - 4),
            ],
        )

        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        """Возвращает корабль в исходную позицию."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = int(self.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
