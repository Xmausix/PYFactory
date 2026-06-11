"""
Factory Automation — Full Edition
==================================
Controls
--------
WASD / ↑↓←→        Camera pan (keyboard)
RMB + drag          Camera pan (mouse drag)
RMB click           Remove building
1-0, u j k t l b n Select building
Q / E               Rotate / cycle recipe
F                   Toggle underground belt mode
LMB                 Place building
LMB on building     Show building info
Shift+LMB           Auto-build chain
P / ESC             Pause menu
F5                  Save
F9                  Load
R                   Research tree
O                   Settings
M                   Toggle minimap
G                   Toggle grid
X                   Logistics overlay
I                   World statistics
H                   Achievements
C                   Clear particles
F11                 Toggle fullscreen
+/- / Scroll        Zoom
ESC                 Deselect / pause menu
"""

import sys
import random
import pygame

from constants import (
    TILE_SIZE, MAP_W, MAP_H, FPS_TARGET,
    ZOOM_LEVELS, DEFAULT_ZOOM_IDX,
    TOP_BAR_H, BOTTOM_BAR_H, SIDE_PANEL_W,
)
from world import GameMap
from systems import (
    Economy, EnergySystem, ProductionSystem,
    PlacementSystem, StatisticsSystem,
    QuestSystem, ResearchSystem, AutoSave,
    TrainSystem, RobotSystem, WeatherSystem,
    PollutionSystem, ContractSystem, AchievementSystem,
    FogOfWar, DynamicMarket, DisasterSystem,
    CompetitorSystem, EventSystem,
)
from ui import (
    WorldRenderer, Minimap, HUD, Dashboard,
    ParticleSystem, MainMenu, SettingsMenu,
    ResearchUI, RocketAnimation, BuildingInfoPanel,
    PauseMenu, LogisticsOverlay, WorldStatsUI,
    AchievementsUI, ContractsUI,
)
from utils import save_game, load_game, save_settings, load_settings, KeybindManager

def _layout(zoom, fullscreen):
    info = pygame.display.Info()
    if fullscreen:
        sw, sh = info.current_w, info.current_h
    else:
        sw = max(900, min(int(info.current_w * 0.88), 1600))
        sh = max(600, min(int(info.current_h * 0.88), 1000))
    pw = sw - SIDE_PANEL_W
    ph = sh - TOP_BAR_H - BOTTOM_BAR_H
    vx = max(8, int(pw / (TILE_SIZE * zoom)))
    vy = max(6, int(ph / (TILE_SIZE * zoom)))
    return sw, sh, pw, ph, vx, vy

