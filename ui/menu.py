import pygame
import random


class MainMenu:
    OPTIONS = ["New Game", "Load Game", "Settings", "Quit"]

    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.selected = 0
        self.font     = pygame.font.SysFont("consolas,monospace", 38, bold=True)
        self.fontM    = pygame.font.SysFont("consolas,monospace", 24, bold=True)
        self.fontS    = pygame.font.SysFont("consolas,monospace", 13)
        self.particles: list[dict] = []
        self._ptimer  = 0.0

    def update(self, dt):
        self._ptimer += dt
        if self._ptimer > 0.04:
            self._ptimer = 0.0
            self.particles.append({
                "x": random.randint(0, self.screen_w),
                "y": self.screen_h + 5,
                "vx": random.uniform(-0.2, 0.2),
                "vy": -random.uniform(0.4, 2.0),
                "t": random.uniform(3.0, 7.0),
                "size": random.randint(2, 5),
                "c": random.choice([
                    (255, 180, 60), (80, 180, 255),
                    (100, 255, 140), (255, 100, 80)]),
            })
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["t"] -= dt
        self.particles = [p for p in self.particles if p["t"] > 0 and p["y"] > -10]

    def _btn_rect(self, index: int) -> pygame.Rect:
        btn_w = 320
        btn_h = 52
        gap   = 12
        total_h = len(self.OPTIONS) * btn_h + (len(self.OPTIONS) - 1) * gap
        start_y = self.screen_h // 2 - total_h // 2 + 40
        x = self.screen_w // 2 - btn_w // 2
        y = start_y + index * (btn_h + gap)
        return pygame.Rect(x, y, btn_w, btn_h)

    def draw(self, screen):
        screen.fill((12, 12, 22))

        # Particles
        for p in self.particles:
            alpha = int(min(255, p["t"] * 45))
            s = pygame.Surface((p["size"], p["size"]), pygame.SRCALPHA)
            s.fill((*p["c"], alpha))
            screen.blit(s, (int(p["x"]), int(p["y"])))

        # Title
        title = self.font.render("FACTORY AUTOMATION", True, (255, 205, 60))
        screen.blit(title, title.get_rect(
            center=(self.screen_w // 2, self.screen_h // 4)))
        sub = self.fontS.render(
            "Build. Automate. Launch the Rocket.", True, (150, 155, 195))
        screen.blit(sub, sub.get_rect(
            center=(self.screen_w // 2, self.screen_h // 4 + 44)))

        # Buttons
        mx, my = pygame.mouse.get_pos()
        for i, opt in enumerate(self.OPTIONS):
            rect    = self._btn_rect(i)
            hovered = rect.collidepoint(mx, my)
            sel     = i == self.selected or hovered

            # Background
            bg = (50, 52, 78) if sel else (32, 34, 52)
            pygame.draw.rect(screen, bg, rect, border_radius=6)

            # Border
            bc = (255, 225, 60) if sel else (60, 62, 85)
            pygame.draw.rect(screen, bc, rect, 2, border_radius=6)

            # Text
            color = (255, 225, 60) if sel else (170, 175, 200)
            pre   = "▶  " if sel else "   "
            t     = self.fontM.render(f"{pre}{opt}", True, color)
            screen.blit(t, t.get_rect(center=rect.center))

        # Hint
        hint = self.fontS.render(
            "↑↓ navigate  •  Enter / Click select  •  F11 fullscreen",
            True, (80, 82, 105))
        screen.blit(hint, hint.get_rect(
            center=(self.screen_w // 2, self.screen_h - 28)))

    def handle_event(self, event) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.OPTIONS)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.OPTIONS)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self._action(self.selected)

        elif event.type == pygame.MOUSEMOTION:
            for i in range(len(self.OPTIONS)):
                if self._btn_rect(i).collidepoint(event.pos):
                    self.selected = i
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in range(len(self.OPTIONS)):
                    if self._btn_rect(i).collidepoint(event.pos):
                        return self._action(i)

        return None

    def _action(self, index: int) -> str:
        return self.OPTIONS[index].lower().replace(" ", "_")