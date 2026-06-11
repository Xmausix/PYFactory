class Generator:
    """Produces power for the factory."""
    btype = "generator"
    POWER_OUTPUT = 100  # MW

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.active = True
        self.status = "working"

    def update(self, dt: float, gmap) -> None:
        pass  # Power is handled by EnergySystem

    def accept_item(self, item: str, _from=None) -> bool:
        return False

    def serialize(self) -> dict:
        return {"type": "generator", "x": self.x, "y": self.y}