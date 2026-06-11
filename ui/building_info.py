import pygame
from constants import (C_PANEL, C_GRID_B, C_TXT, C_TXT_DIM, C_OK, C_WARN,
                        C_ERR, C_MONEY, B_POWER_USAGE, FURNACE_RECIPES,
                        ASSEMBLER_RECIPES, SIDE_PANEL_W, TOP_BAR_H)


class BuildingInfoPanel:
    """Detailed building info popup shown on click."""

    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.building = None
        self.visible  = False
        self.font     = pygame.font.SysFont("consolas,monospace", 14, bold=True)
        self.fontS    = pygame.font.SysFont("consolas,monospace", 12)

    def show(self, building) -> None:
        self.building = building
        self.visible  = True

    def hide(self) -> None:
        self.visible  = False
        self.building = None

    def draw(self, screen) -> None:
        if not self.visible or not self.building:
            return
        b  = self.building
        W  = 280
        H  = 340
        rx = (self.screen_w - SIDE_PANEL_W - W) // 2
        ry = (self.screen_h - H) // 2

        # Background
        pygame.draw.rect(screen, (22, 24, 36), (rx, ry, W, H))
        pygame.draw.rect(screen, C_GRID_B, (rx, ry, W, H), 2)

        y = ry + 8

        def header(text, color=(180, 185, 220)):
            nonlocal y
            screen.blit(self.font.render(text, True, color), (rx + 8, y))
            y += 20

        def row(text, color=C_TXT):
            nonlocal y
            screen.blit(self.fontS.render(text, True, color), (rx + 12, y))
            y += 16

        def bar(pct, color=C_OK, w_=W-24):
            nonlocal y
            pygame.draw.rect(screen, (40, 42, 60), (rx + 12, y, w_, 8))
            pygame.draw.rect(screen, color, (rx + 12, y, int(w_ * pct), 8))
            y += 12

        # Title
        header(f"🏭 {b.btype.replace('_', ' ').title()}")
        row(f"Position: ({b.x}, {b.y})")

        # Status
        status = getattr(b, "status", "unknown")
        sc = {
            "working": C_OK, "waiting": C_WARN,
            "no_power": C_ERR, "idle": C_TXT_DIM,
        }.get(status, C_TXT)
        row(f"Status: {status}", sc)

        # Power
        pwr = B_POWER_USAGE.get(b.btype, 0)
        if pwr > 0:
            row(f"Power: {pwr} MW")

        # Direction
        if hasattr(b, "direction"):
            row(f"Direction: {b.direction}")

        # Module
        if hasattr(b, "module"):
            mod = b.module or "None"
            row(f"Module: {mod}")

        y += 4

        # Type-specific info
        if b.btype == "furnace":
            header("Processing")
            if b.proc_item:
                recipe = FURNACE_RECIPES.get(b.proc_item, {})
                row(f"Input:  {b.proc_item}")
                row(f"Output: {recipe.get('output', '?')}")
                row(f"Progress:")
                bar(b.progress_pct, C_PROG_FG if hasattr(b, "progress_pct") else C_OK)
            else:
                row("Idle - no input", C_TXT_DIM)
            if hasattr(b, "efficiency"):
                row(f"Efficiency: {b.efficiency * 100:.0f}%")
            row(f"Processed: {getattr(b, 'output_count', 0)}")

        elif b.btype == "assembler":
            header("Assembly")
            recipe_data = ASSEMBLER_RECIPES.get(b.recipe, {})
            row(f"Recipe: {b.recipe}")
            if recipe_data:
                row(f"Inputs: {', '.join(recipe_data['inputs'])}")
                row(f"Output: {recipe_data['output']}")
            row(f"Buffer: {len(b.input_buffer)}/{len(recipe_data.get('inputs', []))}")
            if b.proc_item:
                row("Progress:")
                bar(b.progress_pct)
            row(f"Produced: {getattr(b, 'output_count', 0)}")
            if hasattr(b, "efficiency"):
                row(f"Efficiency: {b.efficiency * 100:.0f}%")

        elif b.btype == "miner":
            header("Mining")
            row(f"Buffer: {len(b.output_buffer)}/{b.MAX_BUFFER}")
            tile = None
            row(f"Speed: {b.PRODUCTION_TIME:.1f}s/item")

        elif b.btype == "storage":
            header("Storage")
            row(f"Items: {len(b.items)}/{b.CAPACITY}")
            bar(b.fill_pct, (80, 160, 255) if b.fill_pct < 0.9 else C_ERR)
            counts = b.counts
            for item_name, cnt in list(counts.items())[:5]:
                row(f"  {item_name}: {cnt}")

        elif b.btype == "market":
            header("Sales")
            row(f"Sold: {b.sell_count} items")
            row(f"Earned: {b.total_earned}$", C_MONEY)

        elif b.btype == "coal_generator":
            header("Power Generation")
            row(f"Fuel: {b.fuel} coal")
            row(f"Output: {b.current_output} MW")
            row(f"Active: {'Yes' if b.active else 'No'}")

        elif b.btype == "train_station":
            header("Station")
            row(f"Mode: {b.mode}")
            row(f"Items: {len(b.items)}/{b.CAPACITY}")

        elif b.btype == "robot_port":
            header("Robot Port")
            row(f"Robots: {len(b.robots)}/{b.MAX_BOTS}")
            row(f"Output buffer: {len(b.output_buffer)}")
            row(f"Input buffer: {len(b.input_buffer)}")

        # Close hint
        y = ry + H - 20
        screen.blit(self.fontS.render("Click elsewhere to close", True, C_TXT_DIM), (rx + 8, y))


# Need this import for the bar color
from constants import C_PROG_FG