class Game:
    def __init__(self, seed=None, settings=None, preset="normal"):
        from constants import DEFAULT_SETTINGS
        self.settings   = settings or dict(DEFAULT_SETTINGS)
        self.seed       = seed if seed is not None else random.randint(0, 99999)
        self.preset     = preset
        self.zoom_idx   = self.settings.get("zoom_idx", DEFAULT_ZOOM_IDX)
        self.zoom       = ZOOM_LEVELS[self.zoom_idx]
        self.fullscreen = self.settings.get("fullscreen", False)
        self.keybinds   = KeybindManager()

        self._init_display()
        self._init_world()
        self._init_systems()
        self._init_ui()
        self.cam_x       = 0
        self.cam_y       = 0
        self.cam_spd     = self.settings.get("camera_speed", 10) * TILE_SIZE
        self.sel: str | None = None
        self.paused      = False
        self.shift_held  = False
        self.running     = True
        self.game_won    = False
        self._rocket_started = False
        self._return_to_menu = False
        self._dragging   = False
        self._drag_sx    = 0
        self._drag_sy    = 0
        self._drag_cx    = 0
        self._drag_cy    = 0

        # Load saved game if present
        load_game(self.gmap, self.econ, self.research, self.quests,
                  self.energy, self.weather, self.pollution,
                  self.contracts, self.achievements)

    def _init_display(self):
        sw, sh, pw, ph, vx, vy = _layout(self.zoom, self.fullscreen)
        self.screen_w   = sw
        self.screen_h   = sh
        self.play_w     = pw
        self.play_h     = ph
        self.viewport_x = vx
        self.viewport_y = vy
        flags = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
        self.screen = pygame.display.set_mode((sw, sh), flags)
        pygame.display.set_caption("Factory Automation")
        self.clock = pygame.time.Clock()

    def _init_world(self):
        self.gmap = GameMap(MAP_W, MAP_H, self.seed, self.preset)

    def _init_systems(self):
        self.econ         = Economy(300)
        self.energy       = EnergySystem(self.gmap)
        self.stats        = StatisticsSystem()
        self.research     = ResearchSystem(self.econ)
        self.quests       = QuestSystem(self.gmap, self.econ, self.stats)
        self.contracts    = ContractSystem()
        self.placer       = PlacementSystem(self.gmap, self.econ)
        self.prod         = ProductionSystem(
            self.gmap, self.econ, self.stats, self.quests, self.contracts)
        self.trains       = TrainSystem(self.gmap)
        self.robots       = RobotSystem(self.gmap)
        self.weather      = WeatherSystem()
        self.pollution    = PollutionSystem()
        self.achievements = AchievementSystem()
        self.fog          = FogOfWar(self.gmap)
        self.disasters    = DisasterSystem()
        self.competitors  = CompetitorSystem()
        self.events       = EventSystem()
        self.autosave     = AutoSave(
            120.0 if self.settings.get("autosave", True) else 1e9)

    def _init_ui(self):
        self.renderer      = WorldRenderer(self.screen)
        self.renderer.show_grid   = self.settings.get("show_grid", True)
        self.renderer.fog_enabled = False
        self.minimap       = Minimap(self.gmap)
        self.minimap.enabled = self.settings.get("show_minimap", True)
        self.hud           = HUD(self.screen_w, self.screen_h, self.play_h)
        self.dashboard     = Dashboard(self.screen_w, self.screen_h)
        self.particles     = ParticleSystem()
        self.research_ui   = ResearchUI(self.screen_w, self.screen_h)
        self.settings_ui   = SettingsMenu(self.screen_w, self.screen_h)
        self.rocket_anim   = RocketAnimation(self.screen_w, self.screen_h)
        self.building_info = BuildingInfoPanel(self.screen_w, self.screen_h)
        self.pause_menu    = PauseMenu(self.screen_w, self.screen_h)
        self.overlay       = LogisticsOverlay()
        self.world_stats   = WorldStatsUI(self.screen_w, self.screen_h)
        self.achieve_ui    = AchievementsUI(self.screen_w, self.screen_h)
        self.contracts_ui  = ContractsUI()
    def _resize(self, w, h):
        self.screen_w   = w
        self.screen_h   = h
        self.play_w     = w - SIDE_PANEL_W
        self.play_h     = h - TOP_BAR_H - BOTTOM_BAR_H
        self.viewport_x = max(8, int(self.play_w / (TILE_SIZE * self.zoom)))
        self.viewport_y = max(6, int(self.play_h / (TILE_SIZE * self.zoom)))
        self._clamp_cam()
        self._init_ui()

    def _toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.settings["fullscreen"] = self.fullscreen
        sw, sh, *_ = _layout(self.zoom, self.fullscreen)
        flags = pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
        self.screen = pygame.display.set_mode((sw, sh), flags)
        self._resize(sw, sh)

    def _clamp_cam(self):
        max_x = max(0, self.gmap.width  * TILE_SIZE - self.play_w)
        max_y = max(0, self.gmap.height * TILE_SIZE - self.play_h)
        self.cam_x = int(max(0, min(self.cam_x, max_x)))
        self.cam_y = int(max(0, min(self.cam_y, max_y)))

    def _zoom_change(self, delta):
        self.zoom_idx   = max(0, min(len(ZOOM_LEVELS) - 1, self.zoom_idx + delta))
        self.zoom       = ZOOM_LEVELS[self.zoom_idx]
        self.viewport_x = max(8, int(self.play_w / (TILE_SIZE * self.zoom)))
        self.viewport_y = max(6, int(self.play_h / (TILE_SIZE * self.zoom)))
        self._clamp_cam()

    def _mouse_tile(self, mx, my):
        return (
            (mx + self.cam_x) // TILE_SIZE,
            (my - TOP_BAR_H + self.cam_y) // TILE_SIZE,
        )

    def _in_play(self, mx, my):
        return (0 <= mx < self.play_w
                and TOP_BAR_H <= my < TOP_BAR_H + self.play_h)

    def handle_events(self):
        mx, my = pygame.mouse.get_pos()
        if self._dragging:
            self.cam_x = self._drag_cx + (self._drag_sx - mx)
            self.cam_y = self._drag_cy + (self._drag_sy - my)
            self._clamp_cam()
        no_overlay = not any([
            self.pause_menu.visible,
            self.research_ui.visible,
            self.settings_ui.visible,
            self.world_stats.visible,
            self.achieve_ui.visible,
        ])
        if not self.paused and no_overlay:
            keys = pygame.key.get_pressed()
            spd  = self.cam_spd / FPS_TARGET
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.cam_y -= spd
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.cam_y += spd
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.cam_x -= spd
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.cam_x += spd
            self._clamp_cam()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
                continue

            if ev.type == pygame.VIDEORESIZE:
                self._resize(ev.w, ev.h)
                continue
            if self.rocket_anim.active:
                if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    if self.rocket_anim.finished:
                        self.rocket_anim.active = False
                continue
            if self.settings_ui.visible:
                consumed = self.settings_ui.handle_event(
                    ev, self.settings, self.keybinds)
                # Always apply settings changes
                if consumed:
                    self.renderer.show_grid = self.settings.get("show_grid", True)
                    self.minimap.enabled    = self.settings.get("show_minimap", True)
                    self.cam_spd = self.settings.get("camera_speed", 10) * TILE_SIZE
                continue  # ALWAYS consume when settings open
            if self.pause_menu.visible:
                action = self.pause_menu.handle_event(ev)
                if action == "resume":
                    self.paused = False
                elif action == "save_game":
                    self._do_save()
                elif action == "settings":
                    self.settings_ui.toggle()
                elif action == "main_menu":
                    self._return_to_menu = True
                    self.running = False
                elif action == "quit":
                    self.running = False
                continue  # ALWAYS consume when pause menu open
            if self.research_ui.visible:
                if ev.type == pygame.KEYDOWN:
                    if ev.key in (pygame.K_r, pygame.K_ESCAPE):
                        self.research_ui.toggle()
                elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.research_ui.handle_click(ev.pos, self.research)
                continue  # ALWAYS consume when research open

            if self.world_stats.visible:
                if ev.type == pygame.KEYDOWN:
                    if ev.key in (pygame.K_i, pygame.K_ESCAPE):
                        self.world_stats.toggle()
                continue  # ALWAYS consume when world stats open

            if self.achieve_ui.visible:
                if ev.type == pygame.KEYDOWN:
                    if ev.key in (pygame.K_h, pygame.K_ESCAPE):
                        self.achieve_ui.toggle()
                continue  # ALWAYS consume when achievements open


            if ev.type == pygame.KEYDOWN:
                self._on_keydown(ev)

            elif ev.type == pygame.KEYUP:
                if ev.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    self.shift_held = False

            elif ev.type == pygame.MOUSEBUTTONDOWN:
                # Right click → start camera drag
                if ev.button == 3:
                    self._dragging = True
                    self._drag_sx  = mx
                    self._drag_sy  = my
                    self._drag_cx  = self.cam_x
                    self._drag_cy  = self.cam_y

                # Scroll wheel → zoom
                elif ev.button == 4:
                    self._zoom_change(1)
                elif ev.button == 5:
                    self._zoom_change(-1)

                # Left click → place / select / info
                elif ev.button == 1:
                    if self._in_play(mx, my):
                        wx, wy = self._mouse_tile(mx, my)
                        existing = self.gmap.get_building(wx, wy)
                        if existing and self.sel is None:
                            # Click on building without tool → show info
                            self.building_info.show(existing)
                        else:
                            # Click with tool or on empty → place
                            self.building_info.hide()
                            if self.shift_held:
                                self.placer.auto_build(wx, wy)
                            else:
                                self.placer.place(wx, wy, self.sel)
                    else:
                        # Click outside playfield → close building info
                        self.building_info.hide()

            elif ev.type == pygame.MOUSEBUTTONUP:
                # Right click release → stop drag, maybe remove building
                if ev.button == 3 and self._dragging:
                    drag_dist = abs(mx - self._drag_sx) + abs(my - self._drag_sy)
                    self._dragging = False
                    # Short click (< 5px) → remove building
                    if drag_dist < 5 and self._in_play(mx, my):
                        wx, wy = self._mouse_tile(mx, my)
                        self.placer.remove(wx, wy)

            elif ev.type == pygame.MOUSEWHEEL:
                self._zoom_change(1 if ev.y > 0 else -1)

    def _on_keydown(self, ev):
        kb = self.keybinds
        self.shift_held = bool(pygame.key.get_mods() & pygame.KMOD_SHIFT)

        if ev.key == pygame.K_ESCAPE:
            if self.sel:
                self.sel = None
            elif self.building_info.visible:
                self.building_info.hide()
            else:
                self.pause_menu.toggle()
                self.paused = self.pause_menu.visible
            return

        from constants import B_KEYS
        non_building = {
            "rotate_left", "rotate_right", "toggle_ugb", "pause",
            "save", "load", "research", "settings", "minimap",
            "grid", "clear_particles", "fullscreen", "overlay",
            "world_stats", "achievements", "zoom_in", "zoom_out",
        }
        for bt, k in B_KEYS.items():
            if bt in non_building:
                continue
            if kb.is_key(bt, ev.key):
                self.sel = bt
                self.building_info.hide()
                return

        if kb.is_key("rotate_left", ev.key):
            self._rotate(-1)
            return
        if kb.is_key("rotate_right", ev.key):
            self._rotate(1)
            return
        if kb.is_key("toggle_ugb", ev.key):
            self.placer.toggle_ugb_mode()
            return
        if kb.is_key("pause", ev.key):
            self.pause_menu.toggle()
            self.paused = self.pause_menu.visible
            return
        if kb.is_key("save", ev.key):
            self._do_save()
            return
        if kb.is_key("load", ev.key):
            load_game(self.gmap, self.econ, self.research, self.quests,
                      self.energy, self.weather, self.pollution,
                      self.contracts, self.achievements)
            return
        if kb.is_key("research", ev.key):
            self.research_ui.toggle()
            return
        if kb.is_key("settings", ev.key):
            self.settings_ui.toggle()
            return
        if kb.is_key("minimap", ev.key):
            self.minimap.enabled = not self.minimap.enabled
            self.settings["show_minimap"] = self.minimap.enabled
            return
        if kb.is_key("grid", ev.key):
            self.renderer.show_grid = not self.renderer.show_grid
            self.settings["show_grid"] = self.renderer.show_grid
            return
        if kb.is_key("clear_particles", ev.key):
            self.particles.clear()
            return
        if kb.is_key("fullscreen", ev.key):
            self._toggle_fullscreen()
            return
        if kb.is_key("overlay", ev.key):
            self.overlay.toggle()
            return
        if kb.is_key("world_stats", ev.key):
            self.world_stats.toggle()
            return
        if kb.is_key("achievements", ev.key):
            self.achieve_ui.toggle()
            return
        if kb.is_key("zoom_in", ev.key):
            self._zoom_change(1)
            return
        if kb.is_key("zoom_out", ev.key):
            self._zoom_change(-1)
            return

    def _rotate(self, step):
        rotate_map = {
            "belt":              "rotate_belt",
            "underground_belt":  "rotate_belt",
            "inserter":          "rotate_inserter",
            "splitter":          "rotate_splitter",
            "priority_splitter": "rotate_splitter",
            "merger":            "rotate_merger",
            "rail":              "rotate_rail",
        }
        if self.sel == "assembler":
            self.placer.cycle_recipe(step)
        elif self.sel in rotate_map:
            getattr(self.placer, rotate_map[self.sel])(step)

    def update(self, dt):
        self.rocket_anim.update(dt)

        if self.paused:
            return

        self.prod.update(dt)
        self.energy.update(dt)
        self.research.update(dt, self.gmap)
        self.quests.update()
        self.quests.tick_notifications(dt)
        self.trains.update(dt)
        self.robots.update(dt)
        self.weather.update(dt, self.gmap)
        self.pollution.update(dt, self.gmap)
        self.contracts.update(dt)
        self.achievements.check(self.gmap, self.econ, self.stats, self.pollution)
        self.achievements.tick_notifications(dt)
        self.disasters.update(dt, self.gmap, self.pollution.pct)
        self.disasters.tick_notifications(dt)
        self.competitors.update(dt)
        self.events.update(dt)
        self.events.tick_notifications(dt)
        DynamicMarket.update(dt)
        self.particles.update(dt)

        # Emit particles
        if self.settings.get("show_particles", True):
            for b in self.gmap.buildings:
                if b.btype == "furnace" and getattr(b, "proc_item", None):
                    if random.random() < 0.2:
                        self.particles.emit_smoke(
                            b.x, b.y, self.cam_x, self.cam_y)
                if b.btype == "coal_generator" and getattr(b, "active", False):
                    if random.random() < 0.15:
                        self.particles.emit_spark(
                            b.x, b.y, self.cam_x, self.cam_y)
            if self.weather.current == "rain" and random.random() < 0.4:
                self.particles.emit_rain(self.screen_w, self.screen_h)

        # Autosave
        self.autosave.update(dt, self._do_save)

        # Win condition
        if not self.game_won:
            for q in self.quests.quests:
                if q.title == "Rocket Launch" and q.completed:
                    if not self._rocket_started:
                        self.game_won = True
                        self._rocket_started = True
                        self.rocket_anim.start()

    def _do_save(self):
        save_game(self.gmap, self.econ, self.research, self.quests,
                  self.energy, self.weather, self.pollution,
                  self.contracts, self.achievements)
        self.settings["zoom_idx"] = self.zoom_idx
        save_settings(self.settings)

    def draw(self):
        # Rocket animation takes full screen
        if self.rocket_anim.active:
            self.rocket_anim.draw(self.screen)
            pygame.display.flip()
            return

        self.screen.fill((18, 20, 28))
        clip = pygame.Rect(0, TOP_BAR_H, self.play_w, self.play_h)
        self.screen.set_clip(clip)

        self.renderer.screen = self.screen
        self.renderer.draw_tiles(
            self.gmap, self.cam_x, self.cam_y,
            self.viewport_x, self.viewport_y)
        self.renderer.draw_buildings(
            self.gmap, self.cam_x, self.cam_y)
        self.renderer.draw_belt_items(
            self.gmap, self.cam_x, self.cam_y)
        self.renderer.draw_miner_particles(
            self.gmap, self.cam_x, self.cam_y)

        # Logistics overlay
        self.overlay.draw(
            self.screen, self.gmap,
            self.cam_x, self.cam_y, self.play_h)

        # Hover highlight (only when not dragging)
        mx, my = pygame.mouse.get_pos()
        if not self._dragging:
            self.renderer.draw_highlight(
                mx, my, self.cam_x, self.cam_y,
                self.gmap, self.play_h)

        self.screen.set_clip(None)

        self.particles.draw(self.screen)

        self.hud.screen_w = self.screen_w
        self.hud.screen_h = self.screen_h
        self.hud.play_h   = self.play_h
        self.hud.draw_top_bar(
            self.screen, self.econ, self.energy,
            self.paused, int(self.clock.get_fps()), self.zoom)
        self.hud.draw_bottom_bar(
            self.screen, self.sel, self.placer, self.shift_held)

        # All notifications combined
        all_notifs = (
            self.quests.pop_notifications()
            + self.achievements.notifications
            + self.disasters.notifications
            + self.events.notifications
        )
        self.hud.draw_notifications(self.screen, all_notifs)

        weather_icons = {
            "clear": "☀", "rain": "🌧", "heat": "🔥",
            "wind": "💨", "storm": "⛈",
        }
        wi = weather_icons.get(self.weather.current, "?")
        wfont = pygame.font.SysFont("consolas,monospace", 11)
        self.screen.blit(
            wfont.render(f"{wi} {self.weather.current}", True, (180, 185, 210)),
            (self.screen_w - SIDE_PANEL_W - 100, 12))

        if self.pollution.level > 0:
            from constants import C_POLLUTION
            pb_x = self.screen_w - SIDE_PANEL_W - 100
            pb_y = TOP_BAR_H - 6
            pygame.draw.rect(self.screen, (40, 42, 55), (pb_x, pb_y, 80, 4))
            pygame.draw.rect(self.screen, C_POLLUTION,
                             (pb_x, pb_y, int(80 * self.pollution.pct), 4))

        hovered = None
        if self._in_play(mx, my) and not self._dragging:
            wx, wy  = self._mouse_tile(mx, my)
            hovered = self.gmap.get_building(wx, wy)
        self.dashboard.screen_w = self.screen_w
        self.dashboard.screen_h = self.screen_h
        self.dashboard.draw(
            self.screen, self.econ, self.energy,
            self.stats, self.quests, self.research,
            hovered, self.autosave.last_save_msg)

        self.minimap.draw(
            self.screen, self.cam_x, self.cam_y,
            self.screen_w, self.screen_h, self.play_h)

        self.building_info.screen_w = self.screen_w
        self.building_info.screen_h = self.screen_h
        self.building_info.draw(self.screen)

        self.research_ui.screen_w = self.screen_w
        self.research_ui.screen_h = self.screen_h
        self.research_ui.draw(self.screen, self.research)

        self.world_stats.screen_w = self.screen_w
        self.world_stats.screen_h = self.screen_h
        self.world_stats.draw(
            self.screen, self.gmap, self.econ, self.stats,
            self.pollution, self.weather, self.competitors)

        self.achieve_ui.screen_w = self.screen_w
        self.achieve_ui.screen_h = self.screen_h
        self.achieve_ui.draw(self.screen, self.achievements)

        self.settings_ui.screen_w = self.screen_w
        self.settings_ui.screen_h = self.screen_h
        self.settings_ui.draw(self.screen, self.settings, self.keybinds)

        self.pause_menu.screen_w = self.screen_w
        self.pause_menu.screen_h = self.screen_h
        self.pause_menu.draw(self.screen)

        if self.game_won and not self.rocket_anim.active:
            self.hud.draw_win_screen(self.screen)

        pygame.display.flip()


    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS_TARGET) / 1000.0, 0.05)
            self.handle_events()
            self.update(dt)
            self.draw()
        self._do_save()
        if self._return_to_menu:
            return "menu"
        pygame.quit()
        return "quit"


