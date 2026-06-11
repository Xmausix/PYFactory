import random


class Competitor:
    def __init__(self, name: str):
        self.name       = name
        self.production = 0.0
        self.money      = random.randint(100, 500)
        self.growth     = random.uniform(0.5, 2.0)

    def update(self, dt: float) -> None:
        self.production += self.growth * dt
        self.money      += self.growth * dt * 3


class CompetitorSystem:
    def __init__(self):
        self.competitors = [
            Competitor("Alpha Corp"),
            Competitor("Beta Industries"),
            Competitor("Gamma Mining"),
        ]

    def update(self, dt: float) -> None:
        for c in self.competitors:
            c.update(dt)

    def get_ranking(self, player_production: float, player_money: int) -> list[tuple[str, float]]:
        entries = [("You", player_production)]
        for c in self.competitors:
            entries.append((c.name, c.production))
        return sorted(entries, key=lambda x: -x[1])