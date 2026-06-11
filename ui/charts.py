import pygame
from constants import C_CHART_BG, C_CHART_LINE, C_CHART_MONEY, C_TXT_DIM


class MiniChart:
    """Tiny sparkline chart for the dashboard."""

    def __init__(self, w: int = 160, h: int = 40):
        self.w = w
        self.h = h
        self._font = pygame.font.SysFont("consolas,monospace", 10)

    def draw(self, screen: pygame.Surface,
             x: int, y: int,
             values: list[float],
             color: tuple,
             label: str = "",
             unit: str = "") -> None:
        if not values:
            return
        pygame.draw.rect(screen, C_CHART_BG, (x, y, self.w, self.h))
        pygame.draw.rect(screen, (50, 52, 72),  (x, y, self.w, self.h), 1)

        mx = max(values) if max(values) > 0 else 1
        pts = []
        n   = len(values)
        for i, v in enumerate(values):
            px_ = x + int(i / (n - 1) * (self.w - 2)) + 1
            py_ = y + self.h - 2 - int(v / mx * (self.h - 4))
            pts.append((px_, py_))
        if len(pts) > 1:
            pygame.draw.lines(screen, color, False, pts, 1)

        if label:
            screen.blit(
                self._font.render(label, True, C_TXT_DIM),
                (x + 2, y + 2))
        if values:
            cur = f"{values[-1]:.1f}{unit}"
            screen.blit(
                self._font.render(cur, True, color),
                (x + self.w - len(cur) * 6 - 2, y + 2))