from __future__ import annotations

from typing import Tuple
from rectangular_structure import RectangularStructure


class Road(RectangularStructure):
    def __init__(self, pos: int, length: int, is_vert: int):
        if is_vert:
            x = pos - 1
            y = 0
            width = 3
            height = length
        else:
            x = 0
            y = pos - 1
            width = length
            height = 3

        self.pos = pos
        self.length = length
        self.is_vert = is_vert
        super().__init__(x, y, width, height)

    @property
    def center_line(self) -> Tuple[slice, slice]:
        """Return the center line area of this road as a 2D array index."""
        if self.is_vert:
            return slice(self.pos, self.pos + 1), slice(0, self.length)
        else:
            return (
                slice(0, self.length),
                slice(self.pos, self.pos + 1),
            )

    @property
    def lanes(self) -> Tuple[slice, slice]:
        """Return the lanes of this road as a 2D array index."""
        if self.is_vert:
            return slice(self.pos - 1, self.pos + 2, 2), slice(0, self.length)
        else:
            return (
                slice(0, self.length),
                slice(self.pos - 1, self.pos + 2, 2),
            )
