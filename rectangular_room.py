from __future__ import annotations

from typing import List, Tuple
from rectangular_structure import RectangularStructure


class RectangularRoom(RectangularStructure):
    def __init__(self, x: int, y: int, width: int, height: int, purpose: str = ""):
        super().__init__(x, y, width, height)
        self.purpose = purpose

    @property
    def along_inside_walls(self) -> List[Tuple[int, int]]:
        spots = []
        for x in range(self.x1 + 1, self.x2 - 1):
            spots.append((x, self.y1 + 1))  # top
            spots.append((x, self.y2 - 1))  # bottom
        for y in range(self.y1 + 1, self.y2 - 1):
            spots.append((self.x1 + 1, y))  # left
            spots.append((self.x2 - 1, y))  # right

        return spots
