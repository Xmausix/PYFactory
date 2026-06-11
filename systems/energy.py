from constants import B_POWER_USAGE


class EnergySystem:
    def __init__(self, gmap):
        self.gmap            = gmap
        self.total_generated = 0
        self.total_consumed  = 0
        self.powered         = True
        self.overload_timer  = 0.0

    def update(self, dt: float) -> None:
        gen = sum(b.current_output for b in self.gmap.buildings if hasattr(b, "current_output"))
        con = sum(B_POWER_USAGE.get(b.btype, 0) for b in self.gmap.buildings if not hasattr(b, "current_output"))
        self.total_generated = gen
        self.total_consumed  = con
        self.powered = gen >= con
        if not self.powered:
            self.overload_timer += dt
        else:
            self.overload_timer = 0.0
        for b in self.gmap.buildings:
            if hasattr(b, "powered") and not hasattr(b, "current_output"):
                b.powered = self.powered

    @property
    def status_color(self) -> tuple:
        if self.total_generated == 0:
            return (255, 60, 60)
        ratio = self.total_consumed / self.total_generated
        if ratio < 0.75:
            return (80, 220, 100)
        if ratio < 1.0:
            return (255, 200, 40)
        return (255, 60, 60)

    @property
    def shortage(self) -> int:
        return max(0, self.total_consumed - self.total_generated)

    def serialize(self) -> dict:
        return {"overload_timer": self.overload_timer}

    def deserialize(self, data: dict) -> None:
        self.overload_timer = data.get("overload_timer", 0.0)