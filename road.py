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

    # def intersects(self, other: Road) -> bool:
    #     """Return True if this road overlaps with another Road."""
    #     return (
    #         self.x1 <= other.x2
    #         and self.x2 >= other.x1
    #         and self.y1 <= other.y2
    #         and self.y2 >= other.y1
    #     )

    # @property
    # def vertical_walls(self) -> Tuple[int, int]:
    #     vertical_tiles = []
    #     #  Left and right edges, excluding corners to avoid duplicates
    #     for y in range(self.y1 + 1, self.y2):
    #         vertical_tiles.append((self.x1, y))  # left
    #         vertical_tiles.append((self.x2, y))  # right
    #     return vertical_tiles

    # @property
    # def horizontal_walls(self) -> Tuple[int, int]:
    #     horizontal_tiles = []
    #     # Top and bottom edges
    #     for x in range(self.x1 + 1, self.x2):
    #         horizontal_tiles.append((x, self.y1))  # top
    #         horizontal_tiles.append((x, self.y2))  # bottom
    #     return horizontal_tiles

    # @property
    # def walls(self) -> Tuple[int, int]:
    #     return self.horizontal_walls + self.vertical_walls
