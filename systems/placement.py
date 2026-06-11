from constants import B_COSTS, BELT_DIRS, ASSEMBLER_RECIPES
from entities import (Miner, Belt, Smelter, Inserter,
                      Storage, Market, Assembler, Generator,
                      Splitter, Merger, ENTITY_MAP)


class PlacementSystem:
    def __init__(self, gmap, econ):
        self.gmap = gmap
        self.econ = econ
        self.belt_dir = "right"
        self.inserter_dir = "right"
        self.assembler_recipe = "iron_gears"
        self.splitter_dir = "right"
        self.merger_dir = "right"

    def place(self, x: int, y: int, bt: str | None) -> bool:
        if not bt:
            return False
        if self.gmap.get_building(x, y):
            return False
        if not (0 <= x < self.gmap.width and 0 <= y < self.gmap.height):
            return False

        cost = B_COSTS.get(bt, 999)
        tile = self.gmap.get_tile(x, y)

        if bt == "miner" and not tile.is_resource():
            return False
        if tile.tile_type == "water":
            return False
        if not self.econ.spend(cost):
            return False

        cls = ENTITY_MAP.get(bt)
        if not cls:
            self.econ.earn(cost)
            return False

        b = cls(x, y)
        if bt == "belt":
            b.direction = self.belt_dir
        elif bt == "inserter":
            b.direction = self.inserter_dir
        elif bt == "assembler":
            b.recipe = self.assembler_recipe
        elif bt == "splitter":
            b.direction = self.splitter_dir
        elif bt == "merger":
            b.direction = self.merger_dir

        self.gmap.add_building(b)
        return True

    def remove(self, x: int, y: int) -> bool:
        b = self.gmap.remove_building(x, y)
        if b:
            self.econ.earn(B_COSTS.get(b.btype, 0) // 2)
            return True
        return False

    def rotate_belt(self, s: int = 1) -> None:
        i = BELT_DIRS.index(self.belt_dir)
        self.belt_dir = BELT_DIRS[(i + s) % 4]

    def rotate_inserter(self, s: int = 1) -> None:
        i = BELT_DIRS.index(self.inserter_dir)
        self.inserter_dir = BELT_DIRS[(i + s) % 4]

    def rotate_splitter(self, s: int = 1) -> None:
        i = BELT_DIRS.index(self.splitter_dir)
        self.splitter_dir = BELT_DIRS[(i + s) % 4]

    def rotate_merger(self, s: int = 1) -> None:
        i = BELT_DIRS.index(self.merger_dir)
        self.merger_dir = BELT_DIRS[(i + s) % 4]

    def cycle_recipe(self, s: int = 1) -> None:
        recipes = list(ASSEMBLER_RECIPES.keys())
        i = recipes.index(self.assembler_recipe)
        self.assembler_recipe = recipes[(i + s) % len(recipes)]

    def auto_build(self, x: int, y: int) -> None:
        """Shift+click: auto-build miner->belt->smelter->belt->market."""
        tile = self.gmap.get_tile(x, y)
        if not tile.is_resource():
            return
        self.place(x, y, "miner")
        old_dir = self.belt_dir
        self.belt_dir = "right"
        chain = [
            (x + 1, y, "belt"), (x + 2, y, "belt"),
            (x + 3, y, "smelter"),
            (x + 4, y, "belt"), (x + 5, y, "belt"),
            (x + 6, y, "market"),
        ]
        for cx, cy, ct in chain:
            self.place(cx, cy, ct)
        self.belt_dir = old_dir