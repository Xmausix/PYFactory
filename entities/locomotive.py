from constants import BELT_DIRS, BELT_DELTA


class Locomotive:
    btype    = "locomotive"
    SPEED    = 3.0
    CAPACITY = 100

    def __init__(self, x: int, y: int):
        self.x         = x
        self.y         = y
        self.direction = "right"
        self.cargo: list[str] = []
        self.progress  = 0.0
        self.state     = "travelling"
        self.status    = "working"
        self.powered   = True
        self._route: list[tuple[int, int]] = []
        self._route_idx = 0

    def update(self, dt: float, gmap) -> None:
        if not self.powered:
            self.status = "no_power"
            return
        dx, dy = BELT_DELTA.get(self.direction, (1, 0))
        self.progress += self.SPEED * dt
        if self.progress >= 1.0:
            self.progress -= 1.0
            self.x += dx
            self.y += dy
            self.x = max(0, min(gmap.width - 1, self.x))
            self.y = max(0, min(gmap.height - 1, self.y))
            self._check_station(gmap)
            self._follow_rail(gmap)

    def _follow_rail(self, gmap) -> None:
        dx, dy = BELT_DELTA.get(self.direction, (1, 0))
        ahead = gmap.get_building(self.x + dx, self.y + dy)
        if ahead and ahead.btype == "rail":
            self.direction = ahead.direction
        else:
            idx = BELT_DIRS.index(self.direction)
            for offset in [1, -1, 2]:
                d = BELT_DIRS[(idx + offset) % 4]
                odx, ody = BELT_DELTA[d]
                b = gmap.get_building(self.x + odx, self.y + ody)
                if b and b.btype == "rail":
                    self.direction = d
                    return

    def _check_station(self, gmap) -> None:
        b = gmap.get_building(self.x, self.y)
        if b and b.btype == "train_station":
            if b.mode == "load" and len(self.cargo) < self.CAPACITY:
                item = b.take_item()
                if item:
                    self.cargo.append(item)
                    self.state = "loading"
            elif b.mode == "unload" and self.cargo:
                item = self.cargo.pop(0)
                b.accept_item(item)
                self.state = "unloading"
            else:
                self.state = "travelling"

    def accept_item(self, item: str, _from=None) -> bool:
        return False

    def serialize(self) -> dict:
        return {
            "type": "locomotive", "x": self.x, "y": self.y,
            "direction": self.direction, "cargo": self.cargo,
        }