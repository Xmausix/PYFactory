import pygame
from constants import (TILE_COLORS, B_COLORS, TOP_BAR_H,
                       TILE_SIZE, SIDE_PANEL_W)


class Minimap:
    MM_W = 150
    MM_H = 0  # calculated

    def __init__(self, gmap):
        self.gmap = gmap
        self.enabled = True
        self.MM_H = int(self.MM_W * gmap.height / gmap.width)

    def draw(self, screen: pygame.Surface, cam_x: int, cam_y: int,
             screen_w: int, screen_h: int, play_h: int) -> None:
        if not self.enabled:
            return

        g = self.gmap
        mm_w, mm_h = self.MM_W, self.MM_H
        mm_x = screen_w - mm_w - 10
        mm_y = TOP_BAR_H + 30

        # Background
        bg = pygame.Surface((mm_w + 4, mm_h + 4))
        bg.fill((15, 15, 25))
        screen.blit(bg, (mm_x - 2, mm_y - 2))
        pygame.draw.rect(screen, (80, 80, 100),
                         (mm_x - 2, mm_y - 2, mm_w + 4, mm_h + 4), 1)

        tw = mm_w / g.width
        th = mm_h / g.height

        # Tiles
        for y in range(g.height):
            for x in range(g.width):
                t = g.tiles[y][x]
                c = TILE_COLORS.get(t.tile_type, TILE_COLORS["grass"])
                px = int(mm_x + x * tw)
                py = int(mm_y + y * th)
                pw = max(1, int(tw))
                ph = max(1, int(th))
                pygame.draw.rect(screen, c, (px, py, pw, ph))

        # Buildings
        for b in g.buildings:
            c = B_COLORS.get(b.btype, (255, 255, 255))
            px = int(mm_x + b.x * tw)
            py = int(mm_y + b.y * th)
            pygame.draw.rect(screen, c, (px, py, max(2, int(tw)), max(2, int(th))))

        # Viewport rect
        vx = mm_x + (cam_x / (g.width * TILE_SIZE)) * mm_w
        vy = mm_y + (cam_y / (g.height * TILE_SIZE)) * mm_h
        vw = (screen_w - SIDE_PANEL_W) / (g.width * TILE_SIZE) * mm_w
        vh = play_h / (g.height * TILE_SIZE) * mm_h
        pygame.draw.rect(screen, (255, 255, 0), (vx, vy, vw, vh), 2)

        # Label
        font = pygame.font.SysFont("consolas,monospace", 10)
        screen.blit(font.render("MAP", True, (150, 150, 170)), (mm_x, mm_y - 14))