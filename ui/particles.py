import random
import pygame
from constants import C_PARTICLE, TOP_BAR_H


class ParticleSystem:
    def __init__(self):
        self.particles: list = []

    def emit_smoke(self, x: int, y: int, cam_x: int, cam_y: int) -> None:
        self.particles.append({
            "x": x * 32 - cam_x + random.randint(4, 28),
            "y": y * 32 - cam_y + TOP_BAR_H + 28,
            "vx": random.uniform(-0.3, 0.3),
            "vy": -random.uniform(0.5, 1.5),
            "t": random.uniform(0.6, 1.2),
            "type": "smoke",
        })

    def emit_spark(self, x: int, y: int, cam_x: int, cam_y: int) -> None:
        for _ in range(3):
            self.particles.append({
                "x": x * 32 - cam_x + 16,
                "y": y * 32 - cam_y + TOP_BAR_H + 16,
                "vx": random.uniform(-2, 2),
                "vy": random.uniform(-2, 2),
                "t": random.uniform(0.3, 0.6),
                "type": "spark",
            })

    def update(self, dt: float) -> None:
        for p in self.particles:
            p["t"] -= dt
            p["x"] += p["vx"]
            p["y"] += p["vy"]
        self.particles = [p for p in self.particles if p["t"] > 0]

    def draw(self, screen: pygame.Surface) -> None:
        for p in self.particles:
            alpha = int(max(0, min(255, p["t"] * 200)))
            if p["type"] == "smoke":
                s = pygame.Surface((4, 4), pygame.SRCALPHA)
                s.fill((200, 200, 200, alpha))
                screen.blit(s, (int(p["x"]), int(p["y"])))
            elif p["type"] == "spark":
                s = pygame.Surface((3, 3), pygame.SRCALPHA)
                s.fill((255, 200, 80, alpha))
                screen.blit(s, (int(p["x"]), int(p["y"])))

    def clear(self) -> None:
        self.particles = []