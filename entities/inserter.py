from constants import BELT_DIRS, BELT_DELTA
from .belt import BeltItem


class Inserter:
    btype       = "inserter"
    SWING_SPEED = 3.0

    def __init__(self, x: int, y: int, direction: str = "right"):
        self.x          = x
        self.y          = y
        self.direction  = direction
        self.held_item: str | None = None
        self.swing      = 0.0
        self.powered    = True
        self.status     = "idle"

    def update(self, dt: float, gmap) -> None:
        if not self.powered:
            self.status = "no_power"
            return
        dx, dy = BELT_DELTA[self.direction]
        if self.held_item is not None:
            nb = gmap.get_building(self.x + dx, self.y + dy)
            if nb and nb.accept_item(self.held_item, self.direction):
                self.held_item = None
                self.swing     = 0.0
                self.status    = "working"
                return
            self.swing  = min(1.0, self.swing + dt * self.SWING_SPEED)
            self.status = "working"
        else:
            sb   = gmap.get_building(self.x - dx, self.y - dy)
            item = self._take_from(sb)
            if item:
                self.held_item = item
                self.swing     = 0.0
                self.status    = "working"
            else:
                self.swing  = max(0.0, self.swing - dt * self.SWING_SPEED)
                self.status = "idle"

    @staticmethod
    def _take_from(sb) -> str | None:
        if sb is None:
            return None
        if hasattr(sb, "items") and sb.items:
            first = sb.items[0]
            if hasattr(first, "progress") and first.progress >= 0.75:
                sb.items.pop(0)
                return first.name
        if hasattr(sb, "output_buffer") and sb.output_buffer:
            return sb.pop_output()
        if hasattr(sb, "output_item") and sb.output_item:
            item = sb.output_item
            sb.output_item = None
            return item
        return None

    def accept_item(self, item: str, _from=None) -> bool:
        return False

    def rotate(self, step: int = 1) -> None:
        i = BELT_DIRS.index(self.direction)
        self.direction = BELT_DIRS[(i + step) % 4]

    def serialize(self) -> dict:
        return {
            "type": "inserter", "x": self.x, "y": self.y,
            "direction": self.direction, "held_item": self.held_item,
        }