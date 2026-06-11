from constants import BELT_DIRS, BELT_DELTA
from .belt import BeltItem

MAX_UNDERGROUND = 4


class UndergroundBelt:
    btype     = "underground_belt"
    SPEED     = 1.5
    MAX_ITEMS = 6

    def __init__(self, x: int, y: int, direction: str = "right", mode: str = "input"):
        self.x         = x
        self.y         = y
        self.direction = direction
        self.mode      = mode
        self.items: list[BeltItem] = []
        self.powered   = True
        self.status    = "idle"

    def update(self, dt: float, gmap) -> None:
        if not self.powered:
            self.status = "no_power"
            return
        if self.mode == "input":
            self._update_input(dt, gmap)
        else:
            self._update_output(dt, gmap)

    def _update_input(self, dt, gmap):
        if not self.items:
            self.status = "idle"
            return
        speed  = self.SPEED * dt
        dx, dy = BELT_DELTA[self.direction]
        partner = None
        for dist in range(1, MAX_UNDERGROUND + 2):
            nx, ny = self.x + dx * dist, self.y + dy * dist
            b = gmap.get_building(nx, ny)
            if b and b.btype == "underground_belt" and b.mode == "output" and b.direction == self.direction:
                partner = b
                break
        for bi in self.items:
            bi.progress = min(bi.progress + speed, 1.0)
        if self.items and self.items[0].progress >= 1.0 and partner:
            if partner.accept_item(self.items[0].name):
                self.items.pop(0)
        self.status = "working"

    def _update_output(self, dt, gmap):
        if not self.items:
            self.status = "idle"
            return
        speed  = self.SPEED * dt
        dx, dy = BELT_DELTA[self.direction]
        nb = gmap.get_building(self.x + dx, self.y + dy)
        for bi in self.items:
            bi.progress = min(bi.progress + speed, 1.0)
        if self.items and self.items[0].progress >= 1.0:
            if nb and nb.accept_item(self.items[0].name, self.direction):
                self.items.pop(0)
            else:
                self.items[0].progress = 1.0
        self.status = "working"

    def accept_item(self, item: str, _from=None) -> bool:
        if len(self.items) < self.MAX_ITEMS:
            self.items.append(BeltItem(item, 0.0))
            return True
        return False

    def rotate(self, step: int = 1) -> None:
        i = BELT_DIRS.index(self.direction)
        self.direction = BELT_DIRS[(i + step) % 4]

    def serialize(self) -> dict:
        return {
            "type": "underground_belt", "x": self.x, "y": self.y,
            "direction": self.direction, "mode": self.mode,
            "items": [it.name for it in self.items],
        }