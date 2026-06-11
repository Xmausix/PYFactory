import pygame
from constants import C_OK, C_TXT, C_TXT_DIM


class ResearchUI:
    """Full-screen research tree overlay (press R)."""

    def __init__(self, screen_w: int, screen_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.visible  = False
        self.font     = pygame.font.SysFont("consolas,monospace", 14, bold=True)
        self.fontS    = pygame.font.SysFont("consolas,monospace", 11)

    def toggle(self) -> None:
        self.visible = not self.visible

    def draw(self, screen: pygame.Surface, research) -> None:
        if not self.visible:
            return
        ov = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        ov.fill((8, 8, 18, 230))
        screen.blit(ov, (0, 0))

        title = self.font.render(
            "🔬 Research Tree  —  R to close  —  Click to start",
            True, (180, 185, 230))
        screen.blit(title, (24, 16))

        techs  = list(research.techs.values())
        cols   = 4
        cw     = (self.screen_w - 40) // cols
        ch     = 110
        margin = 8

        for i, tech in enumerate(techs):
            col = i % cols
            row = i // cols
            rx  = 20 + col * cw
            ry  = 50 + row * ch

            # Background color
            if tech.unlocked:
                bg, border = (28, 60, 28), (70, 200, 70)
            elif research.can_research(tech.key):
                bg, border = (30, 32, 70), (90, 100, 220)
            else:
                bg, border = (24, 24, 36), (50, 52, 70)

            bw = cw - margin
            bh = ch - margin
            pygame.draw.rect(screen, bg,     (rx, ry, bw, bh))
            pygame.draw.rect(screen, border, (rx, ry, bw, bh), 2)
            if research.active_research == tech.key:
                pygame.draw.rect(screen, (255, 210, 40), (rx, ry, bw, bh), 3)

            y = ry + 6
            mark = "✓" if tech.unlocked else (
                "▶" if research.active_research == tech.key else "○")
            screen.blit(
                self.font.render(f"{mark} {tech.name}", True, (210, 215, 240)),
                (rx + 6, y))
            y += 18
            screen.blit(
                self.fontS.render(tech.description[:34], True, (150, 155, 190)),
                (rx + 6, y))
            y += 13
            screen.blit(
                self.fontS.render(
                    f"Effect: {tech.effect_desc[:28]}", True, (130, 200, 130)),
                (rx + 6, y))
            y += 13
            cost_c = (180, 180, 80) if not tech.unlocked else (90, 160, 90)
            screen.blit(
                self.fontS.render(f"Cost: {tech.cost} RP", True, cost_c),
                (rx + 6, y))
            if research.can_research(tech.key) and not tech.unlocked:
                screen.blit(
                    self.fontS.render("[Click] Start", True, (100, 200, 255)),
                    (rx + 6, ry + bh - 16))

    def handle_click(self, pos: tuple, research) -> bool:
        if not self.visible:
            return False
        mx, my = pos
        techs  = list(research.techs.values())
        cols   = 4
        cw     = (self.screen_w - 40) // cols
        ch     = 110
        for i, tech in enumerate(techs):
            col = i % cols
            row = i // cols
            rx  = 20 + col * cw
            ry  = 50 + row * ch
            if pygame.Rect(rx, ry, cw - 8, ch - 8).collidepoint(mx, my):
                research.start_research(tech.key)
                return True
        return True