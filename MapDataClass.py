from dataclasses import dataclass


@dataclass
class WallData:
    x_pos: int
    y_pos: int
    direction: int

    def to_object(d: dict):
        return WallData(d["x_pos"], d["y_pos"], d["direction"])
