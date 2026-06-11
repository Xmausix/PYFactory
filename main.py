"""
Factory Automation
==================
Main entry point. Handles game loop, events, window management.

Controls:
  WASD / Arrows  — camera pan
  1-0            — select building
  Q/E            — rotate / cycle recipe
  Left-click     — place building
  Right-click    — remove building
  Shift+click    — auto-build chain
  F5             — save
  F9             — load
  P              — pause
  TAB            — toggle info panel
  R              — research tree
  M              — minimap
  C              — clear particles
  F11            — fullscreen
  +/- / Scroll   — zoom
  ESC            — deselect / back to menu
"""

import sys
import random
import pygame

from constants import (
    TILE_SIZE, MAP_W, MAP_H, FPS_TARGET,
    ZOOM_LEVELS, DEFAULT_ZOOM_IDX,
    TOP_BAR_H, BOTTOM_BAR_H, SIDE_PANEL_W,
    C_BG, B_KEYS,
)
from world import GameMap
from systems import (Economy, EnergySystem, ProductionSystem,
                     PlacementSystem, StatisticsSystem,
                     QuestSystem, ResearchSystem)
from ui import (WorldRenderer, Minimap, HUD, InfoPanel,
                ParticleSystem, MainMenu, ResearchUI)
from utils import save_game, load_game


def _compute_layout(zoom: float, fullscreen: bool):
    """Return (screen_w, screen_h, play_w, play_h, viewport_x, viewport_y)."""
    info = pygame.display.Info()
    if fullscreen:
        sw = info.current_w
        sh = info.current_h
    else:
        sw = int(min(info.current_w * 0.9, 1280))
        sh = int(min(info.current_h * 0.9, 800))

    play_w = sw - SIDE_PANEL_W
    play_h = sh - TOP_BAR_H - BOTTOM_BAR_H
    vp_x = max(10, int(play_w / (TILE_SIZE * zoom)))
    vp_y = max(10, int(play_h / (TILE_SIZE * zoom)))
    return sw, sh, play_w, play_h, vp_x, vp_y


