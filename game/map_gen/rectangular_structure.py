from __future__ import annotations

from typing import List, Tuple
from game.utils.utility import slices_to_xys


class RectangularStructure:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height

    @property
    def x(self):
        return self.x1

    @property
    def y(self):
        return self.y1

    @property
    def w(self):
        return self.width

    @property
    def h(self):
        return self.height

    @property
    def as_tuple(self) -> List[int, int, int, int]:
        return [self.x1, self.y1, self.width, self.height]

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    @property
    def upper_left_center(self) -> Tuple[int, int]:
        x = int((self.x1 + self.x2) // 4)
        y = int((self.y1 + self.y2) // 4)
        return x, y

    @property
    def upper_right_center(self) -> Tuple[int, int]:
        x = int((self.x1 + self.x2) * 3 // 4)
        y = int((self.y1 + self.y2) // 4)
        return x, y

    @property
    def lower_left_center(self) -> Tuple[int, int]:
        x = int((self.x1 + self.x2) // 4)
        y = int((self.y1 + self.y2) * 3 // 4)
        return x, y

    @property
    def lower_right_center(self) -> Tuple[int, int]:
        x = int((self.x1 + self.x2) * 3 // 4)
        y = int((self.y1 + self.y2) * 3 // 4)
        return x, y

    @property
    def quadrant_centers(self) -> List[Tuple[int, int]]:
        return [
            (self.upper_left_center),
            (self.upper_right_center),
            (self.lower_left_center),
            (self.lower_right_center),
        ]

    @property
    def area(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1, self.x2 + 1), slice(self.y1, self.y2 + 1)

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def is_inside(self, x, y):
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2

    def intersects(self, other: RectangularStructure) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

    def abuts(self, other: "RectangularStructure") -> list[tuple[int, int]]:
        """
        Return a list of (x, y) coordinates along the common boundary between this rectangle and another.
        Coordinates are inclusive.
        """
        coords = []

        # Vertical boundaries
        if self.x2 == other.x1:  # self right edge touches other's left edge
            y_start = max(self.y1, other.y1)
            y_end = min(self.y2, other.y2)
            if y_start <= y_end:
                coords.extend([(self.x2, y) for y in range(y_start, y_end + 1)])

        if self.x1 == other.x2:  # self left edge touches other's right edge
            y_start = max(self.y1, other.y1)
            y_end = min(self.y2, other.y2)
            if y_start <= y_end:
                coords.extend([(self.x1, y) for y in range(y_start, y_end + 1)])

        # Horizontal boundaries
        if self.y2 == other.y1:  # self top touches other's bottom
            x_start = max(self.x1, other.x1)
            x_end = min(self.x2, other.x2)
            if x_start <= x_end:
                coords.extend([(x, self.y2) for x in range(x_start, x_end + 1)])

        if self.y1 == other.y2:  # self bottom touches other's top
            x_start = max(self.x1, other.x1)
            x_end = min(self.x2, other.x2)
            if x_start <= x_end:
                coords.extend([(x, self.y1) for x in range(x_start, x_end + 1)])

        return coords

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
            vertical_tiles.extend(((self.x1, y), (self.x2, y)))
        return vertical_tiles

    @property
    def horizontal_edges(self) -> List[Tuple[int, int]]:
        horizontal_tiles = []
        # Top and bottom edges
        for x in range(self.x1 + 1, self.x2):
            horizontal_tiles.extend(((x, self.y1), (x, self.y2)))
        return horizontal_tiles

    @property
    def edges(self) -> List[Tuple[int, int]]:
        return self.horizontal_edges + self.vertical_edges

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
