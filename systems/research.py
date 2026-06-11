from dataclasses import dataclass, field


@dataclass
class Tech:
    key:           str
    name:          str
    description:   str
    cost:          int
    prerequisites: list = field(default_factory=list)
    unlocked:      bool = False
    effect_desc:   str  = ""


TECH_TREE = [
    Tech("fast_miners",    "Fast Miners",    "2× mining speed",        50,  [], "+100% speed"),
    Tech("big_storage",    "Big Storage",    "2× storage capacity",    80,  [], "500→1000"),
    Tech("better_furnace", "Better Furnace", "1.5× faster smelting",  100, ["fast_miners"], "−33% time"),
    Tech("tier2_assembly", "Tier-2 Assembly","Unlock machine_parts",  120, ["better_furnace"], "New recipes"),
    Tech("power_grid",     "Power Grid",     "Generators +50%",       150, ["fast_miners"], "+50% MW"),
    Tech("fast_belts",     "Fast Belts",     "Belt speed ×2",         200, ["tier2_assembly"], "2× speed"),
    Tech("logistics_mk2",  "Logistics Mk2", "Better splitters",      180, ["fast_belts"], "Improved"),
    Tech("assembly_mk2",   "Assembly Mk2",  "Assemblers 2× faster",  250, ["tier2_assembly"], "−50% time"),
    Tech("trains",         "Trains",         "Unlock locomotives",    300, ["logistics_mk2"], "Trains"),
    Tech("robots",         "Robots",         "Unlock robot ports",    400, ["trains"], "Robots"),
]


class ResearchSystem:
    BASE_RP = 0.5

    def __init__(self, econ):
        self.econ            = econ
        self.techs           = {t.key: t for t in TECH_TREE}
        self.research_points = 0.0
        self.active_research: str | None = None

    def update(self, dt: float, gmap) -> None:
        labs = gmap.count_type("assembler")
        rate = self.BASE_RP + labs * 0.4
        self.research_points += rate * dt
        if self.active_research:
            tech = self.techs.get(self.active_research)
            if tech and not tech.unlocked and self.research_points >= tech.cost:
                self.research_points -= tech.cost
                tech.unlocked = True
                self._apply(tech, gmap)
                self.active_research = None

    def _apply(self, tech, gmap) -> None:
        from entities import Miner, Storage, Furnace, Belt, CoalGenerator
        effects = {
            "fast_miners":    lambda: setattr(Miner, "PRODUCTION_TIME", 1.0),
            "big_storage":    lambda: setattr(Storage, "CAPACITY", 1000),
            "better_furnace": lambda: None,
            "power_grid":     lambda: setattr(CoalGenerator, "POWER_OUTPUT", 150),
            "fast_belts":     lambda: setattr(Belt, "SPEED", 3.0),
        }
        fn = effects.get(tech.key)
        if fn:
            fn()

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
        return {"rp": self.research_points, "active": self.active_research,
                "unlocked": [k for k, t in self.techs.items() if t.unlocked]}

    def deserialize(self, data: dict) -> None:
        self.research_points = data.get("rp", 0.0)
        self.active_research = data.get("active")
        for key in data.get("unlocked", []):
            if key in self.techs:
                self.techs[key].unlocked = True