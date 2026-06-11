from constants import BELT_DIRS, BELT_DELTA


class BeltItem:
    """Item travelling on belt with position progress 0.0 -> 1.0."""
    def __init__(self, name: str):
        self.name = name
        self.progress: float = 0.0  # 0 = enter tile, 1 = leave tile


class Belt:
    """Transports items in a direction. Supports item queue."""
    btype = "belt"
    SPEED = 1.5  # tiles per second
    MAX_ITEMS = 3

    def __init__(self, x: int, y: int, direction: str = "right"):
        self.x = x
        self.y = y
        self.direction = direction
        self.items: list[BeltItem] = []
        self.powered = True
        self.status = "idle"

    @property
    def item(self):
        """Legacy compatibility: first item or None."""
        return self.items[0].name if self.items else None

    @item.setter
    def item(self, value):
        """Legacy compatibility setter."""
        if value is None:
            if self.items:
                self.items.pop(0)
        else:
            self.items.insert(0, BeltItem(value))

    @property
    def move_progress(self) -> float:
        return self.items[0].progress if self.items else 0.0

    def update(self, dt: float, gmap) -> None:
        if not self.items:
            self.status = "idle"
            return
        self.status = "working" if self.powered else "no_power"
        if not self.powered:
            return

        speed = self.SPEED * dt
        dx, dy = BELT_DELTA[self.direction]
        nb = gmap.get_building(self.x + dx, self.y + dy)

        # Advance items, front item first
        for i, belt_item in enumerate(self.items):
            # Max progress: 1.0 for front (can transfer), 0.9 gap for others
            max_prog = 1.0 if i == 0 else (self.items[i - 1].progress - 0.15)
            max_prog = max(0.0, max_prog)
            belt_item.progress = min(belt_item.progress + speed, max_prog)

        # Try to push front item out
        front = self.items[0]
        if front.progress >= 1.0:
            if nb and nb.accept_item(front.name, self.direction):
                self.items.pop(0)
                # Reset remaining items positions relative
            else:
                front.progress = 1.0  # Blocked

    def accept_item(self, item: str, _from=None) -> bool:
        if len(self.items) < self.MAX_ITEMS:
            bi = BeltItem(item)
            bi.progress = 0.0
            self.items.append(bi)
            return True
        return False

    def rotate(self, step: int = 1) -> None:
        i = BELT_DIRS.index(self.direction)
        self.direction = BELT_DIRS[(i + step) % 4]

    def serialize(self) -> dict:
        return {
            "type": "belt",
            "x": self.x,
            "y": self.y,
            "direction": self.direction,
            "items": [it.name for it in self.items],
        }