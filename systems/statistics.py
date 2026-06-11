from collections import defaultdict, deque
import time


class StatisticsSystem:
    WINDOW = 60.0

    def __init__(self):
        self._log: dict[str, deque]  = defaultdict(deque)
        self._money: deque           = deque()

    def log_item(self, item: str) -> None:
        self._log[item].append(time.time())

    def log_money(self, amount: int) -> None:
        self._money.append((time.time(), amount))

    def _prune(self) -> None:
        cutoff = time.time() - self.WINDOW
        for q in self._log.values():
            while q and q[0] < cutoff:
                q.popleft()
        while self._money and self._money[0][0] < cutoff:
            self._money.popleft()

    def items_per_minute(self, item: str) -> float:
        self._prune()
        return len(self._log.get(item, [])) * (60.0 / self.WINDOW)

    def money_per_minute(self) -> float:
        self._prune()
        return sum(v for _, v in self._money) * (60.0 / self.WINDOW)

    def all_items(self) -> dict[str, float]:
        self._prune()
        return {item: len(q) * (60.0 / self.WINDOW) for item, q in self._log.items() if q}

    def total_items_per_minute(self) -> float:
        self._prune()
        return sum(len(q) for q in self._log.values()) * (60.0 / self.WINDOW)

    def history_money(self, n: int = 60) -> list[float]:
        now = time.time()
        result = []
        for sec in range(n - 1, -1, -1):
            lo, hi = now - sec - 1, now - sec
            result.append(sum(v for t, v in self._money if lo <= t < hi))
        return result

    def history_item(self, item: str, n: int = 60) -> list[float]:
        now = time.time()
        q   = self._log.get(item, deque())
        result = []
        for sec in range(n - 1, -1, -1):
            lo, hi = now - sec - 1, now - sec
            result.append(float(sum(1 for t in q if lo <= t < hi)))
        return result