class Smelter:
    """Smelts ore into ingots in 3 seconds."""
    btype = "smelter"
    RECIPES = {
        "iron_ore":   "iron_ingot",
        "copper_ore": "copper_ingot",
    }
    PROCESS_TIME = 3.0

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.proc_item: str | None = None
        self.proc_timer: float = 0.0
        self.output_item: str | None = None
        self.powered = True
        self.status = "waiting"

    def update(self, dt: float, gmap) -> None:
        if not self.powered:
            self.status = "no_power"
            return
        if self.proc_item is not None:
            self.proc_timer += dt
            self.status = "working"
            if self.proc_timer >= self.PROCESS_TIME:
                self.output_item = self.RECIPES.get(self.proc_item, self.proc_item)
                self.proc_item = None
                self.proc_timer = 0.0
        else:
            self.status = "waiting"

    def accept_item(self, item: str, _from=None) -> bool:
        if item in self.RECIPES and self.proc_item is None and self.output_item is None:
            self.proc_item = item
            return True
        return False

    @property
    def progress_pct(self) -> float:
        return self.proc_timer / self.PROCESS_TIME if self.proc_item else 0.0

    def serialize(self) -> dict:
        return {
            "type": "smelter",
            "x": self.x,
            "y": self.y,
            "proc_item": self.proc_item,
            "proc_timer": self.proc_timer,
            "output_item": self.output_item,
        }