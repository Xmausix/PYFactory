import pygame
from constants import (C_PANEL, C_GRID_B, C_TXT, C_TXT_DIM,
                       C_MONEY, C_ITEMS, C_OK, C_WARN, C_ERR,
                       SIDE_PANEL_W, TOP_BAR_H, ROCKET_REQUIREMENTS)
from .charts import MiniChart


_STATUS_COLORS = {
    "working":  C_OK,
    "waiting":  C_WARN,
    "no_power": C_ERR,
    "idle":     (90, 90, 110),
}


class Dashboard:
    """Right-side panel: economy · energy · stats · research · quests · rocket."""

    def __init__(self, screen_w: int, screen_h: int):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self._chart   = MiniChart(SIDE_PANEL_W - 20, 38)
        self.font  = pygame.font.SysFont("consolas,monospace", 13, bold=True)
        self.fontS = pygame.font.SysFont("consolas,monospace", 11)
        self.fontT = pygame.font.SysFont("consolas,monospace", 14, bold=True)

    def draw(self, screen: pygame.Surface,
             econ, energy, stats,
             quests, research, building,
             autosave_msg: str) -> None:

        px = self.screen_w - SIDE_PANEL_W
        pw = SIDE_PANEL_W
        pygame.draw.rect(screen, C_PANEL, (px, 0, pw, self.screen_h))
        pygame.draw.line(screen, C_GRID_B, (px, 0), (px, self.screen_h), 2)

        y = TOP_BAR_H + 4

        def header(txt: str, color=(160, 165, 210)) -> None:
            nonlocal y
            pygame.draw.rect(screen, (36, 38, 58), (px + 2, y, pw - 4, 17))
            screen.blit(self.fontT.render(txt, True, color), (px + 5, y + 1))
            y += 20

        def row(txt: str, color=C_TXT) -> None:
            nonlocal y
            if y + 14 > self.screen_h - 4:
                return
            screen.blit(self.fontS.render(txt, True, color), (px + 7, y))
            y += 13

        def gap(n: int = 3) -> None:
            nonlocal y
            y += n

        header("💰 Economy")
        row(f"Money  : {econ.money:,}$",       C_MONEY)
        row(f"Earned : {econ.total_earned:,}$")
        row(f"Spent  : {econ.total_spent:,}$",  C_TXT_DIM)
        mpm = stats.money_per_minute()
        row(f"$/min  : {mpm:.1f}",              C_MONEY)
        gap()
        self._chart.draw(screen, px + 6, y,
                         stats.history_money(SIDE_PANEL_W - 20),
                         C_MONEY, "$/min", "$")
        y += 42
        gap()

        header("⚡ Energy", energy.status_color)
        row(f"Generated : {energy.total_generated} MW")
        row(f"Consumed  : {energy.total_consumed} MW")
        if energy.shortage:
            row(f"⚠ Shortage: {energy.shortage} MW", C_ERR)
        if energy.overload_timer > 0:
            row(f"Overloaded: {energy.overload_timer:.0f}s", C_WARN)
        # Power bar
        cap = max(1, energy.total_generated)
        pct = min(1.0, energy.total_consumed / cap)
        bw  = pw - 14
        pygame.draw.rect(screen, (40, 42, 60), (px + 7, y, bw, 8))
        bar_color = C_OK if pct < 0.75 else C_WARN if pct < 1.0 else C_ERR
        pygame.draw.rect(screen, bar_color, (px + 7, y, int(bw * pct), 8))
        y += 12
        gap()


        header("📊 Production /min")
        all_items = stats.all_items()
        if all_items:
            for item, rate in sorted(
                    all_items.items(), key=lambda kv: -kv[1])[:6]:
                row(f"{item[:16]}: {rate:.1f}")
        else:
            row("(no data yet)", C_TXT_DIM)
        gap()


        header("🔬 Research")
        row(f"Points : {research.research_points:.0f} RP")
        if research.active_research:
            tech = research.techs.get(research.active_research)
            if tech:
                pct = min(1.0, research.research_points / max(1, tech.cost))
                row(f"▶ {tech.name[:18]}")
                bw  = pw - 14
                pygame.draw.rect(screen, (40, 42, 60), (px + 7, y, bw, 7))
                pygame.draw.rect(screen, (80, 150, 255),
                                 (px + 7, y, int(bw * pct), 7))
                y += 10
        else:
            row("[R] Open research tree", C_TXT_DIM)
        gap()


        header("🎯 Quests")
        done  = quests.completed_count()
        total = len(quests.quests)
        row(f"Progress : {done}/{total}")
        for q in quests.quests[:6]:
            mark  = "✓" if q.completed else "□"
            color = C_OK if q.completed else C_TXT
            row(f"{mark} {q.title[:22]}", color)
        gap()


        header("🚀 Rocket")
        for item, need in ROCKET_REQUIREMENTS.items():
            have  = econ.money if item == "money" else quests.total_produced(item)
            pct   = min(1.0, have / need)
            color = C_OK if pct >= 1.0 else C_TXT
            row(f"{item}: {have}/{need}", color)
        gap()


        if building:
            header("🏭 Building")
            row(f"Type   : {building.btype}")
            row(f"Pos    : ({building.x},{building.y})")
            if hasattr(building, "direction"):
                row(f"Dir    : {building.direction}")
            if hasattr(building, "recipe"):
                row(f"Recipe : {building.recipe[:16]}")
            if hasattr(building, "items") and building.items:
                from collections import Counter
                cnts = Counter(
                    it if isinstance(it, str) else it.name
                    for it in building.items)
                row(f"Items ({len(building.items)}):")
                for it, cnt in list(cnts.items())[:4]:
                    row(f"  {it[:14]}: {cnt}")
            if hasattr(building, "output_buffer"):
                row(f"Buffer : {len(building.output_buffer)}")
            if hasattr(building, "fuel"):
                row(f"Fuel   : {building.fuel} coal")
            if hasattr(building, "proc_item") and building.proc_item:
                row(f"Proc   : {building.proc_item}")
            if hasattr(building, "progress_pct") and building.progress_pct > 0:
                pct = building.progress_pct
                bw  = pw - 14
                pygame.draw.rect(screen, (40, 42, 60), (px + 7, y, bw, 7))
                pygame.draw.rect(screen, (255, 160, 40),
                                 (px + 7, y, int(bw * pct), 7))
                y += 10
            status = getattr(building, "status", "")
            if status:
                sc = _STATUS_COLORS.get(status, C_TXT)
                row(f"Status : {status}", sc)
            gap()


        if autosave_msg:
            row(autosave_msg, C_TXT_DIM)