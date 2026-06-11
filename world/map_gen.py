import random
from .tile import Tile
from constants import MAP_PRESETS, DEPOSIT_AMOUNTS

BIOME_TILE = {
    "grassland": "grass",
    "desert":    "sand",
    "forest":    "dark_grass",
}


def generate_map(w: int, h: int, seed: int, preset: str = "normal") -> list[list[Tile]]:
    rng = random.Random(seed)
    cfg = MAP_PRESETS.get(preset, MAP_PRESETS["normal"])

    # Biome centers
    biome_centers = []
    for _ in range(rng.randint(5, 10)):
        bx = rng.randint(0, w - 1)
        by = rng.randint(0, h - 1)
        biome_centers.append((bx, by, rng.choice(["grassland", "desert", "forest"])))

    # Base tiles
    tiles = []
    for y in range(h):
        row = []
        for x in range(w):
            best_biome = "grassland"
            best_dist  = float("inf")
            for bx, by, bn in biome_centers:
                d = (x - bx) ** 2 + (y - by) ** 2
                if d < best_dist:
                    best_dist  = d
                    best_biome = bn
            base = BIOME_TILE.get(best_biome, "grass")
            t = Tile(x, y, base, best_biome)
            t.revealed = True   # ← VISIBLE BY DEFAULT
            row.append(t)
        tiles.append(row)

    # Resource patches
    lo_p, hi_p = cfg["patches"]
    for _ in range(rng.randint(lo_p, hi_p)):
        cx = rng.randint(3, w - 4)
        cy = rng.randint(3, h - 4)
        biome = tiles[cy][cx].biome
        pool = {
            "grassland": ["iron_ore", "iron_ore", "copper_ore", "stone"],
            "desert":    ["copper_ore", "copper_ore", "stone", "coal"],
            "forest":    ["iron_ore", "coal", "coal", "stone"],
        }.get(biome, ["iron_ore", "copper_ore", "stone", "coal"])
        res    = rng.choice(pool)
        radius = rng.uniform(2.5, 5.5)
        for dy in range(max(0, cy - 7), min(h, cy + 8)):
            for dx in range(max(0, cx - 7), min(w, cx + 8)):
                dist = ((dx - cx) ** 2 + (dy - cy) ** 2) ** 0.5
                if dist < radius and rng.random() < 0.72:
                    tiles[dy][dx].tile_type   = res
                    tiles[dy][dx].max_deposit = DEPOSIT_AMOUNTS.get(res, 5000)
                    tiles[dy][dx].deposit     = tiles[dy][dx].max_deposit

    # Rare resources
    if cfg.get("rare", False):
        for _ in range(rng.randint(2, 5)):
            cx     = rng.randint(5, w - 6)
            cy     = rng.randint(5, h - 6)
            res    = rng.choice(["titanium", "uranium", "gold"])
            radius = rng.uniform(1.5, 3.0)
            for dy in range(max(0, cy - 5), min(h, cy + 6)):
                for dx in range(max(0, cx - 5), min(w, cx + 6)):
                    dist = ((dx - cx) ** 2 + (dy - cy) ** 2) ** 0.5
                    if dist < radius and rng.random() < 0.60:
                        tiles[dy][dx].tile_type   = res
                        tiles[dy][dx].max_deposit = DEPOSIT_AMOUNTS.get(res, 1000)
                        tiles[dy][dx].deposit     = tiles[dy][dx].max_deposit

    # Water patches
    lo_w, hi_w = cfg["water"]
    for _ in range(rng.randint(lo_w, hi_w)):
        cx     = rng.randint(4, w - 5)
        cy     = rng.randint(4, h - 5)
        radius = rng.uniform(2.5, 5.0)
        for dy in range(max(0, cy - 7), min(h, cy + 8)):
            for dx in range(max(0, cx - 7), min(w, cx + 8)):
                dist = ((dx - cx) ** 2 + (dy - cy) ** 2) ** 0.5
                base_types = ("grass", "sand", "dark_grass", "forest", "desert")
                if (dist < radius and rng.random() < 0.58
                        and tiles[dy][dx].tile_type in base_types):
                    tiles[dy][dx].tile_type   = "water"
                    tiles[dy][dx].max_deposit = 0
                    tiles[dy][dx].deposit     = 0

    return tiles