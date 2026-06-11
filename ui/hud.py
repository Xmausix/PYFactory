import pygame
from constants import (C_BAR, C_GRID_B, C_MONEY, C_ITEMS, C_TXT,
                       C_ENERGY_OK, C_ENERGY_WARN, C_ENERGY_BAD,
                       B_COLORS, B_KEYS, B_COSTS,
                       TOP_BAR_H, BOTTOM_BAR_H, SIDE_PANEL_W,
                       C_WORKING, C_WAITING, C_NO_POWER)


STATUS_COLORS = {
    "working":  C_WORKING,
    "waiting":  C_WAITING,
    "no_power": C_NO_POWER,
    "idle":     (120, 120, 120),
}


class HUD:
    BUILDINGS = [
        "miner", "belt", "smelter", "inserter",
        "storage", "market", "assembler",
        "generator", "splitter", "merger",
    ]

    def __init__(self, screen_w: int, screen_h: int, play_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.play_h = play_h
        self.font  = pygame.font.SysFont("consolas,monospace", 15, bold=True)
        self.fontS = pygame.font.SysFont("consolas,monospace", 11)
        self.fontL = pygame.font.SysFont("consolas,monospace", 22, bold=True)

    def draw_top_bar(self, screen, econ, energy, paused: bool,
                     fps: int, zoom: float) -> None:
        w = self.screen_w - SIDE_PANEL_W
        pygame.draw.rect(screen, C_BAR, (0, 0, w, TOP_BAR_H))
        pygame.draw.line(screen, C_GRID_B, (0, TOP_BAR_H), (w, TOP_BAR_H), 2)

        screen.blit(
            self.font.render(f"Money: {econ.money}$", True, C_MONEY),
            (10, 8))
        screen.blit(
            self.font.render(f"Earned: {econ.total_earned}$", True, C_ITEMS),
            (200, 8))

        # Energy display
        ec = energy.status_color
        etxt = f"Power: {energy.total_consumed}/{energy.total_generated} MW"
        screen.blit(self.font.render(etxt, True, ec), (420, 8))
        if energy.shortage > 0:
            screen.blit(
                self.fontS.render("⚡ NO POWER", True, C_ENERGY_BAD),
                (620, 10))

        screen.blit(
            self.fontS.render(f"FPS:{fps} Zoom:{zoom:.1f}x", True, (120, 120, 140)),
            (w - 160, 10))

        if paused:
            screen.blit(
                self.font.render("── PAUSED ──", True, (255, 100, 100)),
                (w // 2 - 60, 8))

    def draw_bottom_bar(self, screen, sel, place_sys, shift_held: bool) -> None:
        y0 = TOP_BAR_H + self.play_h
        w = self.screen_w - SIDE_PANEL_W
        pygame.draw.rect(screen, C_BAR, (0, y0, w, BOTTOM_BAR_H))
        pygame.draw.line(screen, C_GRID_B, (0, y0), (w, y0), 2)

        x = 4
        btn_w = 74
        for bt in self.BUILDINGS:
            col = B_COLORS.get(bt, (100, 100, 100))
            r = pygame.Rect(x, y0 + 4, btn_w, BOTTOM_BAR_H - 8)
            pygame.draw.rect(screen, col, r)
            if sel == bt:
                pygame.draw.rect(screen, (255, 255, 150), r, 3)
            else:
                pygame.draw.rect(screen, (200, 200, 200, 60), r, 1)
            key = B_KEYS.get(bt, "?")
            screen.blit(
                self.fontS.render(f"[{key}]{bt[:7]}", True, (255, 255, 255)),
                (x + 2, y0 + 6))
            screen.blit(
                self.fontS.render(f"{B_COSTS.get(bt, '?')}$", True, (200, 200, 200)),
                (x + 2, y0 + 22))
            x += btn_w + 3

        # Hint
        hint = ""
        if sel == "belt":
            hint = f"Q/E: rotate ({place_sys.belt_dir})"
        elif sel == "inserter":
            hint = f"Q/E: rotate ({place_sys.inserter_dir})"
        elif sel == "assembler":
            hint = f"Q/E: recipe ({place_sys.assembler_recipe})"
        elif sel == "splitter":
            hint = f"Q/E: rotate ({place_sys.splitter_dir})"
        elif sel == "merger":
            hint = f"Q/E: rotate ({place_sys.merger_dir})"
        if shift_held:
            hint += "  [SHIFT] auto-build"
        if hint:
            screen.blit(self.fontS.render(hint, True, (180, 180, 180)),
                        (x + 6, y0 + 10))

    def draw_pause_overlay(self, screen) -> None:
        ov = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 140))
        screen.blit(ov, (0, 0))
        t = self.fontL.render("PAUSED  (P to resume)", True, (220, 220, 230))
        screen.blit(t, t.get_rect(center=(self.screen_w // 2, self.screen_h // 2)))

    def draw_win_screen(self, screen) -> None:
        ov = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 180))
        screen.blit(ov, (0, 0))
        lines = [
            "🚀  ROCKET LAUNCHED!  🚀",
            "You built the factory!",
            "Press ESC to continue",
        ]
        cy = self.screen_h // 2 - 30
        for line in lines:
            t = self.fontL.render(line, True, (255, 220, 80))
            screen.blit(t, t.get_rect(center=(self.screen_w // 2, cy)))
            cy += 40

    def draw_notifications(self, screen, notifications: list[dict]) -> None:
        y = TOP_BAR_H + self.play_h - 80
        for n in reversed(notifications[-5:]):
            if n["t"] <= 0:
                continue
            alpha = int(min(255, n["t"] * 120))
            s = pygame.Surface((350, 22), pygame.SRCALPHA)
            s.fill((40, 40, 60, alpha))
            t = self.fontS.render(n["text"], True, (220, 255, 180))
            s.blit(t, (6, 4))
            screen.blit(s, (10, y))
            y -= 24