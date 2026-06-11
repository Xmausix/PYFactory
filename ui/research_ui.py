import pygame
from constants import C_BAR, C_GRID_B, C_TXT, SIDE_PANEL_W


class ResearchUI:
    """Full-screen research tree overlay."""

    def __init__(self, screen_w: int, screen_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.font  = pygame.font.SysFont("consolas,monospace", 14, bold=True)
        self.fontS = pygame.font.SysFont("consolas,monospace", 11)
        self.visible = False

    def toggle(self) -> None:
        self.visible = not self.visible

    def draw(self, screen, research) -> None:
        if not self.visible:
            return

        ov = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        ov.fill((10, 10, 20, 220))
        screen.blit(ov, (0, 0))

        title = self.font.render("🔬 Research Tree  (R to close)", True, (200, 200, 255))
        screen.blit(title, (30, 20))

        techs = list(research.techs.values())
        cols = 3
        cell_w = (self.screen_w - 60) // cols
        cell_h = 100

        for i, tech in enumerate(techs):
            col = i % cols
            row = i // cols
            rx = 30 + col * cell_w
            ry = 60 + row * cell_h

            # Background
            can = research.can_research(tech.key)
            if tech.unlocked:
                bg = (30, 70, 30)
                border = (80, 200, 80)
            elif can:
                bg = (40, 40, 80)
                border = (100, 100, 220)
            else:
                bg = (30, 30, 40)
                border = (60, 60, 80)

            pygame.draw.rect(screen, bg, (rx, ry, cell_w - 10, cell_h - 10))
            pygame.draw.rect(screen, border, (rx, ry, cell_w - 10, cell_h - 10), 2)

            # Active research indicator
            if research.active_research == tech.key:
                pygame.draw.rect(screen, (255, 220, 50),
                                 (rx, ry, cell_w - 10, cell_h - 10), 3)

            y = ry + 6
            mark = "✓" if tech.unlocked else ("▶" if research.active_research == tech.key else "○")
            screen.blit(self.font.render(f"{mark} {tech.name}", True, (220, 220, 255)), (rx + 6, y))
            y += 18
            screen.blit(self.fontS.render(tech.description[:30], True, (160, 160, 200)), (rx + 6, y))
            y += 14
            screen.blit(self.fontS.render(f"Effect: {tech.effect_desc}", True, (140, 200, 140)), (rx + 6, y))
            y += 14
            cost_c = (200, 200, 100) if not tech.unlocked else (100, 180, 100)
            screen.blit(self.fontS.render(f"Cost: {tech.cost} RP", True, cost_c), (rx + 6, y))

            # Click hint
            if can and not tech.unlocked:
                screen.blit(self.fontS.render("[Click] Start", True, (100, 200, 255)),
                            (rx + 6, ry + cell_h - 24))

    def handle_click(self, pos: tuple, research) -> bool:
        """Returns True if click was consumed."""
        if not self.visible:
            return False
        mx, my = pos
        techs = list(research.techs.values())
        cols = 3
        cell_w = (self.screen_w - 60) // cols
        cell_h = 100
        for i, tech in enumerate(techs):
            col = i % cols
            row = i // cols
            rx = 30 + col * cell_w
            ry = 60 + row * cell_h
            r = pygame.Rect(rx, ry, cell_w - 10, cell_h - 10)
            if r.collidepoint(mx, my):
                research.start_research(tech.key)
                return True
        return True  # Consume all clicks when UI open