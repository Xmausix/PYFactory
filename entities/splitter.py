from constants import BELT_DIRS, BELT_DELTA


class Splitter:
    btype = "splitter"

    def __init__(self, x: int, y: int, direction: str = "right"):
        self.x         = x
        self.y         = y
        self.direction = direction
        self.item: str | None = None
        self._toggle   = 0
        self.powered   = True
        self.status    = "idle"

    def update(self, dt: float, gmap) -> None:
        if self.item is None or not self.powered:
            self.status = "idle" if self.powered else "no_power"
            return
        idx = BELT_DIRS.index(self.direction)
        out_dirs = [BELT_DIRS[idx % 4], BELT_DIRS[(idx - 1) % 4]]
        for attempt in range(2):
            d = out_dirs[(self._toggle + attempt) % 2]
            dx, dy = BELT_DELTA[d]
            nb = gmap.get_building(self.x + dx, self.y + dy)
            if nb and nb.accept_item(self.item, d):
                self.item    = None
                self._toggle = (self._toggle + 1) % 2
                self.status  = "working"
                return

    def accept_item(self, item: str, _from=None) -> bool:
        if self.item is None:
            self.item = item
            return True
        return False

    def rotate(self, step: int = 1) -> None:
        i = BELT_DIRS.index(self.direction)
        self.direction = BELT_DIRS[(i + step) % 4]

    def serialize(self) -> dict:
        return {"type": "splitter", "x": self.x, "y": self.y, "direction": self.direction}


class PrioritySplitter(Splitter):
    btype = "priority_splitter"

    def update(self, dt: float, gmap) -> None:
        if self.item is None or not self.powered:
            self.status = "idle" if self.powered else "no_power"
            return
        idx = BELT_DIRS.index(self.direction)
        out_dirs = [BELT_DIRS[idx % 4], BELT_DIRS[(idx - 1) % 4]]
        for d in out_dirs:
            dx, dy = BELT_DELTA[d]
            nb = gmap.get_building(self.x + dx, self.y + dy)
            if nb and nb.accept_item(self.item, d):
                self.item   = None
                self.status = "working"
                return

    def serialize(self) -> dict:
        d = super().serialize()
        d["type"] = "priority_splitter"
        return d