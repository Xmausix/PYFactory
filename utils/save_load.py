import json
import os
from constants import SAVE_FILE
from entities import ENTITY_MAP


def save_game(gmap, econ, research) -> None:
    data = {
        "economy": econ.serialize(),
        "buildings": [b.serialize() for b in gmap.buildings],
        "seed": gmap.seed,
        "research": research.serialize(),
    }
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[SAVE] -> {SAVE_FILE}")


def load_game(gmap, econ, research) -> bool:
    if not os.path.exists(SAVE_FILE):
        return False
    try:
        with open(SAVE_FILE) as f:
            data = json.load(f)

        econ.deserialize(data.get("economy", {}))
        gmap.buildings = []

        for d in data.get("buildings", []):
            bt = d.get("type", "")
            cls = ENTITY_MAP.get(bt)
            if not cls:
                continue
            b = cls(d["x"], d["y"])
            for attr in ("direction", "proc_item", "proc_timer",
                         "output_item", "items", "sell_count",
                         "recipe", "filter", "held_item",
                         "output_buffer", "total_earned"):
                if attr in d and hasattr(b, attr):
                    setattr(b, attr, d[attr])
            gmap.add_building(b)

        research.deserialize(data.get("research", {}))
        print(f"[LOAD] <- {SAVE_FILE}")
        return True
    except Exception as e:
        print(f"[LOAD] Error: {e}")
        return False