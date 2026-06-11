#  PYFactory

A 2D factory-building game inspired by Factorio, built entirely in **Python + Pygame**.

Build miners, conveyor belts, smelters, and assemblers to create automated production lines.  
Research new technologies, manage power, survive disasters, and ultimately **launch a rocket** to win.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

##  Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/factory-automation.git
cd factory-automation

# Install dependencies
pip install pygame

# Run the game
python main.py
```

### Your First Factory (5 minutes)

```
[Iron Ore Tile] → [Miner] → [Belt →] → [Furnace] → [Belt →] → [Market] → $6
```

Press 1 → Place a Miner on an iron ore tile  
Press 2 → Place Belts pointing toward your factory  
Press 3 → Place a Furnace to smelt ore into plates  
Press 6 → Place a Market to sell products  
Press 8 → Build a Coal Generator for power  

Watch your money grow! 

Pro tip: Hold Shift + Click on any ore deposit to auto-build a complete Miner → Belt → Furnace → Market chain instantly!

---

##  Features

###  Core Gameplay
- 18 building types — miners, belts, furnaces, assemblers, generators, splitters, mergers, trains, robots, and more
- Multi-stage production chains — Ore → Plate → Gear → Machine Part
- Smooth item transport — visible items moving along conveyor belts
- Click-to-inspect buildings — detailed popup showing status, efficiency, inputs, outputs, and progress bars
- Deposit depletion — resources run out over time, forcing expansion and logistics planning

###  Energy System
- Coal Generators — 100 MW power production
- Solar Panels — passive generation affected by weather
- Power management — buildings shut down when demand exceeds supply
- Visual indicators — green / yellow / red status dots

###  Research Tree
- 10 technologies including faster miners, better furnaces, trains, robots
- Passive research point generation
- Visual tech tree overlay

### Trains & Logistics
- Rail network system
- Autonomous locomotives
- Train stations
- Splitters, mergers, underground belts

###  Logistic Robots
- Autonomous item transport
- Robot ports with battery system
- Flying logistics without belts

###  Procedural World
- Biomes: Grassland, Desert, Forest
- Rare resources: Titanium, Uranium, Gold
- Seed-based generation

###  Dynamic Systems
- Weather system affecting solar output
- Pollution mechanics
- Market price fluctuations
- Random disasters and events
- AI competitors

###  Progression
- 12 quests
- 10 achievements
- Rocket launch endgame

---

##  Controls

### Camera
- WASD / Arrow Keys — Move camera  
- Right-click + drag — Pan  
- Scroll — Zoom  
- F11 — Fullscreen  

### Buildings
- 1 Miner
- 2 Belt
- 3 Furnace
- 4 Inserter
- 5 Storage
- 6 Market
- 7 Assembler
- 8 Coal Generator
- 9 Solar Panel
- 0 Splitter

### Interaction
- Left click — Place
- Right click — Remove
- Shift + click — Auto-build chain
- ESC — Menu

---

##  Production Chains

### Basic
```
Iron Ore → Furnace → Iron Plate → Market ($6)
```

### Advanced
```
Iron Plate + Copper Wire → Circuit
Circuit + Gear → Machine Part
```

---

##  Power System

- Coal Generator: +100 MW
- Solar Panel: +40 MW
- Miner: -10 MW
- Furnace: -20 MW

If demand exceeds supply → buildings stop working.

---

##  Research Tree

Fast Miners → Better Furnace → Assembly Mk2 → Robots → Trains

---

##  Map Presets

- Normal — balanced
- Archipelago — islands
- Desert — copper rich
- Rich Resources — easy mode
- Hardcore — scarce resources

---

## Achievements

- First Ore
- Tycoon
- Automation Master
- To The Stars (rocket launch)

---

##  Project Structure

```
factory_automation/
├── main.py
├── constants.py
├── entities/
├── systems/
├── world/
├── ui/
├── utils/
└── save/
```

---

##  Technical Highlights

- Entity-based architecture
- 19 independent systems
- Chunk-based world optimization
- Delta-time simulation
- Modular UI system

---

##  Gameplay Tips

- Build power early
- Automate iron first
- Copper is a bottleneck
- Use shift-click auto-build
- Watch pollution levels

---

##  License

MIT License

---

 Credits

Inspired by Factorio by Wube Software Ltd.
Built using Python + Pygame.
