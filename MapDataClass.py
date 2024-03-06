from dataclasses import dataclass
from enum import Enum
import json


@dataclass
class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4


@dataclass
class WallData:
    x_pos: int
    y_pos: int
    direction: int

    def to_object(d: dict):
        return WallData(d["x_pos"], d["y_pos"], d["direction"])
