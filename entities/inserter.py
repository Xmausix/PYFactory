from constants import BELT_DIRS, BELT_DELTA


class Inserter:
    """Transfers items between adjacent buildings."""
    btype = "inserter"
    SWING_SPEED = 3.0

    def __init__(self, x: int, y: int, direction: str = "right"):
        self.x = x
        self.y = y
        self.direction = direction
        self.held_item: str | None = None
        self.swing: float = 0.0
        self.powered = True
        self.status = "idle"

    def update(self, dt: float, gmap) -> None:
        if not self.powered:
            self.status = "no_power"
            return

        dx, dy = BELT_DELTA[self.direction]

        if self.held_item is not None:
            # Deliver to target
            nb = gmap.get_building(self.x + dx, self.y + dy)
            if nb and nb.accept_item(self.held_item, self.direction):
                self.held_item = None
                self.swing = 0.0
                self.status = "working"
                return
            self.swing = min(1.0, self.swing + dt * self.SWING_SPEED)
            self.status = "working"
        else:
            # Pick from source
            sb = gmap.get_building(self.x - dx, self.y - dy)
            if sb:
                item = None
                if hasattr(sb, 'items') and sb.items and not isinstance(sb.items[0], str):
                    # Belt with BeltItem objects
                    if sb.items and sb.items[0].progress >= 0.8:
                        item = sb.items[0].name
                        sb.items.pop(0)
                elif hasattr(sb, 'output_buffer') and sb.output_buffer:
                    item = sb.pop_output()
                elif hasattr(sb, 'output_item') and sb.output_item:
                    item = sb.output_item
                    sb.output_item = None

                if item:
                    self.held_item = item
                    self.swing = 0.0
                    self.status = "working"
                    return
            self.swing = max(0.0, self.swing - dt * self.SWING_SPEED)
            self.status = "idle"

    def rotate(self, step: int = 1) -> None:
        i = BELT_DIRS.index(self.direction)
        self.direction = BELT_DIRS[(i + step) % 4]

    def serialize(self) -> dict:
        return {
            "type": "inserter",
            "x": self.x,
            "y": self.y,
            "direction": self.direction,
            "held_item": self.held_item,
        }