from constants import DEPOSIT_AMOUNTS


class Tile:
    __slots__ = ("x", "y", "tile_type", "biome", "deposit", "max_deposit", "revealed")

    RESOURCES     = frozenset(("iron_ore", "copper_ore", "stone", "coal"))
    RARE_RESOURCES = frozenset(("titanium", "uranium", "gold"))
    ALL_RESOURCES = RESOURCES | RARE_RESOURCES

    def __init__(self, x: int, y: int, t: str = "grass", biome: str = "grassland"):
        self.x           = x
        self.y           = y
        self.tile_type   = t
        self.biome       = biome
        self.revealed    = False
        if t in self.ALL_RESOURCES:
            self.max_deposit = DEPOSIT_AMOUNTS.get(t, 5000)
            self.deposit     = self.max_deposit
        else:
            self.max_deposit = 0
            self.deposit     = 0

    def is_resource(self) -> bool:
        return self.tile_type in self.ALL_RESOURCES

    def resource_name(self) -> str | None:
        return self.tile_type if self.is_resource() else None

    def is_buildable(self) -> bool:
        return self.tile_type != "water"

    def extract(self) -> str | None:
        """Extract one unit. Returns resource name or None if depleted."""
        if self.deposit > 0 and self.is_resource():
            self.deposit -= 1
            return self.tile_type
        return None

    def is_depleted(self) -> bool:
        return self.is_resource() and self.deposit <= 0

    @property
    def deposit_pct(self) -> float:
        return self.deposit / max(1, self.max_deposit)