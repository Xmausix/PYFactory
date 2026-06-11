from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Quest:
    title: str
    description: str
    check: Callable[[], bool]
    reward_money: int = 0
    completed: bool = False
    _notified: bool = field(default=False, repr=False)


class QuestSystem:
    def __init__(self, gmap, econ, stats):
        self.gmap = gmap
        self.econ = econ
        self.stats = stats
        self.quests: list[Quest] = []
        self.notifications: list[dict] = []
        self._build_quests()

    def _build_quests(self) -> None:
        g, e, s = self.gmap, self.econ, self.stats
        self.quests = [
            Quest(
                "First Steps",
                "Place your first Miner",
                lambda: len(g.buildings_of_type("miner")) >= 1,
                reward_money=20,
            ),
            Quest(
                "Power Up",
                "Build a Generator",
                lambda: len(g.buildings_of_type("generator")) >= 1,
                reward_money=30,
            ),
            Quest(
                "Iron Age",
                "Produce 50 Iron Ore",
                lambda: s.items_per_minute("iron_ore") * 60 >= 50
                        or self._total_produced("iron_ore") >= 50,
                reward_money=50,
            ),
            Quest(
                "Merchant",
                "Earn 500$",
                lambda: e.total_earned >= 500,
                reward_money=0,
            ),
            Quest(
                "Factory Builder",
                "Build 5 Miners",
                lambda: len(g.buildings_of_type("miner")) >= 5,
                reward_money=100,
            ),
            Quest(
                "Automation",
                "Build an Assembler",
                lambda: len(g.buildings_of_type("assembler")) >= 1,
                reward_money=80,
            ),
            Quest(
                "Research",
                "Unlock any technology",
                lambda: False,  # Will be updated by ResearchSystem
                reward_money=50,
            ),
            Quest(
                "Rocket Launch",
                "Build the Rocket (endgame)",
                lambda: self._rocket_ready(),
                reward_money=0,
            ),
        ]
        self._produced: dict[str, int] = {}

    def _total_produced(self, item: str) -> int:
        return self._produced.get(item, 0)

    def record_produced(self, item: str) -> None:
        self._produced[item] = self._produced.get(item, 0) + 1

    def _rocket_ready(self) -> bool:
        from constants import ROCKET_REQUIREMENTS
        for item, count in ROCKET_REQUIREMENTS.items():
            if item == "money":
                if self.econ.money < count:
                    return False
            elif self._total_produced(item) < count:
                return False
        return True

    def update(self) -> None:
        for q in self.quests:
            if not q.completed and q.check():
                q.completed = True
                self.econ.earn(q.reward_money)
                self.notifications.append({
                    "text": f"✓ Quest: {q.title}  +{q.reward_money}$",
                    "t": 4.0,
                })

    def pop_notifications(self) -> list[dict]:
        active = [n for n in self.notifications if n["t"] > 0]
        self.notifications = active
        return active

    def tick_notifications(self, dt: float) -> None:
        for n in self.notifications:
            n["t"] -= dt

    def completed_count(self) -> int:
        return sum(1 for q in self.quests if q.completed)