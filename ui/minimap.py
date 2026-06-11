import pygame
from constants import (TILE_COLORS, B_COLORS, TOP_BAR_H,
                        TILE_SIZE, SIDE_PANEL_W)


class Minimap:
    MM_W = 160

    def __init__(self, gmap):
        self.gmap    = gmap
        self.enabled = True
        self.MM_H    = int(self.MM_W * gmap.height / gmap.width)

    def draw(self, screen: pygame.Surface,
             cam_x: int, cam_y: int,
             screen_w: int, screen_h: int,
             play_h: int) -> None:
        if not self.enabled:
            return
        g       = self.gmap
        mm_w    = self.MM_W
        mm_h    = self.MM_H
        mm_x    = screen_w - SIDE_PANEL_W - mm_w - 6
        mm_y    = TOP_BAR_H + 6
        tw      = mm_w / g.width
        th      = mm_h / g.height

        # Background
        pygame.draw.rect(screen, (14, 14, 22),
                         (mm_x - 2, mm_y - 2, mm_w + 4, mm_h + 4))
        pygame.draw.rect(screen, (70, 72, 92),
                         (mm_x - 2, mm_y - 2, mm_w + 4, mm_h + 4), 1)

        # Tiles
        for y in range(g.height):
            for x in range(g.width):
                t  = g.tiles[y][x]
                c  = TILE_COLORS.get(t.tile_type, TILE_COLORS["grass"])
                pygame.draw.rect(screen, c,
                                 (int(mm_x + x * tw), int(mm_y + y * th),
                                  max(1, int(tw)), max(1, int(th))))

        # Buildings
        for b in g.buildings:
            c = B_COLORS.get(b.btype, (200, 200, 200))
            pygame.draw.rect(screen, c,
                             (int(mm_x + b.x * tw), int(mm_y + b.y * th),
                              max(2, int(tw)), max(2, int(th))))

        # Viewport rect
        play_w = screen_w - SIDE_PANEL_W
        vx     = mm_x + (cam_x / (g.width * TILE_SIZE)) * mm_w
        vy     = mm_y + (cam_y / (g.height * TILE_SIZE)) * mm_h
        vw     = (play_w / (g.width * TILE_SIZE)) * mm_w
        vh     = (play_h / (g.height * TILE_SIZE)) * mm_h
        pygame.draw.rect(screen, (255, 255, 0), (vx, vy, vw, vh), 1)

        # Label
        _f = pygame.font.SysFont("consolas,monospace", 10)
        screen.blit(_f.render("MAP (M)", True, (120, 120, 140)),
                    (mm_x, mm_y - 13))