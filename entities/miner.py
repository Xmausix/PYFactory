from constants import BELT_DIRS, BELT_DELTA


class Miner:
    """Extracts resources from the tile beneath (1 item / 2s)."""
    btype = "miner"
    PRODUCTION_TIME = 2.0
    MAX_BUFFER = 5

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.timer = 0.0
        self.output_buffer: list[str] = []
        self.particles: list[dict] = []
        self.powered = True
        self.status = "waiting"  # working / waiting / no_power

    def update(self, dt: float, gmap) -> None:
        if not self.powered:
            self.status = "no_power"
            return
        tile = gmap.get_tile(self.x, self.y)
        if tile.is_resource():
            if len(self.output_buffer) < self.MAX_BUFFER:
                self.timer += dt
                self.status = "working"
                if self.timer >= self.PRODUCTION_TIME:
                    self.timer -= self.PRODUCTION_TIME
                    self.output_buffer.append(tile.resource_name())
                    self.particles.append({"t": 1.0})
            else:
                self.status = "waiting"
        else:
            self.status = "waiting"

        self.particles = [
            {"t": p["t"] - dt} for p in self.particles if p["t"] > 0
        ]

    def pop_output(self) -> str | None:
        return self.output_buffer.pop(0) if self.output_buffer else None

    def serialize(self) -> dict:
        return {
            "type": "miner",
            "x": self.x,
            "y": self.y,
            "output_buffer": self.output_buffer,
        }