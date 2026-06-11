import pygame
from constants import (C_BAR, C_GRID_B, C_MONEY, C_TXT, C_TXT_DIM,
                        C_ERR, C_WARN, C_OK,
                        B_COLORS, B_KEYS, B_COSTS,
                        TOP_BAR_H, BOTTOM_BAR_H, SIDE_PANEL_W)

_STATUS_DOT = {
    "working":  (80,  220, 100),
    "waiting":  (255, 200,  40),
    "no_power": (255,  60,  60),
    "idle":     (80,   80,  80),
}

_BUILDINGS_ORDER = [
    "miner", "belt", "underground_belt", "furnace",
    "inserter", "storage", "market", "assembler",
    "coal_generator", "solar_panel",
    "splitter", "priority_splitter", "merger",
    "train_station", "rail", "robot_port",
]


class HUD:
    BTN_W = 68
    BTN_H = 44

    def __init__(self, screen_w: int, screen_h: int, play_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.play_h   = play_h
        self.font  = pygame.font.SysFont("consolas,monospace", 14, bold=True)
        self.fontS = pygame.font.SysFont("consolas,monospace", 11)
        self.fontL = pygame.font.SysFont("consolas,monospace", 22, bold=True)

    def draw_top_bar(self, screen: pygame.Surface,
                     econ, energy, paused: bool,
                     fps: int, zoom: float) -> None:
        w = self.screen_w - SIDE_PANEL_W
        pygame.draw.rect(screen, C_BAR, (0, 0, w, TOP_BAR_H))
        pygame.draw.line(screen, C_GRID_B, (0, TOP_BAR_H), (w, TOP_BAR_H), 2)

        screen.blit(
            self.font.render(f"💰 {econ.money:,}$", True, C_MONEY),
            (8, 9))
        ec = energy.status_color
        screen.blit(
            self.fontS.render(
                f"⚡ {energy.total_consumed}/{energy.total_generated} MW",
                True, ec),
            (200, 11))
        if energy.shortage:
            screen.blit(
                self.fontS.render("NO POWER", True, C_ERR), (400, 11))
        screen.blit(
            self.fontS.render(
                f"FPS:{fps}  Z:{zoom:.2f}x  [F11] FS  [R] Research",
                True, C_TXT_DIM),
            (w - 310, 11))
        if paused:
            t = self.font.render("── PAUSED ──", True, (255, 100, 100))
            screen.blit(t, t.get_rect(center=(w // 2, TOP_BAR_H // 2)))

    def draw_bottom_bar(self, screen: pygame.Surface,
                        sel: str | None,
                        placer,
                        shift_held: bool) -> None:
        y0 = TOP_BAR_H + self.play_h
        w  = self.screen_w - SIDE_PANEL_W
        pygame.draw.rect(screen, C_BAR, (0, y0, w, BOTTOM_BAR_H))
        pygame.draw.line(screen, C_GRID_B, (0, y0), (w, y0), 2)

        x = 3
        for bt in _BUILDINGS_ORDER:
            if x + self.BTN_W > w - 80:
                break
            col = B_COLORS.get(bt, (100, 100, 100))
            r   = pygame.Rect(x, y0 + 3, self.BTN_W, BOTTOM_BAR_H - 6)
            pygame.draw.rect(screen, col, r)
            if sel == bt:
                pygame.draw.rect(screen, (255, 255, 140), r, 3)
            else:
                pygame.draw.rect(screen, (180, 180, 180), r, 1)
            key = B_KEYS.get(bt, "?")
            label = bt[:7] if len(bt) <= 7 else bt[:6] + "."
            screen.blit(
                self.fontS.render(f"[{key}]{label}", True, (255, 255, 255)),
                (x + 2, y0 + 6))
            screen.blit(
                self.fontS.render(f"{B_COSTS.get(bt, '?')}$",
                                  True, (200, 200, 200)),
                (x + 2, y0 + 20))
            x += self.BTN_W + 2

        # Hint
        hint = self._hint(sel, placer, shift_held)
        if hint:
            screen.blit(
                self.fontS.render(hint, True, (160, 165, 185)),
                (x + 4, y0 + 14))

    @staticmethod
    def _hint(sel: str | None, placer, shift: bool) -> str:
        parts = []
        if sel in ("belt", "underground_belt"):
            parts.append(f"Q/E: dir={placer.belt_dir}")
        if sel == "underground_belt":
            parts.append(f"[F]: mode={placer.ugb_mode}")
        if sel == "inserter":
            parts.append(f"Q/E: dir={placer.inserter_dir}")
        if sel == "assembler":
            parts.append(f"Q/E: recipe={placer.recipe}")
        if sel in ("splitter", "priority_splitter"):
            parts.append(f"Q/E: dir={placer.splitter_dir}")
        if sel == "merger":
            parts.append(f"Q/E: dir={placer.merger_dir}")
        if sel == "rail":
            parts.append(f"Q/E: dir={placer.rail_dir}")
        if shift:
            parts.append("[SHIFT] auto-build")
        return "  ".join(parts)

    def draw_notifications(self, screen: pygame.Surface,
                           notifications: list[dict]) -> None:
        y = TOP_BAR_H + self.play_h - 30
        for n in reversed(notifications[-6:]):
            if n["t"] <= 0:
                continue
            alpha = int(min(255, n["t"] * 100))
            s     = pygame.Surface((380, 20), pygame.SRCALPHA)
            s.fill((36, 36, 54, alpha))
            t = self.fontS.render(n["text"], True, (200, 255, 180))
            s.blit(t, (5, 3))
            screen.blit(s, (8, y))
            y -= 22

    def draw_pause_overlay(self, screen: pygame.Surface) -> None:
        ov = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 150))
        screen.blit(ov, (0, 0))
        t = self.fontL.render("PAUSED  —  P to resume", True, (220, 225, 240))
        screen.blit(t, t.get_rect(center=(self.screen_w // 2,
                                           self.screen_h // 2)))


    def draw_win_screen(self, screen: pygame.Surface) -> None:
        ov = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 190))
        screen.blit(ov, (0, 0))
        cx = self.screen_w // 2
        cy = self.screen_h // 2 - 50
        for line, color in [
            ("🚀  ROCKET LAUNCHED!  🚀", (255, 230, 80)),
            ("Your factory is complete!", (200, 220, 255)),
            ("Press ESC to continue", (150, 155, 175)),
        ]:
            t = self.fontL.render(line, True, color)
            screen.blit(t, t.get_rect(center=(cx, cy)))
            cy += 44