from .tile import Tile
from .map_gen import generate_map
from .chunk import ChunkManager


class GameMap:
    def __init__(self, w: int = 100, h: int = 80, seed: int = 42, preset: str = "normal"):
        self.width    = w
        self.height   = h
        self.seed     = seed
        self.preset   = preset
        self.chunks   = ChunkManager()
        self.tiles: list[list[Tile]] = generate_map(w, h, seed, preset)

    @property
    def buildings(self) -> list:
        return self.chunks.all_buildings()

    def get_tile(self, x: int, y: int) -> Tile:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return Tile(x, y, "grass")

    def get_building(self, x: int, y: int):
        return self.chunks.get_at(x, y)

    def add_building(self, b) -> None:
        self.chunks.add(b)

    def remove_building(self, x: int, y: int):
        b = self.chunks.get_at(x, y)
        if b:
            self.chunks.remove(b)
            return b
        return None

    def buildings_of_type(self, btype: str) -> list:
        return [b for b in self.buildings if b.btype == btype]

    def count_type(self, btype: str) -> int:
        return sum(1 for b in self.buildings if b.btype == btype)

    def reveal_area(self, cx: int, cy: int, radius: int = 10) -> None:
        for dy in range(max(0, cy - radius), min(self.height, cy + radius + 1)):
            for dx in range(max(0, cx - radius), min(self.width, cx + radius + 1)):
                if ((dx - cx) ** 2 + (dy - cy) ** 2) ** 0.5 <= radius:
                    self.tiles[dy][dx].revealed = True

    def serialize(self) -> dict:
        deposits = {}
        revealed = []
        for y in range(self.height):
            for x in range(self.width):
                t = self.tiles[y][x]
                if t.is_resource() and t.deposit < t.max_deposit:
                    deposits[f"{x},{y}"] = t.deposit
                if t.revealed:
                    revealed.append((x, y))
        return {
            "seed":      self.seed,
            "preset":    self.preset,
            "buildings": [b.serialize() for b in self.buildings],
            "deposits":  deposits,
            "revealed":  revealed,
        }