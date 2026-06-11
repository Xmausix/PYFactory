from constants import ASSEMBLER_RECIPES, BELT_DIRS, BELT_DELTA


class Assembler:
    """Assembles items into advanced products."""
    btype = "assembler"

    def __init__(self, x: int, y: int, recipe: str = "iron_gears"):
        self.x = x
        self.y = y
        self.recipe = recipe
        self.proc_item: str | None = None
        self.proc_timer: float = 0.0
        self.output_item: str | None = None
        self.input_buffer: list[str] = []
        self.powered = True
        self.status = "waiting"

    def update(self, dt: float, gmap) -> None:
        if not self.powered:
            self.status = "no_power"
            return

        recipe = ASSEMBLER_RECIPES.get(self.recipe)
        if not recipe:
            return

        needed = recipe["inputs"]

        # Try to gather inputs from adjacent belts
        if self.proc_item is None and len(self.input_buffer) < len(needed):
            for d in BELT_DIRS:
                dx, dy = BELT_DELTA[d]
                sb = gmap.get_building(self.x - dx, self.y - dy)
                if sb and hasattr(sb, 'items') and sb.items:
                    it = sb.items[0].name if hasattr(sb.items[0], 'name') else sb.items[0]
                    if it in needed:
                        self.input_buffer.append(it)
                        sb.items.pop(0)
                        break

        # Start processing if we have enough inputs
        if (self.proc_item is None
                and len(self.input_buffer) >= len(needed)
                and self.output_item is None):
            # Check exact match
            buf_copy = self.input_buffer[:]
            ok = True
            for req in needed:
                if req in buf_copy:
                    buf_copy.remove(req)
                else:
                    ok = False
                    break
            if ok:
                self.proc_item = needed[0]
                self.proc_timer = 0.0
                self.input_buffer = []

        if self.proc_item is not None:
            self.proc_timer += dt
            self.status = "working"
            if self.proc_timer >= recipe["time"]:
                self.output_item = recipe["output"]
                self.proc_item = None
                self.proc_timer = 0.0
        else:
            self.status = "waiting"

    def accept_item(self, item: str, _from=None) -> bool:
        recipe = ASSEMBLER_RECIPES.get(self.recipe)
        if not recipe or item not in recipe["inputs"]:
            return False
        if self.output_item is None and len(self.input_buffer) < len(recipe["inputs"]):
            self.input_buffer.append(item)
            return True
        return False

    @property
    def progress_pct(self) -> float:
        r = ASSEMBLER_RECIPES.get(self.recipe)
        return self.proc_timer / r["time"] if r and self.proc_item else 0.0

    def serialize(self) -> dict:
        return {
            "type": "assembler",
            "x": self.x,
            "y": self.y,
            "recipe": self.recipe,
            "proc_item": self.proc_item,
            "proc_timer": self.proc_timer,
            "output_item": self.output_item,
        }