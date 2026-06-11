import pygame
from constants import C_GRID_B, C_TXT_DIM


class PauseMenu:
    OPTIONS = ["Resume", "Save Game", "Settings", "Main Menu", "Quit"]

    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.visible  = False
        self.selected = 0
        self.font     = pygame.font.SysFont("consolas,monospace", 22, bold=True)
        self.fontS    = pygame.font.SysFont("consolas,monospace", 14)
        self.fontT    = pygame.font.SysFont("consolas,monospace", 28, bold=True)

    def toggle(self):
        self.visible  = not self.visible
        self.selected = 0

    def _get_panel(self):
        W, H = 360, 400
        rx = (self.screen_w - W) // 2
        ry = (self.screen_h - H) // 2
        return W, H, rx, ry

    def _btn_rect(self, index: int) -> pygame.Rect:
        W, H, rx, ry = self._get_panel()
        btn_w = W - 48
        btn_h = 46
        gap   = 8
        start_y = ry + 90
        x = rx + 24
        y = start_y + index * (btn_h + gap)
        return pygame.Rect(x, y, btn_w, btn_h)

    def draw(self, screen):
        if not self.visible:
            return

        # Dim overlay
        ov = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 180))
        screen.blit(ov, (0, 0))

        W, H, rx, ry = self._get_panel()
        pygame.draw.rect(screen, (28, 30, 48), (rx, ry, W, H), border_radius=8)
        pygame.draw.rect(screen, C_GRID_B, (rx, ry, W, H), 2, border_radius=8)

        # Title
        title = self.fontT.render("PAUSED", True, (220, 225, 240))
        screen.blit(title, title.get_rect(
            center=(self.screen_w // 2, ry + 45)))

        # Buttons
        mx, my = pygame.mouse.get_pos()
        for i, opt in enumerate(self.OPTIONS):
            rect    = self._btn_rect(i)
            hovered = rect.collidepoint(mx, my)
            sel     = i == self.selected or hovered

            bg = (44, 46, 68) if sel else (32, 34, 52)
            pygame.draw.rect(screen, bg, rect, border_radius=5)

            bc = (255, 225, 60) if sel else (55, 58, 78)
            pygame.draw.rect(screen, bc, rect, 2, border_radius=5)

            color = (255, 225, 60) if sel else (170, 175, 200)
            pre = "▶  " if sel else "   "
            t = self.font.render(f"{pre}{opt}", True, color)
            screen.blit(t, (rect.x + 14, rect.y + 11))

        # Hint
        screen.blit(self.fontS.render("ESC to resume", True, C_TXT_DIM),
                    (rx + 20, ry + H - 28))

    def handle_event(self, ev) -> str | None:
        if not self.visible:
            return None

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                self.visible = False
                return "resume"
            if ev.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.OPTIONS)
            elif ev.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.OPTIONS)
            elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.visible = False
                return self._action(self.selected)

        elif ev.type == pygame.MOUSEMOTION:
            for i in range(len(self.OPTIONS)):
                if self._btn_rect(i).collidepoint(ev.pos):
                    self.selected = i
                    break

        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            for i in range(len(self.OPTIONS)):
                if self._btn_rect(i).collidepoint(ev.pos):
                    self.visible = False
                    return self._action(i)

        return None

    def _action(self, index: int) -> str:
        return self.OPTIONS[index].lower().replace(" ", "_")