import random
from constants import DISASTER_TYPES


class DisasterSystem:
    def __init__(self):
        self.notifications: list[dict] = []
        self._timer = 0.0

    def update(self, dt: float, gmap, pollution_pct: float) -> None:
        self._timer += dt
        if self._timer < 10.0:
            return
        self._timer = 0.0
        mult = 1.0 + pollution_pct * 2.0
        for d in DISASTER_TYPES:
            if random.random() < d["chance"] * mult:
                self._trigger(d, gmap)

    def _trigger(self, disaster: dict, gmap) -> None:
        target = disaster["target"]
        candidates = [b for b in gmap.buildings if (target == "any" or b.btype == target)]
        if not candidates:
            return
        victim = random.choice(candidates)
        if hasattr(victim, "jammed"):
            victim.jammed = True
        elif hasattr(victim, "active"):
            victim.active = False
        self.notifications.append({"text": f"⚠ {disaster['name']} at ({victim.x},{victim.y})", "t": 6.0})

    def tick_notifications(self, dt: float) -> None:
        for n in self.notifications:
            n["t"] -= dt
        self.notifications = [n for n in self.notifications if n["t"] > 0]