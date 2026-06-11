from entities import Market


class ProductionSystem:
    def __init__(self, gmap, econ, stats=None, quests=None, contracts=None):
        self.gmap      = gmap
        self.econ      = econ
        self.stats     = stats
        self.quests    = quests
        self.contracts = contracts

    def update(self, dt: float) -> None:
        for b in self.gmap.buildings:
            if hasattr(b, "update"):
                b.update(dt, self.gmap)
        for b in self.gmap.buildings:
            if b.btype == "miner":
                self._flush_buffer(b)
            elif b.btype in ("furnace", "assembler"):
                self._flush_output(b)

    def _flush_buffer(self, b) -> None:
        while getattr(b, "output_buffer", []):
            item = b.output_buffer[0]
            if self._deliver(b.x, b.y, item):
                b.output_buffer.pop(0)
                self._record(item)
            else:
                break

    def _flush_output(self, b) -> None:
        item = getattr(b, "output_item", None)
        if not item:
            return
        if self._deliver(b.x, b.y, item):
            b.output_item = None
            self._record(item)

    def _deliver(self, x, y, item) -> bool:
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nb = self.gmap.get_building(x + dx, y + dy)
            if nb is None:
                continue
            result = nb.accept_item(item)
            if isinstance(nb, Market) and isinstance(result, int) and result > 0:
                self.econ.earn(result)
                if self.stats:
                    self.stats.log_money(result)
                if self.contracts:
                    bonus = self.contracts.deliver(item)
                    if bonus > 0:
                        self.econ.earn(bonus)
                return True
            if result is True:
                return True
        return False

    def _record(self, item: str) -> None:
        if self.stats:
            self.stats.log_item(item)
        if self.quests:
            self.quests.record_produced(item)