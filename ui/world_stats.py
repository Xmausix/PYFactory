import pygame
from constants import C_GRID_B, C_TXT, C_TXT_DIM, C_MONEY, SIDE_PANEL_W


class WorldStatsUI:
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.visible  = False
        self.font     = pygame.font.SysFont("consolas,monospace", 16, bold=True)
        self.fontS    = pygame.font.SysFont("consolas,monospace", 12)

    def toggle(self):
        self.visible = not self.visible

    def draw(self, screen, gmap, econ, stats, pollution, weather, competitors):
        if not self.visible:
            return
        ov = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 200))
        screen.blit(ov, (0, 0))
        W, H = min(500, self.screen_w - 40), min(450, self.screen_h - 40)
        rx = (self.screen_w - W) // 2
        ry = (self.screen_h - H) // 2
        pygame.draw.rect(screen, (22, 24, 38), (rx, ry, W, H))
        pygame.draw.rect(screen, C_GRID_B, (rx, ry, W, H), 2)

        y = ry + 12

        def header(text):
            nonlocal y
            screen.blit(self.font.render(text, True, (180, 185, 220)), (rx + 12, y))
            y += 22

        def row(text, color=C_TXT):
            nonlocal y
            screen.blit(self.fontS.render(text, True, color), (rx + 16, y))
            y += 16

        header("🌎 World Statistics")
        row(f"Buildings:      {len(gmap.buildings)}")
        belts = sum(1 for b in gmap.buildings if b.btype in ("belt", "underground_belt"))
        row(f"Belts:          {belts}")
        items_moving = sum(len(getattr(b, "items", [])) for b in gmap.buildings)
        row(f"Items Moving:   {items_moving}")
        row(f"Money Earned:   {econ.total_earned:,}$", C_MONEY)
        row(f"Money Spent:    {econ.total_spent:,}$")
        y += 6
        header("🌦 Weather")
        row(f"Current: {weather.current}")
        y += 6
        header("🏴 Pollution")
        row(f"Level: {pollution.level:.1f} / {100.0} ({pollution.pct*100:.0f}%)")
        y += 6
        header("📊 Production")
        all_items = stats.all_items()
        for item, rate in sorted(all_items.items(), key=lambda x: -x[1])[:8]:
            row(f"  {item}: {rate:.1f}/min")
        y += 6
        header("🏢 Ranking")
        ranking = competitors.get_ranking(stats.total_items_per_minute(), econ.money)
        for i, (name, prod) in enumerate(ranking[:5]):
            marker = " ◀" if name == "You" else ""
            row(f"  {i+1}. {name}: {prod:.0f}/min{marker}")

        row("")
        row("[I] Close", C_TXT_DIM)