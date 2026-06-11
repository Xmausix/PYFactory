from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Quest:
    title:        str
    description:  str
    check:        Callable[[], bool]
    reward_money: int  = 0
    completed:    bool = False


class QuestSystem:
    def __init__(self, gmap, econ, stats):
        self.gmap   = gmap
        self.econ   = econ
        self.stats  = stats
        self._produced: dict[str, int] = {}
        self.notifications: list[dict] = []
        self.quests: list[Quest] = []
        self._build()

    def _build(self) -> None:
        g, e = self.gmap, self.econ
        self.quests = [
            Quest("First Steps",     "Place a Miner",          lambda: g.count_type("miner") >= 1,            20),
            Quest("Power Up",        "Build a Coal Generator", lambda: g.count_type("coal_generator") >= 1,   30),
            Quest("Iron Age",        "Produce 50 Iron Ore",    lambda: self._produced.get("iron_ore", 0) >= 50, 50),
            Quest("Merchant",        "Earn 500$",              lambda: e.total_earned >= 500,                    0),
            Quest("Factory Builder", "Build 5 Miners",         lambda: g.count_type("miner") >= 5,            100),
            Quest("Smelting",        "Build a Furnace",        lambda: g.count_type("furnace") >= 1,            40),
            Quest("Automation",      "Build an Assembler",     lambda: g.count_type("assembler") >= 1,          80),
            Quest("Logistics",       "Build Splitter/Merger",  lambda: g.count_type("splitter") + g.count_type("merger") >= 1, 60),
            Quest("Railroad",        "Build a Train Station",  lambda: g.count_type("train_station") >= 1,    150),
            Quest("Robot Age",       "Build a Robot Port",     lambda: g.count_type("robot_port") >= 1,       200),
            Quest("Rich!",           "Earn 10000$",            lambda: e.total_earned >= 10000,                  0),
            Quest("Rocket Launch",   "Build the Rocket",       lambda: self._rocket_ready(),                     0),
        ]

    def record_produced(self, item: str) -> None:
        self._produced[item] = self._produced.get(item, 0) + 1

    def total_produced(self, item: str) -> int:
        return self._produced.get(item, 0)

    def update(self) -> None:
        for q in self.quests:
            if not q.completed and q.check():
                q.completed = True
                self.econ.earn(q.reward_money)
                self.notifications.append({"text": f"✓ Quest: {q.title} +{q.reward_money}$", "t": 5.0})

    def tick_notifications(self, dt: float) -> None:
        for n in self.notifications:
            n["t"] -= dt

    def pop_notifications(self) -> list[dict]:
        self.notifications = [n for n in self.notifications if n["t"] > 0]
        return self.notifications

    def completed_count(self) -> int:
        return sum(1 for q in self.quests if q.completed)

    def _rocket_ready(self) -> bool:
        from constants import ROCKET_REQUIREMENTS
        for item, need in ROCKET_REQUIREMENTS.items():
            if item == "money":
                if self.econ.money < need:
                    return False
            elif self._produced.get(item, 0) < need:
                return False
        return True

    def serialize(self) -> dict:
        return {"produced": self._produced, "completed": [q.title for q in self.quests if q.completed]}

    def deserialize(self, data: dict) -> None:
        self._produced = data.get("produced", {})
        for q in self.quests:
            if q.title in set(data.get("completed", [])):
                q.completed = True