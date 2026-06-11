from constants import BELT_DIRS, BELT_DELTA


class Merger:
    """Merges two input belts into one output."""
    btype = "merger"

    def __init__(self, x: int, y: int, direction: str = "right"):
        self.x = x
        self.y = y
        self.direction = direction
        self.item: str | None = None
        self.powered = True
        self.status = "idle"

    def update(self, dt: float, gmap) -> None:
        if not self.powered:
            self.status = "no_power"
            return

        if self.item is not None:
            dx, dy = BELT_DELTA[self.direction]
            nb = gmap.get_building(self.x + dx, self.y + dy)
            if nb and nb.accept_item(self.item, self.direction):
                self.item = None
                self.status = "working"
            return

        # Pull from two input sides
        idx = BELT_DIRS.index(self.direction)
        in_dirs = [
            BELT_DIRS[(idx + 2) % 4],  # opposite
            BELT_DIRS[(idx + 1) % 4],  # right side
            BELT_DIRS[(idx - 1) % 4],  # left side
        ]
        for d in in_dirs:
            dx, dy = BELT_DELTA[d]
            sb = gmap.get_building(self.x - dx, self.y - dy)
            if sb and hasattr(sb, 'items') and sb.items:
                it = sb.items[0]
                name = it.name if hasattr(it, 'name') else it
                self.item = name
                sb.items.pop(0)
                self.status = "working"
                return
        self.status = "idle"

    def accept_item(self, item: str, _from=None) -> bool:
        if self.item is None:
            self.item = item
            return True
        return False

    def rotate(self, step: int = 1) -> None:
        i = BELT_DIRS.index(self.direction)
        self.direction = BELT_DIRS[(i + step) % 4]

    def serialize(self) -> dict:
        return {
            "type": "merger",
            "x": self.x,
            "y": self.y,
            "direction": self.direction,
        }