import pygame
from constants import C_GRID_B, C_TXT, C_TXT_DIM, C_OK, C_ERR


class SettingsMenu:
    TABS = ["Graphics", "Controls", "Accessibility"]

    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.visible  = False
        self.tab      = 0
        self.font     = pygame.font.SysFont("consolas,monospace", 16, bold=True)
        self.fontS    = pygame.font.SysFont("consolas,monospace", 12)

        # Interactive state
        self._rows:       list[dict]       = []
        self._tab_rects:  list[pygame.Rect]= []
        self._dragging_slider: dict | None = None  # {"key","lo","hi","track_x","track_w"}

    def toggle(self):
        self.visible = not self.visible
        self._dragging_slider = None

    def _get_layout(self):
        W = min(620, self.screen_w - 40)
        H = min(540, self.screen_h - 40)
        rx = (self.screen_w - W) // 2
        ry = (self.screen_h - H) // 2
        return W, H, rx, ry


    def draw(self, screen, settings, keybinds=None):
        if not self.visible:
            return

        ov = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 210))
        screen.blit(ov, (0, 0))

        W, H, rx, ry = self._get_layout()
        pygame.draw.rect(screen, (22, 24, 38), (rx, ry, W, H), border_radius=8)
        pygame.draw.rect(screen, C_GRID_B, (rx, ry, W, H), 2, border_radius=8)

        # Title
        screen.blit(self.font.render("⚙  Settings", True, (200, 205, 240)),
                    (rx + 16, ry + 10))

        # Tabs
        self._tab_rects = []
        tab_y = ry + 36
        tw    = (W - 20) // len(self.TABS)
        mx, my = pygame.mouse.get_pos()

        for i, tab_name in enumerate(self.TABS):
            tr = pygame.Rect(rx + 10 + i * tw, tab_y, tw, 30)
            self._tab_rects.append(tr)
            hovered = tr.collidepoint(mx, my)
            active  = i == self.tab

            bg = (50, 52, 78) if active else ((40, 42, 62) if hovered else (30, 32, 48))
            pygame.draw.rect(screen, bg, tr, border_radius=4)
            bc = (120, 130, 200) if active else (50, 52, 70)
            pygame.draw.rect(screen, bc, tr, 2, border_radius=4)

            tc = (240, 245, 255) if active else ((200, 205, 220) if hovered else C_TXT_DIM)
            screen.blit(self.fontS.render(tab_name, True, tc),
                        (tr.x + 12, tr.y + 8))

        # Content
        self._rows = []
        content_y = tab_y + 38
        content_bottom = ry + H - 34

        if self.tab == 0:
            content_y = self._toggle_row(screen, rx, content_y, W, "Fullscreen",      "fullscreen",       settings)
            content_y = self._toggle_row(screen, rx, content_y, W, "VSync",           "vsync",            settings)
            content_y = self._toggle_row(screen, rx, content_y, W, "Show Grid",       "show_grid",        settings)
            content_y = self._toggle_row(screen, rx, content_y, W, "Show Minimap",    "show_minimap",     settings)
            content_y = self._toggle_row(screen, rx, content_y, W, "Show Particles",  "show_particles",   settings)
            content_y = self._toggle_row(screen, rx, content_y, W, "Item Labels",     "show_item_labels", settings)
            content_y = self._toggle_row(screen, rx, content_y, W, "Autosave",        "autosave",         settings)
            content_y += 8
            content_y = self._slider_row(screen, rx, content_y, W, "Camera Speed",    "camera_speed",     settings, 1, 20)

        elif self.tab == 1:
            screen.blit(self.font.render("Keybindings  —  click to rebind",
                                          True, (180, 185, 220)), (rx + 16, content_y))
            content_y += 26

            if keybinds and keybinds.is_rebinding:
                screen.blit(self.fontS.render(
                    f">>> Press any key for: {keybinds.rebinding_action} <<<",
                    True, (100, 255, 120)), (rx + 16, content_y))
                content_y += 22

            if keybinds:
                for action in sorted(keybinds.binds.keys()):
                    if content_y + 26 > content_bottom:
                        break
                    key_name = keybinds.binds.get(action, "?")
                    row_rect = pygame.Rect(rx + 12, content_y, W - 24, 24)
                    self._rows.append({
                        "rect": row_rect, "type": "keybind", "action": action
                    })

                    hovered = row_rect.collidepoint(mx, my)
                    bg = (42, 44, 62) if hovered else (28, 30, 44)
                    pygame.draw.rect(screen, bg, row_rect, border_radius=3)
                    pygame.draw.rect(screen, (55, 58, 75) if hovered else (40, 42, 55),
                                     row_rect, 1, border_radius=3)

                    screen.blit(self.fontS.render(action, True, C_TXT),
                                (row_rect.x + 8, row_rect.y + 5))

                    key_col = (255, 255, 140) if hovered else C_OK
                    key_bg  = (50, 52, 72) if hovered else (35, 37, 52)
                    key_rect = pygame.Rect(row_rect.right - 80, row_rect.y + 2, 72, 20)
                    pygame.draw.rect(screen, key_bg, key_rect, border_radius=3)
                    pygame.draw.rect(screen, (60, 62, 80), key_rect, 1, border_radius=3)
                    screen.blit(self.fontS.render(key_name, True, key_col),
                                (key_rect.x + 6, key_rect.y + 3))

                    content_y += 26

        elif self.tab == 2:
            content_y = self._toggle_row(screen, rx, content_y, W, "Colorblind Mode", "colorblind_mode", settings)
            content_y = self._toggle_row(screen, rx, content_y, W, "High Contrast",   "high_contrast",   settings)
            content_y += 8
            content_y = self._slider_row(screen, rx, content_y, W, "Font Size",       "font_size",       settings, 10, 20)

        # Close hint
        screen.blit(self.fontS.render(
            "[O] or [ESC] close  •  ←→ switch tabs  •  Click toggles/sliders",
            True, C_TXT_DIM), (rx + 12, ry + H - 24))

    def _toggle_row(self, screen, rx, y, W, label, key, settings) -> int:
        val      = settings.get(key, False)
        row_rect = pygame.Rect(rx + 12, y, W - 24, 32)
        self._rows.append({"rect": row_rect, "type": "toggle", "key": key})

        mx_, my_ = pygame.mouse.get_pos()
        hovered  = row_rect.collidepoint(mx_, my_)
        bg       = (42, 44, 62) if hovered else (28, 30, 44)
        pygame.draw.rect(screen, bg, row_rect, border_radius=3)
        pygame.draw.rect(screen, (55, 58, 75) if hovered else (40, 42, 55),
                         row_rect, 1, border_radius=3)

        screen.blit(self.fontS.render(label, True, C_TXT), (rx + 20, y + 9))

        # Toggle switch visual
        sw_x = rx + W - 72
        sw_y = y + 9
        sw_w = 40
        sw_h = 14
        track_col = C_OK if val else (60, 62, 80)
        pygame.draw.rect(screen, track_col, (sw_x, sw_y, sw_w, sw_h), border_radius=7)

        knob_x = sw_x + sw_w - 8 if val else sw_x + 8
        knob_col = (255, 255, 255) if val else (120, 122, 140)
        pygame.draw.circle(screen, knob_col, (knob_x, sw_y + 7), 6)

        return y + 36

    def _slider_row(self, screen, rx, y, W, label, key, settings, lo, hi) -> int:
        val = settings.get(key, lo)
        if isinstance(lo, float):
            val = float(val)
        else:
            val = int(val)

        row_rect = pygame.Rect(rx + 12, y, W - 24, 42)
        track_x  = rx + 20
        track_w  = W - 44
        track_y  = y + 28

        self._rows.append({
            "rect": row_rect, "type": "slider", "key": key,
            "lo": lo, "hi": hi, "track_x": track_x, "track_w": track_w
        })

        mx_, my_ = pygame.mouse.get_pos()
        hovered  = row_rect.collidepoint(mx_, my_)
        bg       = (42, 44, 62) if hovered else (28, 30, 44)
        pygame.draw.rect(screen, bg, row_rect, border_radius=3)
        pygame.draw.rect(screen, (55, 58, 75) if hovered else (40, 42, 55),
                         row_rect, 1, border_radius=3)

        # Label + value
        disp = f"{val:.1f}" if isinstance(lo, float) else str(val)
        screen.blit(self.fontS.render(f"{label}:  {disp}", True, C_TXT),
                    (rx + 20, y + 6))

        # Track
        pct = max(0.0, min(1.0, (val - lo) / max(0.001, hi - lo)))
        pygame.draw.rect(screen, (50, 52, 72),
                         (track_x, track_y, track_w, 8), border_radius=4)
        fill_w = int(track_w * pct)
        if fill_w > 0:
            pygame.draw.rect(screen, (80, 160, 255),
                             (track_x, track_y, fill_w, 8), border_radius=4)

        # Handle (knob)
        handle_x = track_x + int(track_w * pct)
        handle_y = track_y + 4

        # Highlight handle if being dragged
        is_dragging = (self._dragging_slider is not None
                       and self._dragging_slider.get("key") == key)
        handle_col  = (255, 255, 140) if is_dragging else (
            (220, 230, 255) if hovered else (180, 190, 220))
        handle_r    = 8 if is_dragging else 7

        pygame.draw.circle(screen, handle_col, (handle_x, handle_y), handle_r)
        pygame.draw.circle(screen, (100, 110, 150), (handle_x, handle_y), handle_r, 2)

        return y + 48

    # ── Event handling ────────────────────────────────────────────────────

    def handle_event(self, ev, settings, keybinds=None) -> bool:
        if not self.visible:
            return False

        # ── Slider dragging (continuous) ──────────────────────────────────
        if self._dragging_slider is not None:
            if ev.type == pygame.MOUSEMOTION:
                self._update_slider_drag(ev.pos, settings)
                return True
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self._update_slider_drag(ev.pos, settings)
                self._dragging_slider = None
                self._save(settings)
                return True
            return True  # consume all events during drag

        # ── Keyboard ─────────────────────────────────────────────────────
        if ev.type == pygame.KEYDOWN:
            if keybinds and keybinds.is_rebinding:
                if ev.key != pygame.K_ESCAPE:
                    keybinds.finish_rebind(ev.key)
                else:
                    keybinds._waiting_for = None
                return True
            if ev.key in (pygame.K_o, pygame.K_ESCAPE):
                self.visible = False
                self._save(settings)
                return True
            if ev.key == pygame.K_LEFT:
                self.tab = (self.tab - 1) % len(self.TABS)
                return True
            if ev.key == pygame.K_RIGHT:
                self.tab = (self.tab + 1) % len(self.TABS)
                return True
            return True  # consume all keys when open

        # ── Mouse click ──────────────────────────────────────────────────
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            # Tab click
            for i, tr in enumerate(self._tab_rects):
                if tr.collidepoint(ev.pos):
                    self.tab = i
                    return True

            # Row click
            for row in self._rows:
                if not row["rect"].collidepoint(ev.pos):
                    continue

                if row["type"] == "toggle":
                    key = row["key"]
                    settings[key] = not settings.get(key, False)
                    self._save(settings)
                    return True

                elif row["type"] == "slider":
                    # Start dragging
                    self._dragging_slider = row
                    self._update_slider_drag(ev.pos, settings)
                    return True

                elif row["type"] == "keybind" and keybinds:
                    keybinds.start_rebind(row["action"])
                    return True

            return True  # consume click even if missed

        # ── Scroll wheel on sliders ──────────────────────────────────────
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button in (4, 5):
            for row in self._rows:
                if row["type"] != "slider":
                    continue
                if row["rect"].collidepoint(ev.pos):
                    key = row["key"]
                    lo, hi = row["lo"], row["hi"]
                    delta = 1 if ev.button == 4 else -1
                    val = settings.get(key, lo)
                    if isinstance(lo, float) or isinstance(hi, float):
                        settings[key] = max(lo, min(hi, round(val + delta * 0.1, 1)))
                    else:
                        settings[key] = max(lo, min(hi, val + delta))
                    self._save(settings)
                    return True

        # Consume mousewheel events
        if ev.type == pygame.MOUSEWHEEL:
            return True

        # Consume mouse motion
        if ev.type == pygame.MOUSEMOTION:
            return True

        return True  # consume everything when settings open

    def _update_slider_drag(self, pos, settings):
        """Update slider value based on mouse position."""
        if self._dragging_slider is None:
            return
        row     = self._dragging_slider
        key     = row["key"]
        lo, hi  = row["lo"], row["hi"]
        track_x = row["track_x"]
        track_w = row["track_w"]

        click_x = pos[0] - track_x
        pct     = max(0.0, min(1.0, click_x / max(1, track_w)))

        if isinstance(lo, float) or isinstance(hi, float):
            settings[key] = round(lo + pct * (hi - lo), 1)
        else:
            settings[key] = int(lo + pct * (hi - lo))

    @staticmethod
    def _save(settings):
        from utils import save_settings
        save_settings(settings)

