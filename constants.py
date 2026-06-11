import os

TILE_SIZE = 32
MAP_W = 60
MAP_H = 40
FPS_TARGET = 60

# Zoom
ZOOM_LEVELS = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
DEFAULT_ZOOM_IDX = 2

# UI
TOP_BAR_H = 32
BOTTOM_BAR_H = 48
SIDE_PANEL_W = 200

# Colors
C_BG        = (25, 25, 35)
C_BAR       = (32, 32, 48)
C_GRID      = (50, 50, 65)
C_GRID_B    = (70, 70, 90)
C_HL        = (255, 255, 120, 90)
C_HL_ERR    = (255, 80, 80, 90)
C_TXT       = (220, 220, 230)
C_MONEY     = (80, 220, 100)
C_ITEMS     = (80, 180, 255)
C_DOT       = (255, 210, 60)
C_DOT_B     = (200, 170, 40)
C_PROG_BG   = (60, 60, 80)
C_PROG_FG   = (255, 160, 40)
C_PARTICLE  = (255, 140, 60)
C_ENERGY_OK = (80, 220, 100)
C_ENERGY_WARN = (255, 200, 40)
C_ENERGY_BAD = (255, 60, 60)
C_WORKING   = (80, 220, 100)
C_WAITING   = (255, 200, 40)
C_NO_POWER  = (255, 60, 60)

B_COLORS = {
    "miner":     (190, 140, 40),
    "belt":      (90, 90, 110),
    "smelter":   (190, 70, 40),
    "inserter":  (140, 90, 180),
    "storage":   (70, 110, 190),
    "market":    (70, 190, 110),
    "assembler": (180, 110, 70),
    "generator": (60, 180, 180),
    "splitter":  (180, 60, 180),
    "merger":    (180, 180, 60),
}

TILE_COLORS = {
    "grass":      (50, 100, 50),
    "iron_ore":   (120, 120, 135),
    "copper_ore": (160, 100, 60),
    "stone":      (130, 130, 130),
    "coal":       (50, 50, 50),
    "water":      (40, 80, 180),
}

TILE_LABELS = {
    "iron_ore": "Fe", "copper_ore": "Cu",
    "stone": "St", "coal": "C", "water": "~",
}

B_COSTS = {
    "miner": 10, "belt": 2, "smelter": 20,
    "inserter": 5, "storage": 15, "market": 30,
    "assembler": 25, "generator": 40,
    "splitter": 10, "merger": 10,
}

B_KEYS = {
    "miner": "1", "belt": "2", "smelter": "3",
    "inserter": "4", "storage": "5", "market": "6",
    "assembler": "7", "generator": "8",
    "splitter": "9", "merger": "0",
}

B_POWER_USAGE = {
    "miner": 10,
    "smelter": 20,
    "assembler": 15,
    "inserter": 2,
    "belt": 1,
    "splitter": 2,
    "merger": 2,
}

BELT_DIRS = ["right", "down", "left", "up"]
BELT_DELTA = {
    "right": (1, 0), "left": (-1, 0),
    "down": (0, 1), "up": (0, -1)
}

SAVE_FILE = os.path.join("save", "world.json")

# Item icons colors (for rendering items on belts)
ITEM_COLORS = {
    "iron_ore":           (120, 120, 135),
    "copper_ore":         (160, 100, 60),
    "stone":              (140, 140, 140),
    "coal":               (60, 60, 60),
    "iron_ingot":         (180, 180, 200),
    "copper_ingot":       (200, 130, 80),
    "iron_gear":          (160, 160, 180),
    "copper_cable":       (200, 140, 60),
    "stone_brick":        (160, 150, 130),
    "electronic_circuit": (60, 200, 80),
    "iron_plate":         (170, 175, 195),
    "machine_part":       (140, 100, 180),
}

# Tier 2 recipes for assembler
ASSEMBLER_RECIPES = {
    "iron_gears":          {
        "inputs": ["iron_ingot", "iron_ingot"],
        "output": "iron_gear", "time": 4.0
    },
    "copper_cables":       {
        "inputs": ["copper_ingot"],
        "output": "copper_cable", "time": 2.0
    },
    "stone_bricks":        {
        "inputs": ["stone", "stone"],
        "output": "stone_brick", "time": 3.0
    },
    "electronic_circuits": {
        "inputs": ["iron_ingot", "copper_cable", "copper_cable"],
        "output": "electronic_circuit", "time": 5.0
    },
    "iron_plates":         {
        "inputs": ["iron_ingot", "iron_ingot"],
        "output": "iron_plate", "time": 3.0
    },
    "machine_parts":       {
        "inputs": ["iron_plate", "iron_gear"],
        "output": "machine_part", "time": 6.0
    },
}

MARKET_PRICES = {
    "iron_ingot": 5,
    "copper_ingot": 4,
    "iron_gear": 8,
    "copper_cable": 3,
    "stone_brick": 4,
    "electronic_circuit": 15,
    "iron_plate": 7,
    "machine_part": 20,
}

# Rocket endgame requirements
ROCKET_REQUIREMENTS = {
    "iron_plate": 1000,
    "machine_part": 500,
    "money": 5000,
}