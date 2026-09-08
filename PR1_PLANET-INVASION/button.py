import pygame


class Button:
    """Простая кнопка Pygame."""

    def __init__(self, ai_game, text, center, width=210, height=60, font_size=32):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center

        self.normal_color = (45, 75, 115)
        self.hover_color = (70, 110, 160)
        self.border_color = (150, 200, 255)

        self.text = text
        self.font = pygame.font.SysFont(None, font_size, bold=True)

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.normal_color

        pygame.draw.rect(self.screen, color, self.rect, border_radius=10)
        pygame.draw.rect(self.screen, self.border_color, self.rect, width=2, border_radius=10)

        text_image = self.font.render(self.text, True, (240, 245, 255))
        text_rect = text_image.get_rect(center=self.rect.center)
        self.screen.blit(text_image, text_rect)
