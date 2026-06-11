import os

# Display
TILE_SIZE        = 32
MAP_W            = 100
MAP_H            = 80
FPS_TARGET       = 60
TOP_BAR_H        = 36
BOTTOM_BAR_H     = 52
SIDE_PANEL_W     = 240
ZOOM_LEVELS      = [0.25, 0.35, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
DEFAULT_ZOOM_IDX = 4
CHUNK_SIZE       = 16

# Autosave
AUTOSAVE_INTERVAL = 120.0
SAVE_FILE         = os.path.join("save", "world.json")
SETTINGS_FILE     = os.path.join("save", "settings.json")
KEYBINDS_FILE     = os.path.join("save", "keybinds.json")

#Colors
C_BG          = (20,  22,  30)
C_BAR         = (28,  30,  45)
C_PANEL       = (24,  26,  38)
C_GRID        = (45,  48,  62)
C_GRID_B      = (65,  68,  88)
C_HL          = (255, 255, 120, 80)
C_HL_ERR      = (255,  70,  70, 80)
C_TXT         = (210, 215, 230)
C_TXT_DIM     = (130, 135, 150)
C_MONEY       = ( 80, 225, 110)
C_ITEMS       = ( 80, 180, 255)
C_WARN        = (255, 200,  40)
C_ERR         = (255,  60,  60)
C_OK          = ( 80, 220, 100)
C_DOT         = (255, 210,  60)
C_DOT_B       = (200, 170,  40)
C_PROG_BG     = ( 50,  52,  72)
C_PROG_FG     = (255, 160,  40)
C_PARTICLE    = (255, 140,  60)
C_ENERGY_OK   = ( 80, 220, 100)
C_ENERGY_WARN = (255, 200,  40)
C_ENERGY_BAD  = (255,  60,  60)
C_WORKING     = ( 80, 220, 100)
C_WAITING     = (255, 200,  40)
C_NO_POWER    = (255,  60,  60)
C_CHART_BG    = ( 18,  20,  28)
C_CHART_LINE  = ( 80, 160, 255)
C_CHART_MONEY = ( 80, 225, 110)
C_POLLUTION   = (120, 180,  60)
C_FOG         = ( 15,  17,  25)
C_OVERLAY_BELT = (100, 200, 255, 120)
C_OVERLAY_PWR  = (255, 220,  60, 100)
C_CONTRACT    = (200, 180, 100)
C_ACHIEVE     = (255, 215,  60)

#  Building colors
B_COLORS = {
    "miner":             (190, 140,  40),
    "belt":              ( 80,  85, 105),
    "underground_belt":  ( 60,  65,  90),
    "furnace":           (200,  75,  35),
    "inserter":          (140,  90, 180),
    "storage":           ( 65, 110, 195),
    "market":            ( 60, 195, 110),
    "assembler":         (180, 110,  65),
    "coal_generator":    ( 60,  60,  70),
    "solar_panel":       (255, 215,  60),
    "splitter":          (180,  55, 180),
    "priority_splitter": (220,  80, 150),
    "merger":            (180, 180,  55),
    "train_station":     (120,  80,  40),
    "rail":              ( 90,  85,  75),
    "locomotive":        (100,  70,  40),
    "robot_port":        ( 55, 180, 200),
    "radar_station":     ( 80, 200, 160),
}
TILE_COLORS = {
    "grass":       ( 45,  95,  45),
    "dark_grass":  ( 35,  80,  35),
    "sand":        (190, 170, 110),
    "desert":      (210, 185, 120),
    "forest":      ( 30,  75,  30),
    "iron_ore":    (115, 120, 138),
    "copper_ore":  (160,  98,  58),
    "stone":       (128, 128, 128),
    "coal":        ( 48,  48,  52),
    "water":       ( 38,  75, 180),
    "titanium":    (180, 200, 220),
    "uranium":     ( 80, 220,  80),
    "gold":        (220, 200,  60),
}

TILE_LABELS = {
    "iron_ore":   "Fe",
    "copper_ore": "Cu",
    "stone":      "St",
    "coal":       "C",
    "water":      "~",
    "titanium":   "Ti",
    "uranium":    "U",
    "gold":       "Au",
}

DEPOSIT_AMOUNTS = {
    "iron_ore":   5000,
    "copper_ore": 4000,
    "stone":      6000,
    "coal":       3000,
    "titanium":   1500,
    "uranium":    800,
    "gold":       600,
}

B_COSTS = {
    "miner":             10,
    "belt":               2,
    "underground_belt":   8,
    "furnace":           25,
    "inserter":           5,
    "storage":           20,
    "market":            35,
    "assembler":         30,
    "coal_generator":    50,
    "solar_panel":       80,
    "splitter":          12,
    "priority_splitter": 18,
    "merger":            12,
    "train_station":    120,
    "rail":               3,
    "locomotive":        80,
    "robot_port":       200,
    "radar_station":    150,
}

DEFAULT_KEYBINDS = {
    "miner":             "1",
    "belt":              "2",
    "furnace":           "3",
    "inserter":          "4",
    "storage":           "5",
    "market":            "6",
    "assembler":         "7",
    "coal_generator":    "8",
    "solar_panel":       "9",
    "splitter":          "0",
    "underground_belt":  "u",
    "merger":            "j",
    "priority_splitter": "k",
    "train_station":     "t",
    "rail":              "l",
    "robot_port":        "b",
    "radar_station":     "n",
    "rotate_left":       "q",
    "rotate_right":      "e",
    "toggle_ugb":        "f",
    "pause":             "p",
    "save":              "F5",
    "load":              "F9",
    "research":          "r",
    "settings":          "o",
    "minimap":           "m",
    "grid":              "g",
    "clear_particles":   "c",
    "fullscreen":        "F11",
    "overlay":           "x",
    "world_stats":       "i",
    "achievements":      "h",
    "zoom_in":           "=",
    "zoom_out":          "-",
}

B_KEYS = dict(DEFAULT_KEYBINDS)

B_POWER_USAGE = {
    "miner":             10,
    "furnace":           20,
    "assembler":         15,
    "inserter":           2,
    "belt":               1,
    "underground_belt":   1,
    "splitter":           2,
    "priority_splitter":  2,
    "merger":             2,
    "robot_port":        30,
    "train_station":     10,
    "locomotive":         5,
    "radar_station":     15,
}

BELT_DIRS  = ["right", "down", "left", "up"]
BELT_DELTA = {
    "right": ( 1,  0),
    "left":  (-1,  0),
    "down":  ( 0,  1),
    "up":    ( 0, -1),
}

ITEM_COLORS = {
    "iron_ore":     (160, 165, 185),
    "copper_ore":   (190, 120,  70),
    "stone":        (155, 155, 155),
    "coal":         ( 65,  65,  70),
    "iron_plate":   (190, 195, 215),
    "copper_plate": (215, 145,  85),
    "iron_gear":    (170, 175, 195),
    "copper_wire":  (225, 165,  65),
    "circuit":      ( 65, 215,  90),
    "machine_part": (155, 105, 200),
    "stone_brick":  (170, 160, 140),
    "titanium":     (200, 220, 240),
    "uranium":      (100, 240, 100),
    "gold":         (240, 220,  70),
}

ITEM_SHAPES = {
    "iron_ore":     "square",
    "copper_ore":   "square",
    "stone":        "square",
    "coal":         "square",
    "iron_plate":   "rect",
    "copper_plate": "rect",
    "iron_gear":    "circle",
    "copper_wire":  "line",
    "circuit":      "diamond",
    "machine_part": "star",
    "stone_brick":  "rect",
}

FURNACE_RECIPES = {
    "iron_ore":   {"output": "iron_plate",   "time": 3.2},
    "copper_ore": {"output": "copper_plate", "time": 3.2},
    "stone":      {"output": "stone_brick",  "time": 2.0},
}

ASSEMBLER_RECIPES = {
    "iron_gears": {
        "inputs": ["iron_plate", "iron_plate"],
        "output": "iron_gear",
        "time":   4.0,
        "tier":   1,
    },
    "copper_wires": {
        "inputs": ["copper_plate"],
        "output": "copper_wire",
        "time":   2.0,
        "tier":   1,
    },
    "circuits": {
        "inputs": ["iron_plate", "copper_wire", "copper_wire"],
        "output": "circuit",
        "time":   5.0,
        "tier":   1,
    },
    "machine_parts": {
        "inputs": ["iron_gear", "iron_plate", "circuit"],
        "output": "machine_part",
        "time":   8.0,
        "tier":   2,
    },
}

MARKET_BASE_PRICES = {
    "iron_plate":   6,
    "copper_plate": 5,
    "iron_gear":    9,
    "copper_wire":  4,
    "circuit":      18,
    "machine_part": 25,
    "stone_brick":  3,
}


ROCKET_REQUIREMENTS = {
    "machine_part": 1000,
    "circuit":       500,
    "money":       10000,
}

MEGAPROJECT_REQUIREMENTS = {
    "space_elevator": {"machine_part": 2000, "circuit": 1000, "iron_plate": 5000, "money": 50000},
    "fusion_reactor": {"machine_part": 3000, "circuit": 2000, "copper_wire": 5000, "money": 80000},
}


BIOMES = ["grassland", "desert", "forest"]

MAP_PRESETS = {
    "normal":         {"w": 100, "h":  80, "patches": (18, 32), "water": (3, 7),  "rare": True},
    "archipelago":    {"w": 120, "h": 100, "patches": (15, 25), "water": (12, 20), "rare": True},
    "desert":         {"w": 100, "h":  80, "patches": (20, 35), "water": (1, 2),  "rare": True},
    "rich_resources": {"w":  80, "h":  60, "patches": (30, 50), "water": (2, 4),  "rare": True},
    "hardcore":       {"w": 120, "h": 100, "patches": (8, 14),  "water": (5, 10), "rare": False},
}


WEATHER_TYPES = {
    "clear":   {"solar_mult": 1.0,  "energy_mult": 1.0,  "duration": (60, 180)},
    "rain":    {"solar_mult": 0.5,  "energy_mult": 1.0,  "duration": (30, 90)},
    "heat":    {"solar_mult": 1.2,  "energy_mult": 1.1,  "duration": (30, 90)},
    "wind":    {"solar_mult": 0.8,  "energy_mult": 0.95, "duration": (30, 120)},
    "storm":   {"solar_mult": 0.2,  "energy_mult": 1.2,  "duration": (20, 60)},
}


POLLUTION_SOURCES = {
    "coal_generator": 5.0,
    "furnace":        2.0,
    "assembler":      1.0,
    "miner":          0.5,
}
POLLUTION_DECAY = 0.1
MAX_POLLUTION = 100.0


MODULE_TYPES = {
    "speed":        {"speed_mult": 1.5, "energy_mult": 1.3, "pollution_mult": 1.2},
    "efficiency":   {"speed_mult": 0.9, "energy_mult": 0.6, "pollution_mult": 0.7},
    "productivity": {"speed_mult": 0.8, "energy_mult": 1.2, "pollution_mult": 1.5, "output_bonus": 0.1},
}

DISASTER_TYPES = [
    {"name": "Furnace Explosion",  "target": "furnace",        "chance": 0.0002},
    {"name": "Conveyor Jam",       "target": "belt",           "chance": 0.0003},
    {"name": "Power Outage",       "target": "coal_generator", "chance": 0.0001},
    {"name": "Meteor Strike",      "target": "any",            "chance": 0.00005},
]

ACHIEVEMENT_DEFS = [
    {"id": "first_ore",     "title": "First Ore",        "desc": "Mine your first ore",          "icon": "⛏"},
    {"id": "first_factory", "title": "First Factory",    "desc": "Complete a production chain",  "icon": "🏭"},
    {"id": "earn_1000",     "title": "Entrepreneur",     "desc": "Earn 1000$",                   "icon": "💰"},
    {"id": "earn_10000",    "title": "Tycoon",           "desc": "Earn 10000$",                  "icon": "💎"},
    {"id": "first_train",   "title": "Railroad Baron",   "desc": "Build a locomotive",           "icon": "🚂"},
    {"id": "first_robot",   "title": "Automation Master","desc": "Build a robot port",           "icon": "🤖"},
    {"id": "polluter",      "title": "Polluter",         "desc": "Reach 50% pollution",          "icon": "🏴"},
    {"id": "eco_friendly",  "title": "Eco Friendly",     "desc": "Use only solar panels",        "icon": "🌱"},
    {"id": "speed_demon",   "title": "Speed Demon",      "desc": "Produce 100 items/min",        "icon": "⚡"},
    {"id": "rocket",        "title": "To The Stars",     "desc": "Launch the rocket",            "icon": "🚀"},
]

DEFAULT_SETTINGS = {
    "fullscreen":       False,
    "vsync":            True,
    "show_grid":        True,
    "show_minimap":     True,
    "show_particles":   True,
    "show_item_labels": False,
    "autosave":         True,
    "camera_speed":     10,
    "ui_scale":         1.0,
    "font_size":        13,
    "colorblind_mode":  False,
    "high_contrast":    False,
    "zoom_idx":         DEFAULT_ZOOM_IDX,
    "map_preset":       "normal",
}