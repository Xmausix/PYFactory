from .tile import Tile
from .map_gen import generate_map


class GameMap:
    def __init__(self, w: int = 60, h: int = 40, seed: int = 42):
        self.width = w
        self.height = h
        self.seed = seed
        self.buildings: list = []
        self.tiles: list[list[Tile]] = generate_map(w, h, seed)

    def get_tile(self, x: int, y: int) -> Tile:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return Tile(x, y, "grass")

    def get_building(self, x: int, y: int):
        for b in self.buildings:
            if b.x == x and b.y == y:
                return b
        return None

    def add_building(self, b) -> None:
        self.buildings.append(b)

    def remove_building(self, x: int, y: int):
        for i, b in enumerate(self.buildings):
            if b.x == x and b.y == y:
                return self.buildings.pop(i)
        return None

    def buildings_of_type(self, btype: str) -> list:
        return [b for b in self.buildings if b.btype == btype]

    def serialize(self) -> dict:
        return {
            "seed": self.seed,
            "buildings": [b.serialize() for b in self.buildings],
        }