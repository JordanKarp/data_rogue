from __future__ import annotations

from typing import List, Tuple


class RectangularStructure:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height

    @property
    def as_tuple(self) -> Tuple[int, int, int, int]:
        return self.x1, self.y1, self.width, self.height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularStructure) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

    @property
    def edges_and_corners(self) -> List[Tuple[int, int]]:
        return self.edges + self.corners

    @property
    def top_left_corner(self) -> Tuple[int, int]:
        return self.x1, self.y1

    @property
    def top_right_corner(self) -> Tuple[int, int]:
        return self.x2, self.y1

    @property
    def bottom_left_corner(self) -> Tuple[int, int]:
        return self.x1, self.y2

    @property
    def bottom_right_corner(self) -> Tuple[int, int]:
        return self.x2, self.y2

    @property
    def corners(self) -> List[Tuple[int, int]]:
        return [
            self.top_left_corner,
            self.top_right_corner,
            self.bottom_left_corner,
            self.bottom_right_corner,
        ]

    @property
    def vertical_edges(self) -> List[Tuple[int, int]]:
        vertical_tiles = []
        #  Left and right edges, excluding corners to avoid duplicates
        for y in range(self.y1 + 1, self.y2):
            vertical_tiles.append((self.x1, y))  # left
            vertical_tiles.append((self.x2, y))  # right
        return vertical_tiles

    @property
    def horizontal_edges(self) -> List[Tuple[int, int]]:
        horizontal_tiles = []
        # Top and bottom edges
        for x in range(self.x1 + 1, self.x2):
            horizontal_tiles.append((x, self.y1))  # top
            horizontal_tiles.append((x, self.y2))  # bottom
        return horizontal_tiles

    @property
    def edges(self) -> List[Tuple[int, int]]:
        return self.horizontal_edges + self.vertical_edges
