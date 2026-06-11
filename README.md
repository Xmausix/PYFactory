# Factory Automation — MVP

A 2D factory-building game made with Pygame. Build production lines, mine resources, smelt ore, and sell products for profit!

## Controls

| Key | Action |
|-----|--------|
| **WASD / Arrow Keys** | Pan camera |
| **1–5** | Select building type |
| **Q / E** | Rotate belt direction (when Belt selected) |
| **Left-click** | Place building |
| **Right-click** | Remove building (50% refund) |
| **F5** | Save game |
| **F9** | Load game |
| **P** | Pause / Resume |
| **ESC** | Deselect building |

## Requirements

- Python 3.8+
- Pygame 2.x

## Run

```bash
pip install pygame
cd factory_automation
python main.py
```

## Building Costs

| Building | Cost | Description |
|----------|------|-------------|
| **Miner** | $10 | Extracts iron ore or coal from resource tiles (1 item / 2s) |
| **Belt** | $2 | Transports items 1 tile / second |
| **Smelter** | $20 | Processes Iron Ore → Iron Ingot (3s) |
| **Storage** | $15 | Stores up to 100 items |
| **Market** | $30 | Sells products (Iron Ingot = $5) |

## Production Chain Example

```
[Iron Ore Tile]  →  [Miner]  →  [Belt →]  →  [Smelter]  →  [Belt →]  →  [Market]  →  $5
```

1. Place a **Miner** on an iron (grey) or coal (dark) tile
2. Place a **Belt** next to it pointing away
3. Add a **Smelter** to process ore into ingots
4. Connect to a **Market** to sell for $5 per ingot
5. Watch your money grow! 🚀

## Project Structure

```
factory_automation/
├── main.py              # Entry point — run this
├── entities/
│   ├── miner.py         # Resource extractor
│   ├── belt.py          # Conveyor transport
│   ├── smelter.py       # Ore → Ingot processor
│   ├── storage.py       # Item warehouse
│   └── market.py        # Product seller
├── systems/
│   ├── production.py    # Game loop logic
│   ├── economy.py       # Money management
│   └── placement.py     # Building placement
├── world/
│   ├── map.py           # Tile grid & generation
│   └── tile.py          # Tile data class
├── assets/              # (reserved for sprites)
└── save/
    └── world.json       # Auto-saved game state
```

## Future Phases

### Phase 2 — Visual Polish
- Map zoom
- Minimap
- Conveyor belt animations
- Particle effects

### Phase 3 — Advanced Features
- Technology research tree
- Automatic sorters
- Seed-based map generation
- Production statistics & charts

### Phase 4 — Complex Production
- Power/energy system
- Multi-stage factories:
  ```
  Iron Ore → Iron Ingot → Iron Plate → Machine Part → Sell
  ```
