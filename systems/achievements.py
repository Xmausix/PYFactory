from constants import ACHIEVEMENT_DEFS


class AchievementSystem:
    def __init__(self):
        self.unlocked: set[str]    = set()
        self.notifications: list[dict] = []

    def check(self, gmap, econ, stats, pollution) -> None:
        checks = {
            "first_ore":     lambda: stats.items_per_minute("iron_ore") > 0 or stats.items_per_minute("copper_ore") > 0,
            "first_factory": lambda: gmap.count_type("furnace") >= 1 and gmap.count_type("market") >= 1,
            "earn_1000":     lambda: econ.total_earned >= 1000,
            "earn_10000":    lambda: econ.total_earned >= 10000,
            "first_train":   lambda: gmap.count_type("locomotive") >= 1,
            "first_robot":   lambda: gmap.count_type("robot_port") >= 1,
            "polluter":      lambda: pollution.pct >= 0.5,
            "eco_friendly":  lambda: gmap.count_type("coal_generator") == 0 and gmap.count_type("solar_panel") >= 3,
            "speed_demon":   lambda: stats.total_items_per_minute() >= 100,
            "rocket":        lambda: econ.total_earned >= 10000,
        }
        for a in ACHIEVEMENT_DEFS:
            aid = a["id"]
            if aid not in self.unlocked:
                check_fn = checks.get(aid)
                if check_fn and check_fn():
                    self.unlocked.add(aid)
                    self.notifications.append({"text": f"🏆 {a['icon']} {a['title']}", "t": 5.0})

    def tick_notifications(self, dt: float) -> None:
        for n in self.notifications:
            n["t"] -= dt
        self.notifications = [n for n in self.notifications if n["t"] > 0]

    def serialize(self) -> dict:
        return {"unlocked": list(self.unlocked)}

    def deserialize(self, data: dict) -> None:
        self.unlocked = set(data.get("unlocked", []))