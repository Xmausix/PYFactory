from constants import B_COSTS, BELT_DIRS, ASSEMBLER_RECIPES
from entities import ENTITY_MAP


class PlacementSystem:
    def __init__(self, gmap, econ):
        self.gmap         = gmap
        self.econ         = econ
        self.belt_dir     = "right"
        self.inserter_dir = "right"
        self.splitter_dir = "right"
        self.merger_dir   = "right"
        self.rail_dir     = "right"
        self.ugb_mode     = "input"
        self.recipe       = "iron_gears"

    def place(self, x: int, y: int, bt: str | None) -> bool:
        if not bt or self.gmap.get_building(x, y):
            return False
        if not (0 <= x < self.gmap.width and 0 <= y < self.gmap.height):
            return False
        tile = self.gmap.get_tile(x, y)
        if not tile.is_buildable():
            return False
        if bt == "miner" and not tile.is_resource():
            return False
        cost = B_COSTS.get(bt, 999)
        if not self.econ.spend(cost):
            return False
        cls = ENTITY_MAP.get(bt)
        if not cls:
            self.econ.earn(cost)
            return False
        b = cls(x, y)
        self._configure(b, bt)
        self.gmap.add_building(b)
        from systems.fog_of_war import FogOfWar
        self.gmap.reveal_area(x, y, 5)
        return True

    def _configure(self, b, bt):
        dirs_map = {
            "belt": "belt_dir", "underground_belt": "belt_dir",
            "inserter": "inserter_dir", "splitter": "splitter_dir",
            "priority_splitter": "splitter_dir", "merger": "merger_dir",
            "rail": "rail_dir",
        }
        if bt in dirs_map and hasattr(b, "direction"):
            b.direction = getattr(self, dirs_map[bt])
        if bt == "underground_belt":
            b.mode = self.ugb_mode
        if bt == "assembler":
            b.recipe = self.recipe

    def remove(self, x: int, y: int) -> bool:
        b = self.gmap.remove_building(x, y)
        if b:
            self.econ.earn(B_COSTS.get(b.btype, 0) // 2)
            return True
        return False

    def sell(self, x: int, y: int) -> bool:
        b = self.gmap.remove_building(x, y)
        if b:
            self.econ.earn(B_COSTS.get(b.btype, 0))
            return True
        return False

    def _rot(self, attr, step):
        cur = getattr(self, attr)
        i   = BELT_DIRS.index(cur)
        setattr(self, attr, BELT_DIRS[(i + step) % 4])

    def rotate_belt(self, s=1):     self._rot("belt_dir", s)
    def rotate_inserter(self, s=1): self._rot("inserter_dir", s)
    def rotate_splitter(self, s=1): self._rot("splitter_dir", s)
    def rotate_merger(self, s=1):   self._rot("merger_dir", s)
    def rotate_rail(self, s=1):     self._rot("rail_dir", s)
    def toggle_ugb_mode(self):      self.ugb_mode = "output" if self.ugb_mode == "input" else "input"

    def cycle_recipe(self, s=1):
        recipes = list(ASSEMBLER_RECIPES.keys())
        i = recipes.index(self.recipe)
        self.recipe = recipes[(i + s) % len(recipes)]

    def auto_build(self, x: int, y: int) -> None:
        tile = self.gmap.get_tile(x, y)
        if not tile.is_resource():
            return
        self.place(x, y, "miner")
        old = self.belt_dir
        self.belt_dir = "right"
        for cx, cy, ct in [(x+1,y,"belt"),(x+2,y,"belt"),(x+3,y,"furnace"),
                            (x+4,y,"belt"),(x+5,y,"belt"),(x+6,y,"market")]:
            self.place(cx, cy, ct)
        self.belt_dir = old