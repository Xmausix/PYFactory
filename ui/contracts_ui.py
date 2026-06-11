import pygame
import time
from constants import C_GRID_B, C_TXT, C_TXT_DIM, C_OK, C_WARN, C_CONTRACT


class ContractsUI:
    def __init__(self):
        self.fontS = pygame.font.SysFont("consolas,monospace", 11)

    def draw_sidebar(self, screen, contracts, x, y, w):
        """Draw active contracts in the dashboard."""
        screen.blit(self.fontS.render("📦 Contracts", True, C_CONTRACT), (x, y))
        y += 16
        now = time.time()
        for c in contracts.contracts[:3]:
            if c.completed:
                continue
            remaining = max(0, c.deadline - now)
            pct       = c.progress / c.amount
            color     = C_OK if pct >= 1.0 else C_WARN if remaining < 30 else C_TXT
            screen.blit(self.fontS.render(
                f"{c.item}: {c.progress}/{c.amount} ({c.reward}$)",
                True, color), (x + 4, y))
            y += 13
            # Timer
            screen.blit(self.fontS.render(
                f"  Time: {remaining:.0f}s", True, C_TXT_DIM), (x + 4, y))
            y += 13
            # Progress bar
            bw = w - 12
            pygame.draw.rect(screen, (40, 42, 60), (x + 4, y, bw, 6))
            pygame.draw.rect(screen, color, (x + 4, y, int(bw * pct), 6))
            y += 10
        return y