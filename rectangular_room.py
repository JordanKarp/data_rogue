from __future__ import annotations

from typing import List, Tuple
from rectangular_structure import RectangularStructure
from utility import slices_to_xys


class RectangularRoom(RectangularStructure):
    def __init__(self, x: int, y: int, width: int, height: int, purpose: str = ""):
        super().__init__(x, y, width, height)
        self.purpose = purpose

    @property
    def along_inside_walls(self) -> List[Tuple[int, int]]:
        spots = []
        for x in range(self.x1 + 1, self.x2):
            spots.extend(((x, self.y1 + 1), (x, self.y2 - 1)))
        for y in range(self.y1 + 1, self.y2):
            spots.extend(((self.x1 + 1, y), (self.x2 - 1, y)))
        return spots

    @property
    def inner_away_from_walls(self) -> List[Tuple[int, int]]:
        return list(set(slices_to_xys(*self.inner)) - set(self.along_inside_walls))
