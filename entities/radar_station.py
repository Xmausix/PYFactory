class RadarStation:
    btype       = "radar_station"
    SCAN_RADIUS = 15
    SCAN_TIME   = 5.0

    def __init__(self, x: int, y: int):
        self.x       = x
        self.y       = y
        self.timer   = 0.0
        self.powered = True
        self.status  = "idle"

    def update(self, dt: float, gmap) -> None:
        if not self.powered:
            self.status = "no_power"
            return
        self.timer += dt
        self.status = "working"
        if self.timer >= self.SCAN_TIME:
            self.timer -= self.SCAN_TIME
            gmap.reveal_area(self.x, self.y, self.SCAN_RADIUS)

    def accept_item(self, item: str, _from=None) -> bool:
        return False

    def serialize(self) -> dict:
        return {"type": "radar_station", "x": self.x, "y": self.y}