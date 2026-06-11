from .miner            import Miner
from .belt             import Belt, BeltItem
from .underground_belt import UndergroundBelt
from .smelter          import Furnace
from .inserter         import Inserter
from .storage          import Storage
from .market           import Market
from .assembler        import Assembler
from .generator        import CoalGenerator, SolarPanel
from .splitter         import Splitter, PrioritySplitter
from .merger           import Merger
from .train_station    import TrainStation
from .rail             import Rail
from .locomotive       import Locomotive
from .robot_port       import RobotPort
from .radar_station    import RadarStation

ENTITY_MAP = {
    "miner": Miner, "belt": Belt, "underground_belt": UndergroundBelt,
    "furnace": Furnace, "inserter": Inserter, "storage": Storage,
    "market": Market, "assembler": Assembler,
    "coal_generator": CoalGenerator, "solar_panel": SolarPanel,
    "splitter": Splitter, "priority_splitter": PrioritySplitter,
    "merger": Merger, "train_station": TrainStation, "rail": Rail,
    "locomotive": Locomotive, "robot_port": RobotPort,
    "radar_station": RadarStation,
}