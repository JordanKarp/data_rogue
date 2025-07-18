from typing import Tuple

import numpy as np  # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if this tile can be walked over.
        ("transparent", np.bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when this tile is in FOV.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types"""
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

device = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("☐"), (255, 255, 255), (30, 30, 30)),
    light=(ord("☐"), (255, 255, 255), (50, 50, 50)),
)
tree = new_tile(
    walkable=True,
    transparent=False,
    dark=(ord("↨"), (0, 255, 0), (30, 30, 30)),
    light=(ord("↨"), (0, 255, 0), (50, 50, 150)),
)


cement = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (10, 10, 10)),
    light=(ord(" "), (255, 255, 255), (20, 20, 20)),
)
floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (30, 30, 30)),
    light=(ord(" "), (255, 255, 255), (50, 50, 50)),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("█"), (255, 255, 255), (30, 30, 30)),
    light=(ord("█"), (255, 255, 255), (50, 50, 150)),
)
vertical_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("│"), (255, 255, 255), (30, 30, 30)),
    light=(ord("│"), (255, 255, 255), (50, 50, 50)),
)
vertical_window = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord("║"), (255, 255, 255), (30, 30, 30)),
    light=(ord("║"), (255, 255, 255), (50, 50, 50)),
)

horizontal_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("─"), (255, 255, 255), (30, 30, 30)),
    light=(ord("─"), (255, 255, 255), (50, 50, 50)),
)
horizontal_window = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord("═"), (255, 255, 255), (30, 30, 30)),
    light=(ord("═"), (255, 255, 255), (50, 50, 50)),
)
top_left_corner_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("┌"), (255, 255, 255), (30, 30, 30)),
    light=(ord("┌"), (255, 255, 255), (50, 50, 50)),
)
bottom_left_corner_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("└"), (255, 255, 255), (30, 30, 30)),
    light=(ord("└"), (255, 255, 255), (50, 50, 50)),
)
top_right_corner_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("┐"), (255, 255, 255), (30, 30, 30)),
    light=(ord("┐"), (255, 255, 255), (50, 50, 50)),
)
bottom_right_corner_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("┘"), (255, 255, 255), (30, 30, 30)),
    light=(ord("┘"), (255, 255, 255), (50, 50, 50)),
)


door = new_tile(
    walkable=True,
    transparent=False,
    dark=(ord("+"), (255, 255, 255), (30, 30, 30)),
    light=(ord("+"), (255, 255, 255), (50, 50, 50)),
)