def run_menu():
    pygame.init()
    settings   = load_settings()
    fullscreen = settings.get("fullscreen", False)
    info       = pygame.display.Info()

    if fullscreen:
        sw, sh = info.current_w, info.current_h
        flags  = pygame.FULLSCREEN
    else:
        sw = max(900, min(int(info.current_w * 0.88), 1280))
        sh = max(600, min(int(info.current_h * 0.88), 800))
        flags = pygame.RESIZABLE

    screen = pygame.display.set_mode((sw, sh), flags)
    pygame.display.set_caption("Factory Automation")
    clock  = pygame.time.Clock()
    menu   = MainMenu(sw, sh)

    # Settings overlay reused in main menu
    settings_ui = SettingsMenu(sw, sh)
    keybinds    = KeybindManager()

    while True:
        dt = clock.tick(60) / 1000.0

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.VIDEORESIZE:
                sw, sh = ev.w, ev.h
                screen = pygame.display.set_mode((sw, sh), pygame.RESIZABLE)
                menu        = MainMenu(sw, sh)
                settings_ui = SettingsMenu(sw, sh)

            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_F11:
                fullscreen = not fullscreen
                settings["fullscreen"] = fullscreen
                save_settings(settings)
                info  = pygame.display.Info()
                flags = pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE
                dim   = ((info.current_w, info.current_h)
                         if fullscreen else (sw, sh))
                screen      = pygame.display.set_mode(dim, flags)
                sw, sh      = screen.get_size()
                menu        = MainMenu(sw, sh)
                settings_ui = SettingsMenu(sw, sh)


            if settings_ui.visible:
                settings_ui.screen_w = sw
                settings_ui.screen_h = sh
                settings_ui.handle_event(ev, settings, keybinds)
                continue  # consume all events when settings open


            action = menu.handle_event(ev)

            if action == "new_game":
                pygame.display.quit()
                pygame.display.init()
                result = Game(
                    seed=random.randint(0, 99999),
                    settings=settings
                ).run()
                if result == "menu":
                    return run_menu()
                return

            elif action == "load_game":
                pygame.display.quit()
                pygame.display.init()
                result = Game(settings=settings).run()
                if result == "menu":
                    return run_menu()
                return

            elif action == "settings":
                settings_ui.toggle()  # ← OTWIERA USTAWIENIA

            elif action == "quit":
                pygame.quit()
                sys.exit()

        menu.update(dt)
        menu.draw(screen)

        # Draw settings overlay ON TOP of menu
        if settings_ui.visible:
            settings_ui.screen_w = sw
            settings_ui.screen_h = sh
            settings_ui.draw(screen, settings, keybinds)

        pygame.display.flip()

# Entry Point

if __name__ == "__main__":
    pygame.init()
    run_menu()