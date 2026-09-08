class Settings:
    """Все постоянные и изменяемые настройки игры."""

    def __init__(self):
        # Постоянные настройки.
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (15, 22, 40)

        self.ship_limit = 3

        self.bullet_width = 4
        self.bullet_height = 14
        self.bullet_color = (245, 230, 90)
        self.bullets_allowed = 3

        self.alien_width = 42
        self.alien_height = 30
        self.alien_color = (80, 220, 130)

        self.fleet_drop_speed = 28

        # Изменяемые настройки.
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Возвращает изменяемые настройки к исходным значениям."""
        self.ship_speed = 6.0
        self.bullet_speed = 8.0
        self.alien_speed = 1.25

        # 1 = вправо, -1 = влево.
        self.fleet_direction = 1

        # Ускорение на каждом новом уровне.
        self.speedup_scale = 1.15

        # Стоимость пришельца увеличивается вместе с уровнем.
        self.alien_points = 50

    def increase_speed(self):
        """Ускоряет корабль, пули и пришельцев после прохождения уровня."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.speedup_scale)
