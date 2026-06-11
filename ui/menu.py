import pygame
import sys
import random
from constants import C_BG, C_TXT


class MainMenu:
    """Main menu with New Game / Load / Quit options."""

    OPTIONS = ["New Game", "Load Game", "Quit"]

    def __init__(self, screen_w: int, screen_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.font  = pygame.font.SysFont("consolas,monospace", 36, bold=True)
        self.fontM = pygame.font.SysFont("consolas,monospace", 22, bold=True)
        self.fontS = pygame.font.SysFont("consolas,monospace", 14)
        self.selected = 0
        self.particles: list[dict] = []
        self._spawn_timer = 0.0

    def _spawn_particle(self) -> None:
        self.particles.append({
            "x": random.randint(0, self.screen_w),
            "y": self.screen_h + 5,
            "vy": -random.uniform(0.5, 2.0),
            "vx": random.uniform(-0.3, 0.3),
            "t": random.uniform(3.0, 6.0),
            "size": random.randint(2, 5),
            "color": random.choice([
                (255, 180, 60), (80, 180, 255),
                (100, 255, 140), (255, 100, 80)
            ]),
        })

    def update(self, dt: float) -> None:
        self._spawn_timer += dt
        if self._spawn_timer > 0.05:
            self._spawn_timer = 0.0
            self._spawn_particle()
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["t"] -= dt
        self.particles = [p for p in self.particles if p["t"] > 0 and p["y"] > -10]

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((15, 15, 25))

        # Particles
        for p in self.particles:
            alpha = int(min(255, p["t"] * 50))
            s = pygame.Surface((p["size"], p["size"]), pygame.SRCALPHA)
            s.fill((*p["color"], alpha))
            screen.blit(s, (int(p["x"]), int(p["y"])))

        # Title
        title = self.font.render("FACTORY AUTOMATION", True, (255, 200, 60))
        screen.blit(title, title.get_rect(center=(self.screen_w // 2, self.screen_h // 3)))
        sub = self.fontS.render("Build your automated factory empire", True, (160, 160, 200))
        screen.blit(sub, sub.get_rect(center=(self.screen_w // 2, self.screen_h // 3 + 44)))

        # Options
        cy = self.screen_h // 2
        for i, opt in enumerate(self.OPTIONS):
            selected = i == self.selected
            color = (255, 220, 60) if selected else (180, 180, 200)
            prefix = "▶ " if selected else "  "
            t = self.fontM.render(f"{prefix}{opt}", True, color)
            r = t.get_rect(center=(self.screen_w // 2, cy))
            if selected:
                pygame.draw.rect(screen, (40, 40, 70),
                                 r.inflate(30, 8))
            screen.blit(t, r)
            cy += 50

        # Controls hint
        hint = self.fontS.render("W/S or ↑↓ to navigate  •  Enter to select  •  F11 fullscreen",
                                 True, (100, 100, 120))
        screen.blit(hint, hint.get_rect(center=(self.screen_w // 2, self.screen_h - 30)))

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Returns action string or None."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.OPTIONS)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.OPTIONS)
            elif event.key == pygame.K_RETURN:
                return self.OPTIONS[self.selected].lower().replace(" ", "_")
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cy = self.screen_h // 2
            for i, opt in enumerate(self.OPTIONS):
                r = pygame.Rect(0, 0, 300, 40)
                r.center = (self.screen_w // 2, cy)
                if r.collidepoint(event.pos):
                    return opt.lower().replace(" ", "_")
                cy += 50
        return None