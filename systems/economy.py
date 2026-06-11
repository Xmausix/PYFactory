class Economy:
    def __init__(self, money: int = 100):
        self.money = money
        self.total_earned = 0
        self.total_spent = 0

    def spend(self, cost: int) -> bool:
        if self.money >= cost:
            self.money -= cost
            self.total_spent += cost
            return True
        return False

    def earn(self, amt: int) -> None:
        self.money += amt
        self.total_earned += amt

    def serialize(self) -> dict:
        return {
            "money": self.money,
            "total_earned": self.total_earned,
            "total_spent": self.total_spent,
        }

    def deserialize(self, data: dict) -> None:
        self.money = data.get("money", 100)
        self.total_earned = data.get("total_earned", 0)
        self.total_spent = data.get("total_spent", 0)