import pygame


class Scoreboard:
    """Выводит счет, рекорд, уровень и количество кораблей."""

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (235, 240, 250)
        self.font = pygame.font.SysFont(None, 30, bold=True)
        self.big_font = pygame.font.SysFont(None, 54, bold=True)

        self.score_image = None
        self.high_score_image = None
        self.level_image = None

        self.prep_images()

    def prep_images(self):
        self.score_image = self.font.render(
            f"SCORE: {self.stats.score:,}", True, self.text_color
        )
        self.high_score_image = self.font.render(
            f"HIGH: {self.stats.high_score:,}", True, self.text_color
        )
        self.level_image = self.font.render(
            f"LEVEL: {self.stats.level}", True, self.text_color
        )

        self.score_rect = self.score_image.get_rect()
        self.score_rect.topright = (self.screen_rect.right - 20, 15)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.topright = (self.screen_rect.right - 20, 48)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.topright = (self.screen_rect.right - 20, 81)

    def draw(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        # Иконки оставшихся кораблей.
        start_x = 20
        y = 20
        for i in range(self.stats.ships_left):
            pygame.draw.polygon(
                self.screen,
                (80, 180, 255),
                [(start_x + i * 36 + 12, y), (start_x + i * 36 + 24, y + 22),
                 (start_x + i * 36, y + 22)],
            )

    def update_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
        self.prep_images()
