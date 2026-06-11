import time
import random
import math
import pygame
from constants import (
    TILE_SIZE, TILE_COLORS, TILE_LABELS, B_COLORS,
    C_GRID, C_HL, C_HL_ERR, C_PROG_BG, C_PROG_FG,
    C_PARTICLE, ITEM_COLORS, ITEM_SHAPES,
    TOP_BAR_H, BELT_DELTA, C_FOG,
)

_STATUS_DOT = {
    "working": (80, 220, 100), "waiting": (255, 200, 40),
    "no_power": (255, 60, 60), "idle": (70, 70, 85),
}


class WorldRenderer:
    def __init__(self, screen):
        self.screen      = screen
        self.fontS       = pygame.font.SysFont("consolas,monospace", 10)
        self.show_grid   = True
        self.fog_enabled = False

    def draw_tiles(self, gmap, cam_x, cam_y, vp_x, vp_y):
        sx = max(0, cam_x // TILE_SIZE)
        sy = max(0, cam_y // TILE_SIZE)
        ex = min(sx + vp_x + 2, gmap.width)
        ey = min(sy + vp_y + 2, gmap.height)

        for ty in range(sy, ey):
            for tx in range(sx, ex):
                tile = gmap.tiles[ty][tx]
                rx   = tx * TILE_SIZE - cam_x
                ry   = ty * TILE_SIZE - cam_y + TOP_BAR_H

                # Fog of war
                if self.fog_enabled and not tile.revealed:
                    pygame.draw.rect(self.screen, C_FOG, (rx, ry, TILE_SIZE, TILE_SIZE))
                    continue

                # Base tile color
                c = TILE_COLORS.get(tile.tile_type, TILE_COLORS.get("grass", (45, 95, 45)))
                if (tx + ty) % 2 == 0:
                    c = tuple(min(255, ch + 12) for ch in c)
                pygame.draw.rect(self.screen, c, (rx, ry, TILE_SIZE, TILE_SIZE))

                if self.show_grid:
                    pygame.draw.rect(self.screen, C_GRID, (rx, ry, TILE_SIZE, TILE_SIZE), 1)

                # Tile label
                lbl = TILE_LABELS.get(tile.tile_type, "")
                if lbl:
                    self.screen.blit(self.fontS.render(lbl, True, (190, 192, 205)), (rx + 2, ry + 2))

                # Deposit depletion bar
                if tile.is_resource() and tile.max_deposit > 0:
                    pct = tile.deposit_pct
                    if pct < 1.0:
                        bw  = max(0, int((TILE_SIZE - 4) * pct))
                        col = (80, 220, 100) if pct > 0.3 else (255, 200, 40) if pct > 0.1 else (255, 60, 60)
                        pygame.draw.rect(self.screen, (40, 42, 55),
                                         (rx + 2, ry + TILE_SIZE - 5, TILE_SIZE - 4, 3))
                        if bw > 0:
                            pygame.draw.rect(self.screen, col,
                                             (rx + 2, ry + TILE_SIZE - 5, bw, 3))

    def draw_buildings(self, gmap, cam_x, cam_y):
        for b in gmap.buildings:
            rx  = b.x * TILE_SIZE - cam_x
            ry  = b.y * TILE_SIZE - cam_y + TOP_BAR_H

            # Cull off-screen
            if rx < -TILE_SIZE or rx > self.screen.get_width() + TILE_SIZE:
                continue
            if ry < TOP_BAR_H - TILE_SIZE or ry > self.screen.get_height() + TILE_SIZE:
                continue

            col = B_COLORS.get(b.btype, (140, 140, 140))
            pygame.draw.rect(self.screen, col, (rx + 1, ry + 1, TILE_SIZE - 2, TILE_SIZE - 2))
            pygame.draw.rect(self.screen, (255, 255, 255), (rx + 1, ry + 1, TILE_SIZE - 2, TILE_SIZE - 2), 1)

            label = b.btype[:6].capitalize()
            self.screen.blit(self.fontS.render(label, True, (255, 255, 255)), (rx + 2, ry + 1))

            if b.btype == "belt":
                self._belt_anim(b, rx, ry)

            if b.btype in ("furnace", "assembler"):
                pct = getattr(b, "progress_pct", 0)
                if pct > 0:
                    pw = int((TILE_SIZE - 4) * pct)
                    pygame.draw.rect(self.screen, C_PROG_BG,
                                     (rx + 2, ry + TILE_SIZE - 6, TILE_SIZE - 4, 4))
                    pygame.draw.rect(self.screen, C_PROG_FG,
                                     (rx + 2, ry + TILE_SIZE - 6, pw, 4))

            if b.btype == "storage" and hasattr(b, "fill_pct"):
                bw = int((TILE_SIZE - 4) * b.fill_pct)
                pygame.draw.rect(self.screen, C_PROG_BG,
                                 (rx + 2, ry + TILE_SIZE - 6, TILE_SIZE - 4, 4))
                pygame.draw.rect(self.screen, (80, 160, 255),
                                 (rx + 2, ry + TILE_SIZE - 6, bw, 4))

            if b.btype == "coal_generator" and hasattr(b, "fuel"):
                self.screen.blit(self.fontS.render(f"⛽{b.fuel}", True, (255, 220, 80)),
                                 (rx + 2, ry + TILE_SIZE - 14))

            # Status dot
            status = getattr(b, "status", None)
            if status and status in _STATUS_DOT:
                sc = _STATUS_DOT[status]
                pygame.draw.circle(self.screen, sc, (rx + TILE_SIZE - 5, ry + 5), 3)

    def _belt_anim(self, belt, rx, ry):
        ts = TILE_SIZE
        pygame.draw.rect(self.screen, (62, 64, 82), (rx + 2, ry + 2, ts - 4, ts - 4))
        offset = (time.time() * 28) % 8
        d  = belt.direction
        cx = rx + ts // 2
        cy = ry + ts // 2 + 2

        if d in ("right", "left"):
            off = offset if d == "right" else -offset
            for i in range(-2, 5):
                xp = rx + 4 + i * 8 + int(off) % 8
                if rx + 3 < xp < rx + ts - 3:
                    pygame.draw.line(self.screen, (95, 98, 120),
                                     (xp, ry + 4), (xp, ry + ts - 4), 1)
        else:
            off = offset if d == "down" else -offset
            for i in range(-2, 5):
                yp = ry + 4 + i * 8 + int(off) % 8
                if ry + 3 < yp < ry + ts - 3:
                    pygame.draw.line(self.screen, (95, 98, 120),
                                     (rx + 4, yp), (rx + ts - 4, yp), 1)

        arrows = {
            "right": [(cx - 5, cy - 4), (cx - 5, cy + 4), (cx + 5, cy)],
            "left":  [(cx + 5, cy - 4), (cx + 5, cy + 4), (cx - 5, cy)],
            "down":  [(cx - 4, cy - 5), (cx + 4, cy - 5), (cx, cy + 5)],
            "up":    [(cx - 4, cy + 5), (cx + 4, cy + 5), (cx, cy - 5)],
        }
        pygame.draw.polygon(self.screen, (170, 175, 200), arrows[d])

    def draw_belt_items(self, gmap, cam_x, cam_y):
        for b in gmap.buildings:
            if b.btype not in ("belt", "underground_belt"):
                continue
            if not getattr(b, "items", None):
                continue
            dx, dy = BELT_DELTA.get(getattr(b, "direction", "right"), (1, 0))
            for bi in b.items:
                prog = getattr(bi, "progress", 0.0)
                name = getattr(bi, "name", str(bi))
                bx = b.x * TILE_SIZE - cam_x + TILE_SIZE / 2 + dx * prog * TILE_SIZE
                by = b.y * TILE_SIZE - cam_y + TOP_BAR_H + TILE_SIZE / 2 + dy * prog * TILE_SIZE
                ic = ITEM_COLORS.get(name, (200, 200, 60))
                shape = ITEM_SHAPES.get(name, "circle")
                ix, iy = int(bx), int(by)

                if shape == "square":
                    pygame.draw.rect(self.screen, ic, (ix - 4, iy - 4, 8, 8))
                    pygame.draw.rect(self.screen, (255, 255, 255), (ix - 4, iy - 4, 8, 8), 1)
                elif shape == "rect":
                    pygame.draw.rect(self.screen, ic, (ix - 5, iy - 3, 10, 6))
                    pygame.draw.rect(self.screen, (255, 255, 255), (ix - 5, iy - 3, 10, 6), 1)
                elif shape == "diamond":
                    pts = [(ix, iy - 5), (ix + 5, iy), (ix, iy + 5), (ix - 5, iy)]
                    pygame.draw.polygon(self.screen, ic, pts)
                    pygame.draw.polygon(self.screen, (255, 255, 255), pts, 1)
                elif shape == "line":
                    pygame.draw.line(self.screen, ic, (ix - 5, iy), (ix + 5, iy), 3)
                elif shape == "star":
                    for angle in range(0, 360, 72):
                        rad = math.radians(angle)
                        px = ix + int(5 * math.cos(rad))
                        py = iy + int(5 * math.sin(rad))
                        pygame.draw.line(self.screen, ic, (ix, iy), (px, py), 1)
                    pygame.draw.circle(self.screen, ic, (ix, iy), 3)
                else:
                    pygame.draw.circle(self.screen, ic, (ix, iy), 5)
                    pygame.draw.circle(self.screen, (255, 255, 255), (ix, iy), 5, 1)

        # Inserter held items
        for b in gmap.buildings:
            if b.btype == "inserter" and getattr(b, "held_item", None):
                dx, dy = BELT_DELTA.get(b.direction, (1, 0))
                cxf = b.x * TILE_SIZE - cam_x + TILE_SIZE / 2
                cyf = b.y * TILE_SIZE - cam_y + TOP_BAR_H + TILE_SIZE / 2
                ox = dx * b.swing * 10
                oy = dy * b.swing * 10
                ic = ITEM_COLORS.get(b.held_item, (200, 200, 60))
                pygame.draw.rect(self.screen, ic,
                                 (int(cxf + ox - 4), int(cyf + oy - 4), 8, 8))

        # Robot dots
        for b in gmap.buildings:
            if b.btype == "robot_port" and hasattr(b, "robots"):
                for robot in b.robots:
                    rx_ = int(robot.x * TILE_SIZE - cam_x + TILE_SIZE / 2)
                    ry_ = int(robot.y * TILE_SIZE - cam_y + TOP_BAR_H + TILE_SIZE / 2)
                    col = (80, 220, 255) if robot.cargo else (80, 120, 180)
                    pygame.draw.circle(self.screen, col, (rx_, ry_), 4)

    def draw_miner_particles(self, gmap, cam_x, cam_y):
        for b in gmap.buildings:
            if b.btype != "miner":
                continue
            for p in getattr(b, "particles", []):
                alpha = int(max(0, min(255, p["t"] * 255)))
                if alpha <= 0:
                    continue
                px_ = b.x * TILE_SIZE - cam_x + TILE_SIZE // 2 + random.randint(-6, 6)
                py_ = b.y * TILE_SIZE - cam_y + TOP_BAR_H + 4
                s = pygame.Surface((4, 4), pygame.SRCALPHA)
                s.fill((C_PARTICLE[0], C_PARTICLE[1], C_PARTICLE[2], alpha))
                self.screen.blit(s, (px_, py_))

    def draw_highlight(self, mx, my, cam_x, cam_y, gmap, play_h):
        if not (TOP_BAR_H <= my < TOP_BAR_H + play_h):
            return
        hx = (mx + cam_x) // TILE_SIZE
        hy = (my - TOP_BAR_H + cam_y) // TILE_SIZE
        if not (0 <= hx < gmap.width and 0 <= hy < gmap.height):
            return
        occ = gmap.get_building(hx, hy) is not None
        s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        s.fill(C_HL_ERR if occ else C_HL)
        self.screen.blit(s, (hx * TILE_SIZE - cam_x, hy * TILE_SIZE - cam_y + TOP_BAR_H))