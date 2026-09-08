import sys
import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from scoreboard import Scoreboard
from button import Button


class AlienInvasion:
    """Главный класс игры."""

    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        self.clock = pygame.time.Clock()
        self.stats = GameStats(self)

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.sb = Scoreboard(self)

        self.title_font = pygame.font.SysFont(None, 86, bold=True)
        self.subtitle_font = pygame.font.SysFont(None, 30)
        self.message_font = pygame.font.SysFont(None, 34, bold=True)

        self.play_button = Button(
            self,
            "PLAY",
            (self.screen.get_rect().centerx, 390),
            width=260,
            height=70,
            font_size=38,
        )
        self.easy_button = Button(
            self,
            "EASY",
            (self.screen.get_rect().centerx - 300, 510),
            width=180,
            height=58,
            font_size=28,
        )
        self.normal_button = Button(
            self,
            "NORMAL",
            (self.screen.get_rect().centerx, 510),
            width=180,
            height=58,
            font_size=28,
        )
        self.hard_button = Button(
            self,
            "HARD",
            (self.screen.get_rect().centerx + 300, 510),
            width=180,
            height=58,
            font_size=28,
        )

        self.difficulty = "NORMAL"
        self._apply_difficulty(self.difficulty)

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_button(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_ESCAPE:
            self._quit_game()

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.stats.game_active:
                self._fire_bullet()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self.start_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_mouse_button(self, event):
        if self.stats.game_active:
            return

        mouse_pos = event.pos

        if self.play_button.rect.collidepoint(mouse_pos):
            self.start_game()
        elif self.easy_button.rect.collidepoint(mouse_pos):
            self._apply_difficulty("EASY")
        elif self.normal_button.rect.collidepoint(mouse_pos):
            self._apply_difficulty("NORMAL")
        elif self.hard_button.rect.collidepoint(mouse_pos):
            self._apply_difficulty("HARD")

    # ------------------------------------------------------------------
    # Game start / difficulty
    # ------------------------------------------------------------------

    def _apply_difficulty(self, difficulty):
        self.difficulty = difficulty

        presets = {
            "EASY": (0.95, 7.5, 1.10, 1.10),
            "NORMAL": (1.25, 8.0, 1.15, 1.15),
            "HARD": (1.65, 9.0, 1.22, 1.20),
        }

        alien_speed, bullet_speed, speedup, _ = presets[difficulty]
        self.settings.alien_speed = alien_speed
        self.settings.bullet_speed = bullet_speed
        self.settings.speedup_scale = speedup

    def start_game(self):
        """Начинает новую игру и сбрасывает изменяемые настройки."""
        self.settings.initialize_dynamic_settings()
        self._apply_difficulty(self.difficulty)

        self.stats.reset_stats()
        self.stats.game_active = True

        self.bullets.empty()
        self.aliens.empty()

        self.ship.center_ship()
        self._create_fleet()

        self.sb.update_score()
        pygame.mouse.set_visible(False)

    # ------------------------------------------------------------------
    # Bullets
    # ------------------------------------------------------------------

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            bullet = Bullet(self)
            self.bullets.add(bullet)

    def _update_bullets(self):
        self.bullets.update()

        for bullet in list(self.bullets):
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            # Начисляем очки за каждого уничтоженного пришельца.
            destroyed = sum(len(alien_list) for alien_list in collisions.values())
            self.stats.score += destroyed * self.settings.alien_points

            if self.stats.score > self.stats.high_score:
                self.stats.high_score = self.stats.score

            self.sb.update_score()

        if not self.aliens:
            self.bullets.empty()
            self.settings.increase_speed()
            self.stats.level += 1
            self._create_fleet()
            self.sb.update_score()

    # ------------------------------------------------------------------
    # Aliens
    # ------------------------------------------------------------------

    def _create_fleet(self):
        alien = Alien(self)

        available_space_x = self.settings.screen_width - 2 * alien.rect.width
        number_aliens_x = max(
            1, int(available_space_x // (2 * alien.rect.width))
        )

        # Ряды по высоте: верхняя часть экрана занята флотом.
        available_space_y = (
            self.settings.screen_height
            - 3 * alien.rect.height
            - self.ship.rect.height
        )
        number_rows = max(
            1, int(available_space_y // (2 * alien.rect.height))
        )

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)

        alien.rect.x = alien.rect.width + 2 * alien.rect.width * alien_number
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        alien.x = float(alien.rect.x)

        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        # Пришелец столкнулся с кораблем.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    # ------------------------------------------------------------------
    # Ship / lives
    # ------------------------------------------------------------------

    def _ship_hit(self):
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.sb.update_score()

            self.bullets.empty()
            self.aliens.empty()

            self.ship.center_ship()
            self._create_fleet()

            pygame.time.delay(650)
        else:
            self.stats.game_active = False
            self.stats.save_high_score()
            pygame.mouse.set_visible(True)

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        if self.stats.game_active:
            self.ship.blitme()

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            self.aliens.draw(self.screen)
            self.sb.draw()
        else:
            self._draw_menu()

        pygame.display.flip()

    def _draw_menu(self):
        title = self.title_font.render("ALIEN INVASION", True, (235, 240, 250))
        title_rect = title.get_rect(
            center=(self.screen.get_rect().centerx, 150)
        )
        self.screen.blit(title, title_rect)

        subtitle = self.subtitle_font.render(
            "Destroy the alien fleet before it reaches you",
            True,
            (170, 185, 205),
        )
        subtitle_rect = subtitle.get_rect(
            center=(self.screen.get_rect().centerx, 215)
        )
        self.screen.blit(subtitle, subtitle_rect)

        score_text = self.message_font.render(
            f"HIGH SCORE: {self.stats.high_score:,}",
            True,
            (245, 230, 90),
        )
        score_rect = score_text.get_rect(
            center=(self.screen.get_rect().centerx, 275)
        )
        self.screen.blit(score_text, score_rect)

        diff_text = self.subtitle_font.render(
            f"Difficulty: {self.difficulty}",
            True,
            (190, 205, 220),
        )
        diff_rect = diff_text.get_rect(
            center=(self.screen.get_rect().centerx, 325)
        )
        self.screen.blit(diff_text, diff_rect)

        self.play_button.draw()
        self.easy_button.draw()
        self.normal_button.draw()
        self.hard_button.draw()

        controls = self.subtitle_font.render(
            "P — start    ← → — move    SPACE — fire    ESC — exit",
            True,
            (145, 160, 180),
        )
        controls_rect = controls.get_rect(
            center=(self.screen.get_rect().centerx, 625)
        )
        self.screen.blit(controls, controls_rect)

    def _quit_game(self):
        self.stats.save_high_score()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = AlienInvasion()
    game.run_game()
