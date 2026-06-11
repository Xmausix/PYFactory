import random
import pygame
from constants import TOP_BAR_H


class ParticleSystem:
    def __init__(self):
        self.particles: list[dict] = []

    def emit_smoke(self, x, y, cam_x, cam_y):
        self.particles.append({
            "x": x * 32 - cam_x + random.randint(4, 28),
            "y": y * 32 - cam_y + TOP_BAR_H + 28,
            "vx": random.uniform(-0.3, 0.3),
            "vy": -random.uniform(0.5, 1.5),
            "t": random.uniform(0.6, 1.2),
            "type": "smoke",
        })

    def emit_spark(self, x, y, cam_x, cam_y):
        for _ in range(4):
            self.particles.append({
                "x": x * 32 - cam_x + 16,
                "y": y * 32 - cam_y + TOP_BAR_H + 16,
                "vx": random.uniform(-2.5, 2.5),
                "vy": random.uniform(-2.5, 2.5),
                "t": random.uniform(0.3, 0.7),
                "type": "spark",
            })

    def emit_rocket(self, x, y, cam_x, cam_y):
        for _ in range(12):
            self.particles.append({
                "x": x * 32 - cam_x + random.randint(0, 32),
                "y": y * 32 - cam_y + TOP_BAR_H + 32,
                "vx": random.uniform(-3, 3),
                "vy": -random.uniform(2, 6),
                "t": random.uniform(1.0, 2.5),
                "type": "rocket",
            })

    def emit_rain(self, screen_w, screen_h):
        self.particles.append({
            "x": random.randint(0, screen_w),
            "y": -5,
            "vx": random.uniform(-0.5, 0.5),
            "vy": random.uniform(4, 8),
            "t": random.uniform(1.0, 3.0),
            "type": "rain",
        })

    def update(self, dt):
        for p in self.particles:
            p["t"] -= dt
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["type"] == "rocket":
                p["vy"] -= dt * 2
        self.particles = [p for p in self.particles if p["t"] > 0]

    def draw(self, screen):
        for p in self.particles:
            alpha = int(max(0, min(255, p["t"] * 200)))
            if p["type"] == "smoke":
                s = pygame.Surface((5, 5), pygame.SRCALPHA)
                s.fill((200, 200, 200, alpha))
                screen.blit(s, (int(p["x"]), int(p["y"])))
            elif p["type"] == "spark":
                s = pygame.Surface((3, 3), pygame.SRCALPHA)
                s.fill((255, 200, 80, alpha))
                screen.blit(s, (int(p["x"]), int(p["y"])))
            elif p["type"] == "rocket":
                s = pygame.Surface((6, 6), pygame.SRCALPHA)
                s.fill((255, 120, 40, alpha))
                screen.blit(s, (int(p["x"]), int(p["y"])))
            elif p["type"] == "rain":
                pygame.draw.line(screen, (100, 140, 200, min(180, alpha)),
                                 (int(p["x"]), int(p["y"])),
                                 (int(p["x"] + p["vx"]), int(p["y"] + 3)), 1)

    def clear(self):
        self.particles.clear()