import random
import time
from constants import WEATHER_TYPES


class WeatherSystem:
    def __init__(self):
        self.current     = "clear"
        self.timer       = 0.0
        self.duration    = 120.0
        self._last_change = time.time()

    def update(self, dt: float, gmap) -> None:
        self.timer += dt
        if self.timer >= self.duration:
            self.timer    = 0.0
            self.current  = random.choice(list(WEATHER_TYPES.keys()))
            cfg           = WEATHER_TYPES[self.current]
            lo, hi        = cfg["duration"]
            self.duration = random.uniform(lo, hi)
            for b in gmap.buildings:
                if b.btype == "solar_panel" and hasattr(b, "weather_mult"):
                    b.weather_mult = cfg["solar_mult"]

    @property
    def info(self) -> dict:
        return WEATHER_TYPES.get(self.current, WEATHER_TYPES["clear"])

    def serialize(self) -> dict:
        return {"current": self.current, "timer": self.timer, "duration": self.duration}

    def deserialize(self, data: dict) -> None:
        self.current  = data.get("current", "clear")
        self.timer    = data.get("timer", 0.0)
        self.duration = data.get("duration", 120.0)