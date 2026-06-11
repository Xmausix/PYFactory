from constants import BELT_DIRS


class Rail:
    btype = "rail"

    def __init__(self, x: int, y: int, direction: str = "right"):
        self.x         = x
        self.y         = y
        self.direction = direction
        self.status    = "idle"

    def accept_item(self, item: str, _from=None) -> bool:
        return False

    def rotate(self, step: int = 1) -> None:
        i = BELT_DIRS.index(self.direction)
        self.direction = BELT_DIRS[(i + step) % 4]

    def update(self, dt: float, gmap) -> None:
        pass

    def serialize(self) -> dict:
        return {"type": "rail", "x": self.x, "y": self.y, "direction": self.direction}