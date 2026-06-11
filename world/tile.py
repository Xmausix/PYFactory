class Tile:
    __slots__ = ("x", "y", "tile_type")

    RESOURCES = ("iron_ore", "copper_ore", "stone", "coal")

    def __init__(self, x: int, y: int, t: str = "grass"):
        self.x = x
        self.y = y
        self.tile_type = t

    def is_resource(self) -> bool:
        return self.tile_type in self.RESOURCES

    def resource_name(self) -> str | None:
        return self.tile_type if self.is_resource() else None

    def is_walkable(self) -> bool:
        return self.tile_type != "water"