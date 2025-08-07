from __future__ import annotations

from typing import Tuple
from rectangular_structure import RectangularStructure


class RectangularRoad(RectangularStructure):
    def __init__(self, x: int, y: int, width: int, height: int, is_vert: bool):

        # self.x1 = x
        # self.y1 = y
        # self.width = width
        # self.height = height
        self.is_vert = is_vert
        super().__init__(x, y, width, height)

    @property
    def center_line(self) -> Tuple[slice, slice]:
        """Return the center line area of this road as a 2D array index."""
        if self.is_vert:
            return slice(self.x + 1, self.x + 2), slice(self.y, self.y + self.height)
        else:
            return (
                slice(self.x, self.x + self.width),
                slice(self.y + 1, self.y + 2),
            )

    @property
    def lanes(self) -> Tuple[slice, slice]:
        """Return the lanes of this road as a 2D array index."""
        if self.is_vert:
            return slice(self.x, self.x + 3, 2), slice(self.y, self.y + self.height)
        else:
            return (
                slice(self.x, self.x + self.width),
                slice(self.y, self.y + 3, 2),
            )


'''    @property
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
'''