class Game:
    def __init__(self, seed: int | None = None):
        self.seed = seed if seed is not None else random.randint(0, 99999)
        self.fullscreen = False
        self.zoom_idx = DEFAULT_ZOOM_IDX
        self.zoom = ZOOM_LEVELS[self.zoom_idx]

        self._init_display()
        self._init_world()
        self._init_systems()
        self._init_ui()

        self.cam_x = 0
        self.cam_y = 0
        self.cam_spd = TILE_SIZE * 2
        self.sel: str | None = None
        self.paused = False
        self.shift_held = False
        self.show_info = True
        self.running = True
        self.game_won = False

        load_game(self.gmap, self.econ, self.research)

    # ── Initialisation ────────────────────────────────────────────────────

    def _init_display(self) -> None:
        sw, sh, pw, ph, vx, vy = _compute_layout(self.zoom, self.fullscreen)
        self.screen_w = sw
        self.screen_h = sh
        self.play_w = pw
        self.play_h = ph
        self.viewport_x = vx
        self.viewport_y = vy

        flags = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
        self.screen = pygame.display.set_mode((sw, sh), flags)
        pygame.display.set_caption("Factory Automation")
        self.clock = pygame.time.Clock()

    def _init_world(self) -> None:
        self.gmap = GameMap(MAP_W, MAP_H, self.seed)

    def _init_systems(self) -> None:
        self.econ     = Economy(200)
        self.energy   = EnergySystem(self.gmap)
        self.stats    = StatisticsSystem()
        self.research = ResearchSystem(self.econ)
        self.quests   = QuestSystem(self.gmap, self.econ, self.stats)
        self.placer   = PlacementSystem(self.gmap, self.econ)
        self.prod     = ProductionSystem(
            self.gmap, self.econ, self.stats, self.quests)

    def _init_ui(self) -> None:
        self.renderer    = WorldRenderer(self.screen)
        self.minimap     = Minimap(self.gmap)
        self.hud         = HUD(self.screen_w, self.screen_h, self.play_h)
        self.info_panel  = InfoPanel(self.screen_w, self.screen_h)
        self.particles   = ParticleSystem()
        self.research_ui = ResearchUI(self.screen_w, self.screen_h)

    def _resize(self, w: int, h: int) -> None:
        self.screen_w = w
        self.screen_h = h
        self.play_w = w - SIDE_PANEL_W
        self.play_h = h - TOP_BAR_H - BOTTOM_BAR_H
        self.viewport_x = max(10, int(self.play_w / (TILE_SIZE * self.zoom)))
        self.viewport_y = max(10, int(self.play_h / (TILE_SIZE * self.zoom)))
        self._clamp_camera()
        self._init_ui()

    def _toggle_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        flags = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
        sw, sh, pw, ph, vx, vy = _compute_layout(self.zoom, self.fullscreen)
        self.screen = pygame.display.set_mode((sw, sh), flags)
        self._resize(sw, sh)

    def _clamp_camera(self) -> None:
        max_cx = max(0, self.gmap.width * TILE_SIZE - self.play_w)
        max_cy = max(0, self.gmap.height * TILE_SIZE - self.play_h)
        self.cam_x = max(0, min(self.cam_x, max_cx))
        self.cam_y = max(0, min(self.cam_y, max_cy))

    # ── World coords ──────────────────────────────────────────────────────

    def _mouse_tile(self, mx: int, my: int) -> tuple[int, int]:
        wx = (mx + self.cam_x) // TILE_SIZE
        wy = (my - TOP_BAR_H + self.cam_y) // TILE_SIZE
        return wx, wy

    def _in_playfield(self, mx: int, my: int) -> bool:
        return (0 <= mx < self.play_w and
                TOP_BAR_H <= my < TOP_BAR_H + self.play_h)

    # ── Events ────────────────────────────────────────────────────────────

    def handle_events(self) -> None:
        mx, my = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False

            elif ev.type == pygame.VIDEORESIZE:
                self._resize(ev.w, ev.h)

            elif ev.type == pygame.KEYDOWN:
                self._on_keydown(ev)

            elif ev.type == pygame.KEYUP:
                if ev.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    self.shift_held = False

            elif ev.type == pygame.MOUSEBUTTONDOWN:
                self._on_mousedown(ev, mx, my)

            elif ev.type == pygame.MOUSEWHEEL:
                self._zoom_change(1 if ev.y > 0 else -1)

    def _on_keydown(self, ev: pygame.event.Event) -> None:
        self.shift_held = bool(pygame.key.get_mods() & pygame.KMOD_SHIFT)

        # Research UI swallows keys
        if self.research_ui.visible:
            if ev.key in (pygame.K_r, pygame.K_ESCAPE):
                self.research_ui.toggle()
            return

        # Camera
        spd = self.cam_spd
        if ev.key in (pygame.K_w, pygame.K_UP):
            self.cam_y = max(0, self.cam_y - spd)
        elif ev.key in (pygame.K_s, pygame.K_DOWN):
            self.cam_y = min(
                max(0, self.gmap.height * TILE_SIZE - self.play_h),
                self.cam_y + spd)
        elif ev.key in (pygame.K_a, pygame.K_LEFT):
            self.cam_x = max(0, self.cam_x - spd)
        elif ev.key in (pygame.K_d, pygame.K_RIGHT):
            self.cam_x = min(
                max(0, self.gmap.width * TILE_SIZE - self.play_w),
                self.cam_x + spd)

        # Building selection
        for bt, k in B_KEYS.items():
            try:
                if ev.key == pygame.key.key_code(k):
                    self.sel = bt
            except Exception:
                pass

        if ev.key == pygame.K_ESCAPE:
            self.sel = None

        # Rotation / recipe
        if ev.key == pygame.K_q:
            self._rotate(-1)
        elif ev.key == pygame.K_e:
            self._rotate(1)

        # Game controls
        if ev.key == pygame.K_p:
            self.paused = not self.paused
        if ev.key == pygame.K_F5:
            save_game(self.gmap, self.econ, self.research)
        if ev.key == pygame.K_F9:
            load_game(self.gmap, self.econ, self.research)
        if ev.key == pygame.K_TAB:
            self.show_info = not self.show_info
        if ev.key == pygame.K_r:
            self.research_ui.toggle()
        if ev.key == pygame.K_m:
            self.minimap.enabled = not self.minimap.enabled
        if ev.key == pygame.K_c:
            self.particles.clear()
        if ev.key == pygame.K_F11:
            self._toggle_fullscreen()
        if ev.key in (pygame.K_EQUALS, pygame.K_PLUS):
            self._zoom_change(1)
        if ev.key == pygame.K_MINUS:
            self._zoom_change(-1)

    def _rotate(self, step: int) -> None:
        if self.sel == "belt":
            self.placer.rotate_belt(step)
        elif self.sel == "inserter":
            self.placer.rotate_inserter(step)
        elif self.sel == "assembler":
            self.placer.cycle_recipe(step)
        elif self.sel == "splitter":
            self.placer.rotate_splitter(step)
        elif self.sel == "merger":
            self.placer.rotate_merger(step)

    def _on_mousedown(self, ev: pygame.event.Event, mx: int, my: int) -> None:
        # Research UI
        if self.research_ui.handle_click((mx, my), self.research):
            return

        wx, wy = self._mouse_tile(mx, my)

        if ev.button == 1 and self._in_playfield(mx, my):
            if self.shift_held:
                self.placer.auto_build(wx, wy)
            else:
                self.placer.place(wx, wy, self.sel)
        elif ev.button == 3 and self._in_playfield(mx, my):
            self.placer.remove(wx, wy)

    def _zoom_change(self, delta: int) -> None:
        self.zoom_idx = max(0, min(len(ZOOM_LEVELS) - 1, self.zoom_idx + delta))
        self.zoom = ZOOM_LEVELS[self.zoom_idx]
        self.viewport_x = max(10, int(self.play_w / (TILE_SIZE * self.zoom)))
        self.viewport_y = max(10, int(self.play_h / (TILE_SIZE * self.zoom)))
        self._clamp_camera()

    # ── Update ────────────────────────────────────────────────────────────

    def update(self, dt: float) -> None:
        if self.paused:
            return

        self.prod.update(dt)
        self.energy.update()
        self.research.update(dt, self.gmap)
        self.quests.update()
        self.quests.tick_notifications(dt)
        self.particles.update(dt)

        # Emit particles for active smelters
        for b in self.gmap.buildings:
            if b.btype == "smelter" and b.proc_item and random.random() < 0.25:
                self.particles.emit_smoke(b.x, b.y, self.cam_x, self.cam_y)

        # Check win
        if not self.game_won:
            for q in self.quests.quests:
                if q.title == "Rocket Launch" and q.completed:
                    self.game_won = True

    # ── Draw ──────────────────────────────────────────────────────────────

    def draw(self) -> None:
        self.screen.fill(C_BG)

        # Clip to playfield
        clip = pygame.Rect(0, TOP_BAR_H, self.play_w, self.play_h)
        self.screen.set_clip(clip)

        self.renderer.screen = self.screen
        self.renderer.draw_tiles(
            self.gmap, self.cam_x, self.cam_y,
            self.viewport_x, self.viewport_y, self.screen_w)
        self.renderer.draw_buildings(self.gmap, self.cam_x, self.cam_y)
        self.renderer.draw_belt_items(self.gmap, self.cam_x, self.cam_y)
        self.renderer.draw_miner_particles(self.gmap, self.cam_x, self.cam_y)
        self.renderer.draw_highlight(
            *pygame.mouse.get_pos(), self.cam_x, self.cam_y,
            self.gmap, self.play_h)

        self.screen.set_clip(None)

        # Particles (global, can be outside playfield clip)
        self.particles.draw(self.screen)

        # HUD
        self.hud.screen_w = self.screen_w
        self.hud.screen_h = self.screen_h
        self.hud.play_h = self.play_h
        self.hud.draw_top_bar(
            self.screen, self.econ, self.energy,
            self.paused, int(self.clock.get_fps()), self.zoom)
        self.hud.draw_bottom_bar(
            self.screen, self.sel, self.placer, self.shift_held)
        self.hud.draw_notifications(
            self.screen, self.quests.pop_notifications())

        # Side panel
        mx, my = pygame.mouse.get_pos()
        hovered = None
        if self._in_playfield(mx, my):
            wx, wy = self._mouse_tile(mx, my)
            hovered = self.gmap.get_building(wx, wy)
        self.info_panel.screen_w = self.screen_w
        self.info_panel.screen_h = self.screen_h
        self.info_panel.draw(
            self.screen, self.econ, self.energy,
            self.stats, self.quests, self.research,
            hovered, self.show_info)

        # Minimap
        self.minimap.draw(
            self.screen, self.cam_x, self.cam_y,
            self.screen_w, self.screen_h, self.play_h)

        # Research UI overlay
        self.research_ui.screen_w = self.screen_w
        self.research_ui.screen_h = self.screen_h
        self.research_ui.draw(self.screen, self.research)

        # Overlays
        if self.paused:
            self.hud.draw_pause_overlay(self.screen)
        if self.game_won:
            self.hud.draw_win_screen(self.screen)

        pygame.display.flip()

    # ── Main Loop ─────────────────────────────────────────────────────────

    def run(self) -> None:
        while self.running:
            dt = min(self.clock.tick(FPS_TARGET) / 1000.0, 0.05)
            self.handle_events()
            self.update(dt)
            self.draw()
        save_game(self.gmap, self.econ, self.research)
        pygame.quit()
        sys.exit()


