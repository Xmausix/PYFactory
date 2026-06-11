import pygame
from constants import C_GRID_B, C_TXT, C_TXT_DIM, C_ACHIEVE, ACHIEVEMENT_DEFS


class AchievementsUI:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.visible  = False
        self.font     = pygame.font.SysFont("consolas,monospace", 16, bold=True)
        self.fontS    = pygame.font.SysFont("consolas,monospace", 12)

    def toggle(self):
        self.visible = not self.visible

    def draw(self, screen, achievements):
        if not self.visible:
            return
        ov = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 200))
        screen.blit(ov, (0, 0))
        W, H = min(450, self.screen_w - 40), min(420, self.screen_h - 40)
        rx = (self.screen_w - W) // 2
        ry = (self.screen_h - H) // 2
        pygame.draw.rect(screen, (22, 24, 38), (rx, ry, W, H))
        pygame.draw.rect(screen, C_GRID_B, (rx, ry, W, H), 2)

        y = ry + 12
        screen.blit(self.font.render(f"🏆 Achievements ({len(achievements.unlocked)}/{len(ACHIEVEMENT_DEFS)})",
                                      True, C_ACHIEVE), (rx + 12, y))
        y += 28
        for a in ACHIEVEMENT_DEFS:
            unlocked = a["id"] in achievements.unlocked
            icon     = a["icon"] if unlocked else "🔒"
            color    = C_ACHIEVE if unlocked else C_TXT_DIM
            screen.blit(self.fontS.render(f"{icon} {a['title']}", True, color), (rx + 16, y))
            screen.blit(self.fontS.render(a["desc"], True, C_TXT_DIM), (rx + 180, y))
            y += 20
        y += 10
        screen.blit(self.fontS.render("[H] Close", True, C_TXT_DIM), (rx + 16, y))