from constants import POLLUTION_SOURCES, POLLUTION_DECAY, MAX_POLLUTION


class PollutionSystem:
    def __init__(self):
        self.level = 0.0

    def update(self, dt: float, gmap) -> None:
        gen = sum(POLLUTION_SOURCES.get(b.btype, 0) for b in gmap.buildings
                  if getattr(b, "status", "") == "working")
        self.level += gen * dt * 0.01
        self.level -= POLLUTION_DECAY * dt
        self.level  = max(0.0, min(MAX_POLLUTION, self.level))

    @property
    def pct(self) -> float:
        return self.level / MAX_POLLUTION

    def serialize(self) -> dict:
        return {"level": self.level}

    def deserialize(self, data: dict) -> None:
        self.level = data.get("level", 0.0)