import random
from .tile import Tile


def generate_map(w: int, h: int, seed: int) -> list[list[Tile]]:
    rng = random.Random(seed)
    tiles = [[Tile(x, y, "grass") for x in range(w)] for y in range(h)]

    # Resource patches
    n_patches = rng.randint(10, 20)
    for _ in range(n_patches):
        cx = rng.randint(2, w - 3)
        cy = rng.randint(2, h - 3)
        res = rng.choice(["iron_ore", "copper_ore", "stone", "coal"])
        radius = rng.uniform(2.0, 4.5)
        for y in range(h):
            for x in range(w):
                dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if dist < radius and rng.random() < 0.70:
                    tiles[y][x].tile_type = res

    # Water patches
    n_water = rng.randint(2, 5)
    for _ in range(n_water):
        cx = rng.randint(3, w - 4)
        cy = rng.randint(3, h - 4)
        radius = rng.uniform(2.0, 4.5)
        for y in range(h):
            for x in range(w):
                dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if (dist < radius and rng.random() < 0.55
                        and tiles[y][x].tile_type == "grass"):
                    tiles[y][x].tile_type = "water"

    return tiles