# ── Entry point with main menu ────────────────────────────────────────────


def run_menu() -> None:
    pygame.init()
    info = pygame.display.Info()
    sw = min(info.current_w, 1024)
    sh = min(info.current_h, 640)
    screen = pygame.display.set_mode((sw, sh), pygame.RESIZABLE)
    pygame.display.set_caption("Factory Automation")
    clock = pygame.time.Clock()
    menu = MainMenu(sw, sh)
    fullscreen = False

    while True:
        dt = clock.tick(60) / 1000.0
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.VIDEORESIZE:
                sw, sh = ev.w, ev.h
                screen = pygame.display.set_mode((sw, sh), pygame.RESIZABLE)
                menu = MainMenu(sw, sh)
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_F11:
                fullscreen = not fullscreen
                flags = pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE
                info = pygame.display.Info()
                if fullscreen:
                    screen = pygame.display.set_mode(
                        (info.current_w, info.current_h), flags)
                else:
                    screen = pygame.display.set_mode((1024, 640), flags)
                menu = MainMenu(screen.get_width(), screen.get_height())

            action = menu.handle_event(ev)
            if action == "new_game":
                pygame.display.quit()
                pygame.display.init()
                g = Game(seed=random.randint(0, 99999))
                g.run()
                return
            elif action == "load_game":
                pygame.display.quit()
                pygame.display.init()
                g = Game()
                g.run()
                return
            elif action == "quit":
                pygame.quit()
                sys.exit()

        menu.update(dt)
        menu.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    run_menu()