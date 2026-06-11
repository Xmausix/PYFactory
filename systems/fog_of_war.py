class FogOfWar:
    def __init__(self, gmap):
        self.gmap    = gmap
        self.enabled = True

    def is_revealed(self, x: int, y: int) -> bool:
        if not self.enabled:
            return True
        if 0 <= x < self.gmap.width and 0 <= y < self.gmap.height:
            return self.gmap.tiles[y][x].revealed
        return False

    def reveal_around(self, x: int, y: int, radius: int = 5) -> None:
        self.gmap.reveal_area(x, y, radius)