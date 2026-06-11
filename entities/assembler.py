from constants import ASSEMBLER_RECIPES, BELT_DIRS, BELT_DELTA, MODULE_TYPES
from .belt import BeltItem


class Assembler:
    btype = "assembler"

    def __init__(self, x: int, y: int, recipe: str = "iron_gears"):
        self.x            = x
        self.y            = y
        self.recipe       = recipe
        self.proc_item:   str | None = None
        self.proc_timer   = 0.0
        self.output_item: str | None = None
        self.input_buffer: list[str] = []
        self.powered      = True
        self.status       = "waiting"
        self.module: str | None = None
        self.input_count  = 0
        self.output_count = 0

    def update(self, dt: float, gmap) -> None:
        if not self.powered:
            self.status = "no_power"
            return
        r = ASSEMBLER_RECIPES.get(self.recipe)
        if not r:
            return
        needed = r["inputs"]
        if self.proc_item is None and len(self.input_buffer) < len(needed):
            for d in BELT_DIRS:
                dx, dy = BELT_DELTA[d]
                sb = gmap.get_building(self.x - dx, self.y - dy)
                if sb and hasattr(sb, "items") and sb.items:
                    first = sb.items[0]
                    name  = first.name if isinstance(first, BeltItem) else first
                    if name in needed:
                        sb.items.pop(0)
                        self.input_buffer.append(name)
                        self.input_count += 1
                        break
        if self.proc_item is None and self.output_item is None and len(self.input_buffer) >= len(needed):
            buf = self.input_buffer[:]
            ok  = True
            for req in needed:
                if req in buf:
                    buf.remove(req)
                else:
                    ok = False
                    break
            if ok:
                self.proc_item    = needed[0]
                self.proc_timer   = 0.0
                self.input_buffer = []
        if self.proc_item is not None:
            time_ = r["time"] / self._speed_mult()
            self.proc_timer += dt
            self.status = "working"
            if self.proc_timer >= time_:
                self.output_item  = r["output"]
                self.output_count += 1
                self.proc_item    = None
                self.proc_timer   = 0.0
        else:
            self.status = "waiting"

    def accept_item(self, item: str, _from=None) -> bool:
        r = ASSEMBLER_RECIPES.get(self.recipe)
        if not r or item not in r["inputs"]:
            return False
        if self.output_item is None and len(self.input_buffer) < len(r["inputs"]):
            self.input_buffer.append(item)
            self.input_count += 1
            return True
        return False

    def _speed_mult(self) -> float:
        if self.module and self.module in MODULE_TYPES:
            return MODULE_TYPES[self.module].get("speed_mult", 1.0)
        return 1.0

    @property
    def progress_pct(self) -> float:
        r = ASSEMBLER_RECIPES.get(self.recipe)
        if r and self.proc_item:
            return min(1.0, self.proc_timer / (r["time"] / self._speed_mult()))
        return 0.0

    @property
    def efficiency(self) -> float:
        if self.output_count == 0:
            return 0.0
        return min(1.0, self.output_count / max(1, self.input_count))

    def serialize(self) -> dict:
        return {
            "type": "assembler", "x": self.x, "y": self.y,
            "recipe": self.recipe, "proc_item": self.proc_item,
            "proc_timer": self.proc_timer, "output_item": self.output_item,
            "input_buffer": self.input_buffer, "module": self.module,
            "input_count": self.input_count, "output_count": self.output_count,
        }