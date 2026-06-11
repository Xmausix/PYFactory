import json
import os
from constants import SAVE_FILE, SETTINGS_FILE, DEFAULT_SETTINGS
from entities import ENTITY_MAP, BeltItem


def save_game(gmap, econ, research, quests, energy, weather=None,
              pollution=None, contracts=None, achievements=None) -> None:
    data = {
        "economy":      econ.serialize(),
        "research":     research.serialize(),
        "quests":       quests.serialize(),
        "energy":       energy.serialize(),
        "seed":         gmap.seed,
        "preset":       gmap.preset,
        "buildings":    [b.serialize() for b in gmap.buildings],
    }
    if weather:
        data["weather"] = weather.serialize()
    if pollution:
        data["pollution"] = pollution.serialize()
    if contracts:
        data["contracts"] = contracts.serialize()
    if achievements:
        data["achievements"] = achievements.serialize()
    # Save deposits
    deposits = {}
    for y in range(gmap.height):
        for x in range(gmap.width):
            t = gmap.tiles[y][x]
            if t.is_resource() and t.deposit < t.max_deposit:
                deposits[f"{x},{y}"] = t.deposit
    data["deposits"] = deposits
    # Save revealed tiles
    revealed = []
    for y in range(gmap.height):
        for x in range(gmap.width):
            if gmap.tiles[y][x].revealed:
                revealed.append([x, y])
    data["revealed"] = revealed

    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    print(f"[SAVE] {SAVE_FILE}")


def load_game(gmap, econ, research, quests, energy, weather=None,
              pollution=None, contracts=None, achievements=None) -> bool:
    if not os.path.exists(SAVE_FILE):
        return False
    try:
        with open(SAVE_FILE) as f:
            data = json.load(f)
        econ.deserialize(data.get("economy", {}))
        research.deserialize(data.get("research", {}))
        quests.deserialize(data.get("quests", {}))
        energy.deserialize(data.get("energy", {}))
        if weather and "weather" in data:
            weather.deserialize(data["weather"])
        if pollution and "pollution" in data:
            pollution.deserialize(data["pollution"])
        if contracts and "contracts" in data:
            contracts.deserialize(data["contracts"])
        if achievements and "achievements" in data:
            achievements.deserialize(data["achievements"])
        # Restore deposits
        for key, val in data.get("deposits", {}).items():
            x, y = map(int, key.split(","))
            if 0 <= x < gmap.width and 0 <= y < gmap.height:
                gmap.tiles[y][x].deposit = val
        # Restore revealed
        for pos in data.get("revealed", []):
            x, y = pos
            if 0 <= x < gmap.width and 0 <= y < gmap.height:
                gmap.tiles[y][x].revealed = True
        # Restore buildings
        gmap.chunks.clear()
        for d in data.get("buildings", []):
            bt  = d.get("type", "")
            cls = ENTITY_MAP.get(bt)
            if not cls:
                continue
            b = cls(d["x"], d["y"])
            for attr in ("direction", "proc_item", "proc_timer", "output_item",
                         "items", "sell_count", "recipe", "filter", "held_item",
                         "output_buffer", "total_earned", "mode", "fuel",
                         "burn_timer", "cargo", "input_buffer", "module",
                         "input_count", "output_count"):
                if attr in d and hasattr(b, attr):
                    setattr(b, attr, d[attr])
            if hasattr(b, "items") and b.items and isinstance(b.items[0], str):
                b.items = [BeltItem(name) for name in b.items]
            gmap.add_building(b)
        print(f"[LOAD] {SAVE_FILE}")
        return True
    except Exception as e:
        print(f"[LOAD ERROR] {e}")
        return False


def save_settings(settings: dict) -> None:
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


def load_settings() -> dict:
    if not os.path.exists(SETTINGS_FILE):
        return dict(DEFAULT_SETTINGS)
    try:
        with open(SETTINGS_FILE) as f:
            result = dict(DEFAULT_SETTINGS)
            result.update(json.load(f))
            return result
    except Exception:
        return dict(DEFAULT_SETTINGS)