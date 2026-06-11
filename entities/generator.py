class CoalGenerator:
    btype          = "coal_generator"
    POWER_OUTPUT   = 100
    COAL_BURN_TIME = 8.0

    def __init__(self, x: int, y: int):
        self.x          = x
        self.y          = y
        self.fuel       = 0
        self.burn_timer = 0.0
        self.active     = False
        self.status     = "waiting"

    def update(self, dt: float, gmap) -> None:
        if self.fuel > 0:
            self.burn_timer += dt
            self.active = True
            self.status = "working"
            if self.burn_timer >= self.COAL_BURN_TIME:
                self.burn_timer -= self.COAL_BURN_TIME
                self.fuel -= 1
        else:
            self.active = False
            self.status = "waiting"

    def accept_item(self, item: str, _from=None) -> bool:
        if item == "coal" and self.fuel < 10:
            self.fuel += 1
            return True
        return False

    @property
    def current_output(self) -> int:
        return self.POWER_OUTPUT if self.active else 0

    def serialize(self) -> dict:
        return {
            "type": "coal_generator", "x": self.x, "y": self.y,
            "fuel": self.fuel, "burn_timer": self.burn_timer,
        }


class SolarPanel:
    btype        = "solar_panel"
    POWER_OUTPUT = 40

    def __init__(self, x: int, y: int):
        self.x       = x
        self.y       = y
        self.active  = True
        self.status  = "working"
        self.weather_mult = 1.0

    def update(self, dt: float, gmap) -> None:
        pass

    def accept_item(self, item: str, _from=None) -> bool:
        return False

    @property
    def current_output(self) -> int:
        return int(self.POWER_OUTPUT * self.weather_mult)

    def serialize(self) -> dict:
        return {"type": "solar_panel", "x": self.x, "y": self.y}