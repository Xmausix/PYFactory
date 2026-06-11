import time
import random
import pygame
from constants import (
    TILE_SIZE, TILE_COLORS, TILE_LABELS, B_COLORS,
    C_BG, C_GRID, C_HL, C_HL_ERR, C_DOT, C_DOT_B,
    C_PROG_BG, C_PROG_FG, C_PARTICLE, C_TXT,
    TOP_BAR_H, SIDE_PANEL_W, BELT_DELTA, ITEM_COLORS,
)


STATUS_DOT_COLORS = {
    "working":  (80, 220, 100),
    "waiting":  (255, 200, 40),
    "no_power": (255, 60, 60),
    "idle":     (80, 80, 80),
}


class WorldRenderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.fontS = pygame.font.SysFont("consolas,monospace", 11)
        self.font  = pygame.font.SysFont("consolas,monospace", 14, bold=True)

    def draw_tiles(self, gmap, cam_x: int, cam_y: int,
                   viewport_x: int, viewport_y: int,
                   screen_w: int) -> None:
        sx = cam_x // TILE_SIZE
        sy = cam_y // TILE_SIZE
        ex = min(sx + viewport_x + 2, gmap.width)
        ey = min(sy + viewport_y + 2, gmap.height)

        for ty in range(sy, ey):
            for tx in range(sx, ex):
                tile = gmap.tiles[ty][tx]
                rx = tx * TILE_SIZE - cam_x
                ry = ty * TILE_SIZE - cam_y + TOP_BAR_H
                c = TILE_COLORS.get(tile.tile_type, TILE_COLORS["grass"])
                if (tx + ty) % 2 == 0:
                    c = tuple(min(255, ch + 10) for ch in c)
                pygame.draw.rect(self.screen, c, (rx, ry, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(self.screen, C_GRID,
                                 (rx, ry, TILE_SIZE, TILE_SIZE), 1)
                lbl = TILE_LABELS.get(tile.tile_type, "")
                if lbl:
                    lc = (190, 190, 200)
                    self.screen.blit(
                        self.fontS.render(lbl, True, lc), (rx + 4, ry + 4))

    def draw_buildings(self, gmap, cam_x: int, cam_y: int) -> None:
        for b in gmap.buildings:
            rx = b.x * TILE_SIZE - cam_x
            ry = b.y * TILE_SIZE - cam_y + TOP_BAR_H
            col = B_COLORS.get(b.btype, (150, 150, 150))

            pygame.draw.rect(self.screen, col,
                             (rx + 1, ry + 1, TILE_SIZE - 2, TILE_SIZE - 2))
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (rx + 1, ry + 1, TILE_SIZE - 2, TILE_SIZE - 2), 1)

            label = b.btype[:6].capitalize()
            self.screen.blit(
                self.fontS.render(label, True, (255, 255, 255)),
                (rx + 3, ry + 2))

            if b.btype == "belt":
                self._draw_belt(b, rx, ry)
            if b.btype == "storage":
                self.screen.blit(
                    self.fontS.render(f"{len(b.items)}/{b.CAPACITY}", True, (255, 255, 255)),
                    (rx + 2, ry + TILE_SIZE - 14))
            if b.btype in ("smelter", "assembler") and b.proc_item:
                self._draw_progress(rx, ry, b.progress_pct)

            # Status dot
            status = getattr(b, "status", None)
            if status:
                sc = STATUS_DOT_COLORS.get(status, (120, 120, 120))
                pygame.draw.circle(
                    self.screen, sc,
                    (rx + TILE_SIZE - 5, ry + 5), 3)

    def _draw_belt(self, belt, rx: int, ry: int) -> None:
        pygame.draw.rect(self.screen, (65, 65, 85),
                         (rx + 2, ry + 2, TILE_SIZE - 4, TILE_SIZE - 4))
        offset = (time.time() * 24) % 8
        d = belt.direction
        cx = rx + TILE_SIZE // 2
        cy = ry + TILE_SIZE // 2 + 2

        if d in ("right", "left"):
            step = 8
            off = offset if d == "right" else -offset
            for i in range(-2, 5):
                xp = rx + 4 + i * step + int(off) % step
                if rx + 4 <= xp <= rx + TILE_SIZE - 4:
                    pygame.draw.line(self.screen, (100, 100, 125),
                                     (xp, ry + 4), (xp, ry + TILE_SIZE - 4), 1)
        else:
            step = 8
            off = offset if d == "down" else -offset
            for i in range(-2, 5):
                yp = ry + 4 + i * step + int(off) % step
                if ry + 4 <= yp <= ry + TILE_SIZE - 4:
                    pygame.draw.line(self.screen, (100, 100, 125),
                                     (rx + 4, yp), (rx + TILE_SIZE - 4, yp), 1)

        arrows = {
            "right": [(cx - 5, cy - 4), (cx - 5, cy + 4), (cx + 5, cy)],
            "left":  [(cx + 5, cy - 4), (cx + 5, cy + 4), (cx - 5, cy)],
            "down":  [(cx - 4, cy - 5), (cx + 4, cy - 5), (cx, cy + 5)],
            "up":    [(cx - 4, cy + 5), (cx + 4, cy + 5), (cx, cy - 5)],
        }
        pygame.draw.polygon(self.screen, (180, 180, 210), arrows[d])

    def _draw_progress(self, rx: int, ry: int, pct: float) -> None:
        pw = int((TILE_SIZE - 4) * pct)
        pygame.draw.rect(self.screen, C_PROG_BG,
                         (rx + 2, ry + TILE_SIZE - 6, TILE_SIZE - 4, 4))
        pygame.draw.rect(self.screen, C_PROG_FG,
                         (rx + 2, ry + TILE_SIZE - 6, pw, 4))

    def draw_belt_items(self, gmap, cam_x: int, cam_y: int) -> None:
        """Draw items on belts with smooth movement."""
        for b in gmap.buildings:
            if b.btype != "belt" or not b.items:
                continue
            dx, dy = BELT_DELTA[b.direction]
            for belt_item in b.items:
                prog = belt_item.progress
                base_x = b.x * TILE_SIZE - cam_x + TILE_SIZE / 2
                base_y = b.y * TILE_SIZE - cam_y + TOP_BAR_H + TILE_SIZE / 2
                ox = dx * prog * TILE_SIZE
                oy = dy * prog * TILE_SIZE
                ix = int(base_x + ox)
                iy = int(base_y + oy)
                ic = ITEM_COLORS.get(belt_item.name, C_DOT)
                pygame.draw.circle(self.screen, ic, (ix, iy), 5)
                pygame.draw.circle(self.screen, (255, 255, 255), (ix, iy), 5, 1)

        # Inserter held items
        for b in gmap.buildings:
            if b.btype == "inserter" and b.held_item:
                dx, dy = BELT_DELTA[b.direction]
                cx = b.x * TILE_SIZE - cam_x + TILE_SIZE / 2
                cy = b.y * TILE_SIZE - cam_y + TOP_BAR_H + TILE_SIZE / 2
                ox = dx * b.swing * 10
                oy = dy * b.swing * 10
                ic = ITEM_COLORS.get(b.held_item, C_DOT)
                pygame.draw.rect(self.screen, ic,
                                 (int(cx + ox - 4), int(cy + oy - 4), 8, 8))
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (int(cx + ox - 4), int(cy + oy - 4), 8, 8), 1)

    def draw_miner_particles(self, gmap, cam_x: int, cam_y: int) -> None:
        for b in gmap.buildings:
            if b.btype != "miner":
                continue
            for p in b.particles:
                alpha = int(max(0, min(255, p["t"] * 255)))
                if alpha <= 0:
                    continue
                px = b.x * TILE_SIZE - cam_x + TILE_SIZE // 2 + random.randint(-6, 6)
                py = b.y * TILE_SIZE - cam_y + TOP_BAR_H + 4
                s = pygame.Surface((4, 4), pygame.SRCALPHA)
                s.fill((C_PARTICLE[0], C_PARTICLE[1], C_PARTICLE[2], alpha))
                self.screen.blit(s, (px, py))

    def draw_highlight(self, mx: int, my: int,
                       cam_x: int, cam_y: int, gmap,
                       play_h: int) -> None:
        if not (TOP_BAR_H <= my < TOP_BAR_H + play_h):
            return
        hx = (mx + cam_x) // TILE_SIZE
        hy = (my - TOP_BAR_H + cam_y) // TILE_SIZE
        if not (0 <= hx < gmap.width and 0 <= hy < gmap.height):
            return
        hr = pygame.Rect(
            hx * TILE_SIZE - cam_x,
            hy * TILE_SIZE - cam_y + TOP_BAR_H,
            TILE_SIZE, TILE_SIZE)
        occ = gmap.get_building(hx, hy) is not None
        s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        s.fill(C_HL_ERR if occ else C_HL)
        self.screen.blit(s, hr.topleft)