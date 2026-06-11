class RobotSystem:
    def __init__(self, gmap):
        self.gmap = gmap

    def update(self, dt: float) -> None:
        for b in self.gmap.buildings:
            if b.btype == "robot_port":
                b.update(dt, self.gmap)