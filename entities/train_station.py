class TrainStation:
    btype    = "train_station"
    CAPACITY = 200

    def __init__(self, x: int, y: int):
        self.x        = x
        self.y        = y
        self.items: list[str] = []
        self.mode     = "load"
        self.powered  = True
        self.status   = "idle"

    def accept_item(self, item: str, _from=None) -> bool:
        if self.mode == "load" and len(self.items) < self.CAPACITY:
            self.items.append(item)
            self.status = "working"
            return True
        return False

    def take_item(self) -> str | None:
        return self.items.pop(0) if self.items else None

    def update(self, dt: float, gmap) -> None:
        pass

    def serialize(self) -> dict:
        return {"type": "train_station", "x": self.x, "y": self.y, "mode": self.mode, "items": self.items}