from constants import MARKET_PRICES


class Market:
    """Sells finished products for money."""
    btype = "market"

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.sell_count = 0
        self.total_earned = 0
        self.status = "idle"

    def accept_item(self, item: str, _from=None):
        price = MARKET_PRICES.get(item)
        if price is not None:
            self.sell_count += 1
            self.total_earned += price
            self.status = "working"
            return price
        return 0

    def serialize(self) -> dict:
        return {
            "type": "market",
            "x": self.x,
            "y": self.y,
            "sell_count": self.sell_count,
            "total_earned": self.total_earned,
        }