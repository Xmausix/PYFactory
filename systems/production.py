from entities import Market


class ProductionSystem:
    def __init__(self, gmap, econ, stats=None, quests=None):
        self.gmap = gmap
        self.econ = econ
        self.stats = stats
        self.quests = quests

    def update(self, dt: float) -> None:
        # Update all buildings
        for b in self.gmap.buildings:
            if hasattr(b, "update"):
                b.update(dt, self.gmap)

        # Deliver outputs
        for b in self.gmap.buildings:
            if b.btype == "miner":
                self._flush_miner(b)
            elif b.btype in ("smelter", "assembler"):
                self._flush_processor(b)

    def _flush_miner(self, b) -> None:
        while b.output_buffer:
            item = b.output_buffer[0]
            if self._deliver(b.x, b.y, item):
                b.output_buffer.pop(0)
                if self.stats:
                    self.stats.log_item(item)
                if self.quests:
                    self.quests.record_produced(item)
            else:
                break

    def _flush_processor(self, b) -> None:
        if not getattr(b, "output_item", None):
            return
        item = b.output_item
        if self._deliver(b.x, b.y, item):
            b.output_item = None
            if self.stats:
                self.stats.log_item(item)
            if self.quests:
                self.quests.record_produced(item)

    def _deliver(self, x: int, y: int, item: str) -> bool:
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nb = self.gmap.get_building(x + dx, y + dy)
            if nb:
                result = nb.accept_item(item)
                if isinstance(nb, Market) and isinstance(result, int) and result > 0:
                    self.econ.earn(result)
                    if self.stats:
                        self.stats.log_money(result)
                    return True
                if result is True:
                    return True
        return False