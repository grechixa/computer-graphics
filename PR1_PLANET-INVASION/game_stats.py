class GameStats:
    """Хранит статистику текущей игры."""

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False

        # Исторический рекорд сохраняется между запусками.
        self.high_score = self._load_high_score()

    def reset_stats(self):
        """Сбрасывает статистику новой игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _load_high_score(self):
        try:
            with open("highscore.txt", "r", encoding="utf-8") as file:
                return int(file.read().strip() or 0)
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        """Сохраняет рекорд в файл."""
        try:
            with open("highscore.txt", "w", encoding="utf-8") as file:
                file.write(str(int(self.high_score)))
        except OSError:
            pass
