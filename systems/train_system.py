class TrainSystem:
    def __init__(self, gmap):
        self.gmap = gmap

    def update(self, dt: float) -> None:
        for b in self.gmap.buildings:
            if b.btype == "locomotive":
                b.update(dt, self.gmap)