from constants import BELT_DIRS, BELT_DELTA


class BeltItem:
    __slots__ = ("name", "progress")
    def __init__(self, name: str, progress: float = 0.0):
        self.name     = name
        self.progress = progress


class Belt:
    btype     = "belt"
    SPEED     = 1.5
    MAX_ITEMS = 3

    def __init__(self, x: int, y: int, direction: str = "right"):
        self.x         = x
        self.y         = y
        self.direction = direction
        self.items: list[BeltItem] = []
        self.powered   = True
        self.status    = "idle"
        self.jammed    = False

    @property
    def item(self) -> str | None:
        return self.items[0].name if self.items else None

    @item.setter
    def item(self, value):
        if value is None:
            if self.items:
                self.items.pop(0)
        else:
            self.items.insert(0, BeltItem(value))

    @property
    def move_progress(self) -> float:
        return self.items[0].progress if self.items else 0.0

    def update(self, dt: float, gmap) -> None:
        if self.jammed:
            self.status = "waiting"
            return
        if not self.items:
            self.status = "idle"
            return
        self.status = "working" if self.powered else "no_power"
        if not self.powered:
            return
        speed  = self.SPEED * dt
        dx, dy = BELT_DELTA[self.direction]
        nb     = gmap.get_building(self.x + dx, self.y + dy)
        for i, bi in enumerate(self.items):
            limit = 1.0 if i == 0 else max(0.0, self.items[i - 1].progress - 0.32)
            bi.progress = min(bi.progress + speed, limit)
        front = self.items[0]
        if front.progress >= 1.0:
            if nb and nb.accept_item(front.name, self.direction):
                self.items.pop(0)
            else:
                front.progress = 1.0

    def accept_item(self, item: str, _from=None) -> bool:
        if self.jammed:
            return False
        if len(self.items) < self.MAX_ITEMS:
            self.items.append(BeltItem(item, 0.0))
            return True
        return False

    def rotate(self, step: int = 1) -> None:
        i = BELT_DIRS.index(self.direction)
        self.direction = BELT_DIRS[(i + step) % 4]

    def serialize(self) -> dict:
        return {
            "type": "belt", "x": self.x, "y": self.y,
            "direction": self.direction,
            "items": [it.name for it in self.items],
        }