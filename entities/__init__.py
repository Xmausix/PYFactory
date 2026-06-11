from .miner import Miner
from .belt import Belt
from .smelter import Smelter
from .inserter import Inserter
from .storage import Storage
from .market import Market
from .assembler import Assembler
from .generator import Generator
from .splitter import Splitter
from .merger import Merger

ENTITY_MAP = {
    "miner": Miner,
    "belt": Belt,
    "smelter": Smelter,
    "inserter": Inserter,
    "storage": Storage,
    "market": Market,
    "assembler": Assembler,
    "generator": Generator,
    "splitter": Splitter,
    "merger": Merger,
}