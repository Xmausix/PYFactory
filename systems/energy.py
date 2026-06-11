
from constants import B_POWER_USAGE
from entities import Generator


class EnergySystem:
    """Tracks power generation and consumption."""

    def __init__(self, gmap):
        self.gmap = gmap
        self.total_generated = 0
        self.total_consumed = 0
        self.powered = True

    def update(self) -> None:
        gen = sum(
            Generator.POWER_OUTPUT
            for b in self.gmap.buildings
            if b.btype == "generator"
        )
        con = sum(
            B_POWER_USAGE.get(b.btype, 0)
            for b in self.gmap.buildings
            if b.btype != "generator"
        )
        self.total_generated = gen
        self.total_consumed = con
        self.powered = gen >= con

        # Apply power state to all buildings
        for b in self.gmap.buildings:
            if b.btype == "generator":
                continue
            if hasattr(b, "powered"):
                # Only unpowered if total power fails
                b.powered = self.powered

    @property
    def status_color(self) -> tuple:
        from constants import C_ENERGY_OK, C_ENERGY_WARN, C_ENERGY_BAD
        ratio = self.total_consumed / max(1, self.total_generated)
        if ratio < 0.75:
            return C_ENERGY_OK
        if ratio < 1.0:
            return C_ENERGY_WARN
        return C_ENERGY_BAD

    @property
    def shortage(self) -> int:
        return max(0, self.total_consumed - self.total_generated)