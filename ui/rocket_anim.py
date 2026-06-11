import pygame
import math


class RocketAnimation:
    """Fullscreen rocket launch animation."""

    def __init__(self, screen_w: int, screen_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.active   = False
        self.t        = 0.0
        self.font     = pygame.font.SysFont("consolas,monospace", 42, bold=True)
        self.fontM    = pygame.font.SysFont("consolas,monospace", 22, bold=True)
        self.fontS    = pygame.font.SysFont("consolas,monospace", 15)
        self._done    = False

    def start(self) -> None:
        self.active = True
        self.t      = 0.0
        self._done  = False

    @property
    def finished(self) -> bool:
        return self._done

    def update(self, dt: float) -> None:
        if not self.active:
            return
        self.t += dt
        if self.t > 8.0:
            self._done = True

    def draw(self, screen: pygame.Surface) -> None:
        if not self.active:
            return
        # Dark sky
        sky_col = tuple(
            int(c * max(0.0, 1.0 - self.t / 6))
            for c in (20, 22, 35))
        screen.fill(sky_col)

        # Stars appear
        if self.t > 2.0:
            import random
            rng = random.Random(42)
            for _ in range(80):
                sx = rng.randint(0, self.screen_w)
                sy = rng.randint(0, self.screen_h // 2)
                br = min(255, int((self.t - 2.0) * 80))
                pygame.draw.circle(screen, (br, br, br), (sx, sy), 1)

        # Rocket body
        cx  = self.screen_w // 2
        base_y = self.screen_h * 0.75
        ry_ = base_y - max(0, (self.t ** 2) * 60)
        ry_ = max(-60, ry_)

        # Exhaust flame
        flame_h = int(30 + 20 * math.sin(self.t * 20))
        for i in range(flame_h):
            alpha  = int(255 * (1 - i / flame_h))
            radius = max(1, int((flame_h - i) * 0.4))
            c      = (255, max(50, 200 - i * 4), 0)
            s      = pygame.Surface(
                (radius * 2, radius * 2), pygame.SRCALPHA)
            s.fill((*c, alpha))
            screen.blit(s, (cx - radius, int(ry_) + 30 + i))

        # Body
        pygame.draw.rect(screen, (200, 205, 220),
                         (cx - 12, int(ry_) - 28, 24, 60))
        # Nose cone
        pygame.draw.polygon(screen, (230, 235, 255), [
            (cx, int(ry_) - 50),
            (cx - 12, int(ry_) - 28),
            (cx + 12, int(ry_) - 28),
        ])
        # Fins
        pygame.draw.polygon(screen, (180, 185, 200), [
            (cx - 12, int(ry_) + 30),
            (cx - 24, int(ry_) + 50),
            (cx - 12, int(ry_) + 50),
        ])
        pygame.draw.polygon(screen, (180, 185, 200), [
            (cx + 12, int(ry_) + 30),
            (cx + 24, int(ry_) + 50),
            (cx + 12, int(ry_) + 50),
        ])

        # Text
        if self.t > 1.0:
            t1 = self.font.render("🚀  LAUNCHED!", True, (255, 230, 80))
            screen.blit(t1, t1.get_rect(
                center=(self.screen_w // 2, self.screen_h // 2 + 60)))
        if self.t > 2.5:
            t2 = self.fontM.render(
                "Your factory has reached the stars.", True, (200, 220, 255))
            screen.blit(t2, t2.get_rect(
                center=(self.screen_w // 2, self.screen_h // 2 + 110)))
        if self.t > 4.0:
            t3 = self.fontS.render(
                "Press any key to continue", True, (130, 135, 160))
            screen.blit(t3, t3.get_rect(
                center=(self.screen_w // 2, self.screen_h // 2 + 150)))