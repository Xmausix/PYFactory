import random


class EventSystem:
    def __init__(self):
        self.active_event: dict | None = None
        self.timer       = 0.0
        self.event_timer = 0.0
        self.notifications: list[dict] = []

    def update(self, dt: float) -> None:
        self.timer += dt
        if self.active_event:
            self.event_timer -= dt
            if self.event_timer <= 0:
                self.active_event = None
        if self.timer >= random.uniform(120, 300) and not self.active_event:
            self.timer = 0.0
            self._spawn()

    def _spawn(self) -> None:
        events = [
            {"name": "Scientific Breakthrough", "effect": "research_boost", "mult": 1.5, "duration": 60},
            {"name": "Market Boom",             "effect": "price_boost",    "mult": 1.3, "duration": 45},
            {"name": "Efficiency Drive",        "effect": "speed_boost",    "mult": 1.2, "duration": 90},
        ]
        ev = random.choice(events)
        self.active_event = ev
        self.event_timer  = ev["duration"]
        self.notifications.append({"text": f"🌟 Event: {ev['name']} ({ev['duration']}s)", "t": 5.0})

    def get_mult(self, effect: str) -> float:
        if self.active_event and self.active_event["effect"] == effect:
            return self.active_event["mult"]
        return 1.0

    def tick_notifications(self, dt: float) -> None:
        for n in self.notifications:
            n["t"] -= dt
        self.notifications = [n for n in self.notifications if n["t"] > 0]