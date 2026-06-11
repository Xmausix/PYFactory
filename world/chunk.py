from constants import CHUNK_SIZE


class ChunkManager:
    """Spatial partitioning for buildings."""

    def __init__(self):
        self._chunks: dict[tuple[int, int], list] = {}

    def _key(self, x: int, y: int) -> tuple[int, int]:
        return (x // CHUNK_SIZE, y // CHUNK_SIZE)

    def add(self, building) -> None:
        k = self._key(building.x, building.y)
        if k not in self._chunks:
            self._chunks[k] = []
        self._chunks[k].append(building)

    def remove(self, building) -> None:
        k = self._key(building.x, building.y)
        if k in self._chunks:
            self._chunks[k] = [b for b in self._chunks[k]
                                if not (b.x == building.x and b.y == building.y)]

    def get_at(self, x: int, y: int):
        k = self._key(x, y)
        for b in self._chunks.get(k, []):
            if b.x == x and b.y == y:
                return b
        return None

    def get_nearby(self, x: int, y: int, radius: int = 1) -> list:
        result = []
        cx, cy = self._key(x, y)
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                result.extend(self._chunks.get((cx + dx, cy + dy), []))
        return result

    def all_buildings(self) -> list:
        result = []
        for chunk in self._chunks.values():
            result.extend(chunk)
        return result

    def clear(self) -> None:
        self._chunks.clear()

    def rebuild(self, buildings: list) -> None:
        self.clear()
        for b in buildings:
            self.add(b)