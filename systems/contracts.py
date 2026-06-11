import random
import time
from constants import MARKET_BASE_PRICES


class Contract:
    def __init__(self, item: str, amount: int, reward: int, deadline: float):
        self.item     = item
        self.amount   = amount
        self.reward   = reward
        self.deadline = deadline
        self.progress = 0
        self.completed = False
        self.expired   = False


class ContractSystem:
    MAX_CONTRACTS = 3
    SPAWN_INTERVAL = 60.0

    def __init__(self):
        self.contracts: list[Contract] = []
        self._timer = 0.0

    def update(self, dt: float) -> None:
        self._timer += dt
        now = time.time()
        for c in self.contracts:
            if not c.completed and now > c.deadline:
                c.expired = True
        self.contracts = [c for c in self.contracts if not c.expired]
        if self._timer >= self.SPAWN_INTERVAL and len(self.contracts) < self.MAX_CONTRACTS:
            self._timer = 0.0
            self._spawn()

    def _spawn(self) -> None:
        items = list(MARKET_BASE_PRICES.keys())
        item  = random.choice(items)
        amount = random.randint(20, 200)
        base   = MARKET_BASE_PRICES.get(item, 5)
        reward = int(amount * base * random.uniform(1.5, 3.0))
        deadline = time.time() + random.uniform(120, 300)
        self.contracts.append(Contract(item, amount, reward, deadline))

    def deliver(self, item: str) -> int:
        for c in self.contracts:
            if not c.completed and c.item == item and c.progress < c.amount:
                c.progress += 1
                if c.progress >= c.amount:
                    c.completed = True
                    return c.reward
        return 0

    def serialize(self) -> dict:
        return {"contracts": [{"item": c.item, "amount": c.amount, "reward": c.reward,
                                "progress": c.progress, "completed": c.completed} for c in self.contracts]}

    def deserialize(self, data: dict) -> None:
        self.contracts = []
        for d in data.get("contracts", []):
            c = Contract(d["item"], d["amount"], d["reward"], time.time() + 120)
            c.progress  = d.get("progress", 0)
            c.completed = d.get("completed", False)
            self.contracts.append(c)