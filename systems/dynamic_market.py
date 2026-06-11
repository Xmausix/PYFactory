import random
import time
from constants import MARKET_BASE_PRICES


class DynamicMarket:
    _prices:   dict[str, int] = dict(MARKET_BASE_PRICES)
    _history:  dict[str, list[tuple[float, int]]] = {}
    _last_update: float = 0.0
    UPDATE_INTERVAL = 30.0

    @classmethod
    def get_price(cls, item: str) -> int:
        return cls._prices.get(item, 0)

    @classmethod
    def update(cls, dt: float) -> None:
        now = time.time()
        if now - cls._last_update < cls.UPDATE_INTERVAL:
            return
        cls._last_update = now
        for item, base in MARKET_BASE_PRICES.items():
            change = random.uniform(-0.25, 0.25)
            new_price = max(1, int(base * (1.0 + change)))
            cls._prices[item] = new_price
            if item not in cls._history:
                cls._history[item] = []
            cls._history[item].append((now, new_price))
            if len(cls._history[item]) > 60:
                cls._history[item] = cls._history[item][-60:]

    @classmethod
    def get_all_prices(cls) -> dict[str, int]:
        return dict(cls._prices)

    @classmethod
    def get_history(cls, item: str) -> list[tuple[float, int]]:
        return cls._history.get(item, [])