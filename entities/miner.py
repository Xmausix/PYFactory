class Miner:
    btype           = "miner"
    PRODUCTION_TIME = 2.0
    MAX_BUFFER      = 8

    def __init__(self, x: int, y: int):
        self.x              = x
        self.y              = y
        self.timer          = 0.0
        self.output_buffer: list[str] = []
        self.particles:     list[dict] = []
        self.powered        = True
        self.status         = "idle"
        self.module: str | None = None
        self.efficiency     = 1.0

    def update(self, dt: float, gmap) -> None:
        if not self.powered:
            self.status = "no_power"
            return
        tile = gmap.get_tile(self.x, self.y)
        if not tile.is_resource() or tile.is_depleted():
            self.status = "idle"
            return
        if len(self.output_buffer) >= self.MAX_BUFFER:
            self.status = "waiting"
            return
        speed = self._speed_mult()
        self.timer += dt * speed
        self.status = "working"
        if self.timer >= self.PRODUCTION_TIME:
            self.timer -= self.PRODUCTION_TIME
            resource = tile.extract()
            if resource:
                self.output_buffer.append(resource)
                self.particles.append({"t": 1.0})
        self.particles = [{"t": p["t"] - dt} for p in self.particles if p["t"] > 0]

    def _speed_mult(self) -> float:
        from constants import MODULE_TYPES
        if self.module and self.module in MODULE_TYPES:
            return MODULE_TYPES[self.module].get("speed_mult", 1.0)
        return 1.0

    def pop_output(self) -> str | None:
        return self.output_buffer.pop(0) if self.output_buffer else None

    def accept_item(self, item: str, _from=None) -> bool:
        return False

    def serialize(self) -> dict:
        return {
            "type": "miner", "x": self.x, "y": self.y,
            "output_buffer": self.output_buffer,
            "timer": self.timer, "module": self.module,
        }