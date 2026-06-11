from constants import FURNACE_RECIPES, MODULE_TYPES


class Furnace:
    btype = "furnace"

    def __init__(self, x: int, y: int):
        self.x           = x
        self.y           = y
        self.proc_item:  str | None = None
        self.proc_timer  = 0.0
        self.output_item: str | None = None
        self.input_count  = 0
        self.output_count = 0
        self.powered     = True
        self.status      = "waiting"
        self.module: str | None = None

    def update(self, dt: float, gmap) -> None:
        if not self.powered:
            self.status = "no_power"
            return
        if self.proc_item is not None:
            recipe = FURNACE_RECIPES.get(self.proc_item, {})
            time_  = recipe.get("time", 3.0) / self._speed_mult()
            self.proc_timer += dt
            self.status = "working"
            if self.proc_timer >= time_:
                self.output_item  = recipe.get("output", self.proc_item)
                self.output_count += 1
                self.proc_item    = None
                self.proc_timer   = 0.0
        else:
            self.status = "waiting"

    def accept_item(self, item: str, _from=None) -> bool:
        if item in FURNACE_RECIPES and self.proc_item is None and self.output_item is None:
            self.proc_item  = item
            self.proc_timer = 0.0
            self.input_count += 1
            return True
        return False

    def _speed_mult(self) -> float:
        if self.module and self.module in MODULE_TYPES:
            return MODULE_TYPES[self.module].get("speed_mult", 1.0)
        return 1.0

    @property
    def progress_pct(self) -> float:
        if not self.proc_item:
            return 0.0
        recipe = FURNACE_RECIPES.get(self.proc_item, {})
        time_  = recipe.get("time", 3.0) / self._speed_mult()
        return min(1.0, self.proc_timer / time_)

    @property
    def efficiency(self) -> float:
        if self.output_count == 0:
            return 0.0
        return min(1.0, self.output_count / max(1, self.input_count))

    def serialize(self) -> dict:
        return {
            "type": "furnace", "x": self.x, "y": self.y,
            "proc_item": self.proc_item, "proc_timer": self.proc_timer,
            "output_item": self.output_item, "module": self.module,
            "input_count": self.input_count, "output_count": self.output_count,
        }