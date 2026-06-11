import pygame
from constants import (C_BAR, C_GRID_B, C_TXT, SIDE_PANEL_W,
                       TOP_BAR_H, C_MONEY, C_ITEMS,
                       C_ENERGY_OK, C_ENERGY_WARN, C_ENERGY_BAD,
                       ROCKET_REQUIREMENTS)


class InfoPanel:
    """Right-side panel: economy, stats, quests, building info."""

    def __init__(self, screen_w: int, screen_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.font  = pygame.font.SysFont("consolas,monospace", 13, bold=True)
        self.fontS = pygame.font.SysFont("consolas,monospace", 11)
        self.fontT = pygame.font.SysFont("consolas,monospace", 14, bold=True)
        self.scroll = 0

    def draw(self, screen, econ, energy, stats,
             quests, research, building, show: bool) -> None:
        px = self.screen_w - SIDE_PANEL_W
        pygame.draw.rect(screen, (28, 28, 42),
                         (px, 0, SIDE_PANEL_W, self.screen_h))
        pygame.draw.line(screen, C_GRID_B,
                         (px, 0), (px, self.screen_h), 2)

        y = TOP_BAR_H + 6
        pw = SIDE_PANEL_W - 12

        def header(text, color=(180, 180, 220)):
            nonlocal y
            pygame.draw.rect(screen, (40, 40, 60), (px + 4, y, pw, 18))
            screen.blit(self.fontT.render(text, True, color), (px + 6, y + 2))
            y += 22

        def row(text, color=C_TXT):
            nonlocal y
            screen.blit(self.fontS.render(text, True, color), (px + 8, y))
            y += 14

        # ── Economy ──
        header("💰 Economy")
        row(f"Money:  {econ.money}$", C_MONEY)
        row(f"Earned: {econ.total_earned}$")
        row(f"Spent:  {econ.total_spent}$")
        y += 4

        # ── Energy ──
        header("⚡ Energy", energy.status_color)
        row(f"Generated: {energy.total_generated} MW")
        row(f"Consumed:  {energy.total_consumed} MW")
        if energy.shortage:
            row(f"Shortage: {energy.shortage} MW", C_ENERGY_BAD)
        y += 4

        # ── Production Stats ──
        header("📊 Production /min")
        all_items = stats.all_items()
        if all_items:
            for item, rate in sorted(all_items.items(),
                                     key=lambda x: -x[1])[:6]:
                row(f"{item[:14]}: {rate:.1f}")
        else:
            row("(no production yet)")
        row(f"Money/min: {stats.money_per_minute():.1f}$", C_MONEY)
        y += 4

        # ── Research ──
        header("🔬 Research")
        row(f"Points: {research.research_points:.0f}")
        if research.active_research:
            tech = research.techs.get(research.active_research)
            if tech:
                pct = min(1.0, research.research_points / tech.cost)
                row(f"Researching: {tech.name}")
                # Progress bar
                bar_w = pw - 4
                pygame.draw.rect(screen, (50, 50, 70),
                                 (px + 6, y, bar_w, 8))
                pygame.draw.rect(screen, (80, 160, 255),
                                 (px + 6, y, int(bar_w * pct), 8))
                y += 12
        else:
            row("Press R to open research")
        y += 4

        # ── Quests ──
        header("🎯 Quests")
        done = quests.completed_count()
        total = len(quests.quests)
        row(f"Completed: {done}/{total}")
        for q in quests.quests[:5]:
            mark = "✓" if q.completed else "□"
            color = (100, 220, 100) if q.completed else C_TXT
            row(f"{mark} {q.title[:20]}", color)
        y += 4

        # ── Rocket Progress ──
        header("🚀 Rocket")
        for item, need in ROCKET_REQUIREMENTS.items():
            if item == "money":
                have = econ.money
            else:
                have = quests._total_produced(item)
            pct = min(1.0, have / need)
            color = (100, 220, 100) if pct >= 1.0 else C_TXT
            row(f"{item}: {have}/{need}", color)
        y += 4

        # ── Building Info ──
        if building:
            header("🏭 Selected Building")
            row(f"Type: {building.btype}")
            row(f"Pos:  ({building.x}, {building.y})")
            if hasattr(building, "direction"):
                row(f"Dir:  {building.direction}")
            if hasattr(building, "recipe"):
                row(f"Recipe: {building.recipe[:16]}")
            if hasattr(building, "items"):
                from collections import Counter
                counts = Counter(building.items)
                row(f"Items ({len(building.items)}):")
                for it, cnt in list(counts.items())[:4]:
                    row(f"  {it[:14]}: {cnt}")
            if hasattr(building, "sell_count"):
                row(f"Sold:  {building.sell_count}")
            if hasattr(building, "output_buffer"):
                row(f"Buffer:{len(building.output_buffer)}")
            if hasattr(building, "proc_item") and building.proc_item:
                row(f"Proc:  {building.proc_item}")
            if hasattr(building, "progress_pct"):
                pct = building.progress_pct
                bar_w = pw - 4
                pygame.draw.rect(screen, (50, 50, 70),
                                 (px + 6, y, bar_w, 8))
                pygame.draw.rect(screen, (255, 160, 40),
                                 (px + 6, y, int(bar_w * pct), 8))
                y += 12
            status = getattr(building, "status", "")
            if status:
                sc = {
                    "working": (80, 220, 100),
                    "waiting": (255, 200, 40),
                    "no_power": (255, 60, 60),
                    "idle": (120, 120, 120),
                }.get(status, C_TXT)
                row(f"Status: {status}", sc)