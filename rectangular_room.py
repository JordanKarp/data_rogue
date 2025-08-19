from __future__ import annotations

from typing import List, Tuple
from rectangular_structure import RectangularStructure


class RectangularRoom(RectangularStructure):
    def __init__(self, x: int, y: int, width: int, height: int, purpose: str = ""):
        super().__init__(x, y, width, height)
        self.purpose = purpose
