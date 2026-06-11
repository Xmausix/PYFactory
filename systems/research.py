from dataclasses import dataclass, field


@dataclass
class Tech:
    key: str
    name: str
    description: str
    cost: int  # research points
    prerequisites: list[str] = field(default_factory=list)
    unlocked: bool = False
    # Effect lambdas applied on unlock
    effect_desc: str = ""


TECH_TREE = [
    Tech("fast_miners",   "Fast Miners",    "Miners produce 2x faster",        50,  [],             effect_desc="+100% miner speed"),
    Tech("big_storage",   "Big Storage",    "Storage capacity 500→1000",        80,  [],             effect_desc="2x storage capacity"),
    Tech("better_smelter","Better Smelter", "Smelting 1.5x faster",            100, ["fast_miners"], effect_desc="-33% smelt time"),
    Tech("tier2_assembly","Tier-2 Assembly","Unlock iron_plates/machine_parts", 120, ["better_smelter"], effect_desc="New recipes"),
    Tech("power_grid",    "Power Grid",     "Generators produce 150 MW",       150, ["fast_miners"], effect_desc="+50% generator output"),
    Tech("advanced_belt", "Advanced Belt",  "Belt speed x2",                   200, ["tier2_assembly"], effect_desc="2x belt speed"),
]


class ResearchSystem:
    RESEARCH_PER_SECOND = 1.0  # points/s passively

    def __init__(self, econ):
        self.econ = econ
        self.techs: dict[str, Tech] = {t.key: t for t in TECH_TREE}
        self.research_points = 0.0
        self.active_research: str | None = None
        self._applied: set[str] = set()

    def update(self, dt: float, gmap) -> None:
        # Passive research generation
        labs = sum(1 for b in gmap.buildings if b.btype == "assembler")
        rate = self.RESEARCH_PER_SECOND + labs * 0.5
        self.research_points += rate * dt

        if self.active_research:
            tech = self.techs.get(self.active_research)
            if tech and not tech.unlocked and self.research_points >= tech.cost:
                self.research_points -= tech.cost
                tech.unlocked = True
                self._apply_effect(tech, gmap)
                self.active_research = None

    def _apply_effect(self, tech: Tech, gmap) -> None:
        if tech.key == "fast_miners":
            from entities import Miner
            Miner.PRODUCTION_TIME = 1.0
        elif tech.key == "big_storage":
            from entities import Storage
            Storage.CAPACITY = 1000
        elif tech.key == "better_smelter":
            from entities import Smelter
            Smelter.PROCESS_TIME = 2.0
        elif tech.key == "power_grid":
            from entities import Generator
            Generator.POWER_OUTPUT = 150
        elif tech.key == "advanced_belt":
            from entities import Belt
            Belt.SPEED = 3.0

    def can_research(self, key: str) -> bool:
        tech = self.techs.get(key)
        if not tech or tech.unlocked:
            return False
        return all(self.techs[p].unlocked for p in tech.prerequisites)

    def start_research(self, key: str) -> bool:
        if self.can_research(key):
            self.active_research = key
            return True
        return False

    def serialize(self) -> dict:
        return {
            "research_points": self.research_points,
            "active_research": self.active_research,
            "unlocked": [k for k, t in self.techs.items() if t.unlocked],
        }

    def deserialize(self, data: dict) -> None:
        self.research_points = data.get("research_points", 0.0)
        self.active_research = data.get("active_research")
        for key in data.get("unlocked", []):
            if key in self.techs:
                self.techs[key].unlocked = True