from collections import defaultdict, deque
import time


class StatisticsSystem:
    """Tracks per-minute production stats."""
    WINDOW = 60.0  # seconds

    def __init__(self):
        # item_name -> deque of timestamps
        self._log: dict[str, deque] = defaultdict(deque)
        self.money_log: deque = deque()
        self._last_money = 0

    def log_item(self, item: str) -> None:
        now = time.time()
        self._log[item].append(now)

    def log_money(self, amount: int) -> None:
        now = time.time()
        self.money_log.append((now, amount))

    def _prune(self) -> None:
        cutoff = time.time() - self.WINDOW
        for q in self._log.values():
            while q and q[0] < cutoff:
                q.popleft()
        while self.money_log and self.money_log[0][0] < cutoff:
            self.money_log.popleft()

    def items_per_minute(self, item: str) -> float:
        self._prune()
        return len(self._log.get(item, [])) * (60.0 / self.WINDOW)

    def money_per_minute(self) -> float:
        self._prune()
        total = sum(v for _, v in self.money_log)
        return total * (60.0 / self.WINDOW)

    def all_items(self) -> dict[str, float]:
        self._prune()
        return {
            item: len(q) * (60.0 / self.WINDOW)
            for item, q in self._log.items()
            if q
        }