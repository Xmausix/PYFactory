from collections import Counter


class Storage:
    btype    = "storage"
    CAPACITY = 500

    def __init__(self, x: int, y: int):
        self.x       = x
        self.y       = y
        self.items: list[str] = []
        self.filter: str | None = None
        self.status  = "idle"

    def accept_item(self, item: str, _from=None) -> bool:
        if self.filter and self.filter != item:
            return False
        if len(self.items) < self.CAPACITY:
            self.items.append(item)
            self.status = "working"
            return True
        self.status = "waiting"
        return False

    def take_item(self, item_type: str | None = None) -> str | None:
        if not self.items:
            return None
        if item_type is None:
            return self.items.pop(0)
        for i, it in enumerate(self.items):
            if it == item_type:
                return self.items.pop(i)
        return None

    @property
    def fill_pct(self) -> float:
        return len(self.items) / self.CAPACITY

    @property
    def counts(self) -> dict:
        return dict(Counter(self.items))

    def serialize(self) -> dict:
        return {
            "type": "storage", "x": self.x, "y": self.y,
            "items": self.items, "filter": self.filter,
        }