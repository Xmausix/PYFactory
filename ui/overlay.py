import pygame
from constants import (TILE_SIZE, TOP_BAR_H, BELT_DELTA, B_POWER_USAGE,
                        C_OVERLAY_BELT, C_OVERLAY_PWR)


class LogisticsOverlay:
    """Press X to show belt directions, item flow, and power zones."""

    def __init__(self):
        self.enabled = False

    def toggle(self):
        self.enabled = not self.enabled

    def draw(self, screen, gmap, cam_x, cam_y, play_h):
        if not self.enabled:
            return
        for b in gmap.buildings:
            rx = b.x * TILE_SIZE - cam_x
            ry = b.y * TILE_SIZE - cam_y + TOP_BAR_H
            if not (-TILE_SIZE <= rx <= screen.get_width() and
                    TOP_BAR_H - TILE_SIZE <= ry <= TOP_BAR_H + play_h):
                continue
            # Belt direction arrows
            if b.btype in ("belt", "underground_belt") and hasattr(b, "direction"):
                dx, dy = BELT_DELTA.get(b.direction, (1, 0))
                cx, cy = rx + TILE_SIZE // 2, ry + TILE_SIZE // 2
                ex, ey = cx + dx * 12, cy + dy * 12
                s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                s.fill((100, 200, 255, 40))
                screen.blit(s, (rx, ry))
                pygame.draw.line(screen, (100, 200, 255), (cx, cy), (ex, ey), 2)
                pygame.draw.circle(screen, (100, 200, 255), (ex, ey), 3)
            # Power consumers
            pwr = B_POWER_USAGE.get(b.btype, 0)
            if pwr > 0:
                s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                s.fill((255, 220, 60, 30))
                screen.blit(s, (rx, ry))
                font = pygame.font.SysFont("consolas,monospace", 9)
                screen.blit(font.render(f"{pwr}MW", True, (255, 220, 60)), (rx + 1, ry + TILE_SIZE - 10))
            # Power producers
            if hasattr(b, "current_output"):
                s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                s.fill((80, 255, 120, 30))
                screen.blit(s, (rx, ry))