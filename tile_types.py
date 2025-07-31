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


SHROUD = np.array((ord(" "), (255, 255, 255), (20, 20, 20)), dtype=graphic_dt)


tree = new_tile(
    walkable=True,
    transparent=False,
    dark=(ord("↨"), (0, 255, 0), (30, 30, 30)),
    light=(ord("↨"), (0, 255, 0), (50, 50, 150)),
)
chair_horiz = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("¥"), (225, 225, 225), (100, 100, 100)),
    light=(ord("¥"), (255, 255, 255), (130, 130, 130)),
)


road = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (40, 40, 40)),
    light=(ord(" "), (255, 255, 255), (70, 70, 70)),
)

road_divider_horiz = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("═"), (225, 225, 0), (40, 40, 40)),
    light=(ord("═"), (255, 255, 0), (70, 70, 70)),
)
road_divider_vert = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("║"), (225, 225, 0), (40, 40, 40)),
    light=(ord("║"), (255, 255, 0), (70, 70, 70)),
)
road_divider_intersection = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("╬"), (255, 255, 0), (40, 40, 40)),
    light=(ord("╬"), (255, 255, 0), (70, 70, 70)),
)
stop_line_vert = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("▐"), (255, 255, 255), (40, 40, 40)),
    light=(ord("▐"), (255, 255, 255), (70, 70, 70)),
)
stop_line_horiz = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("_"), (255, 255, 255), (40, 40, 40)),
    light=(ord("_"), (255, 255, 255), (70, 70, 70)),
)
cement = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (70, 70, 70)),
    light=(ord(" "), (255, 255, 255), (100, 100, 100)),
)
floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (100, 100, 100)),
    light=(ord(" "), (255, 255, 255), (130, 130, 130)),
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
    dark=(ord("│"), (0, 0, 0), (70, 70, 70)),
    light=(ord("│"), (0, 0, 0), (100, 100, 100)),
)
vertical_window = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord("║"), (0, 0, 0), (70, 70, 70)),
    light=(ord("║"), (0, 0, 0), (100, 100, 100)),
)

horizontal_wall = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord("─"), (0, 0, 0), (70, 70, 70)),
    light=(ord("─"), (0, 0, 0), (100, 100, 100)),
)
horizontal_window = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord("═"), (0, 0, 0), (70, 70, 70)),
    light=(ord("═"), (0, 0, 0), (100, 100, 100)),
)

cross_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("┼"), (0, 0, 0), (70, 70, 70)),
    light=(ord("┼"), (0, 0, 0), (100, 100, 100)),
)
left_t_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("┤"), (0, 0, 0), (70, 70, 70)),
    light=(ord("┤"), (0, 0, 0), (100, 100, 100)),
)
right_t_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("├"), (0, 0, 0), (70, 70, 70)),
    light=(ord("├"), (0, 0, 0), (100, 100, 100)),
)
up_t_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("┴"), (0, 0, 0), (70, 70, 70)),
    light=(ord("┴"), (0, 0, 0), (100, 100, 100)),
)
down_t_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("┬"), (0, 0, 0), (70, 70, 70)),
    light=(ord("┬"), (0, 0, 0), (100, 100, 100)),
)
top_left_corner_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("┌"), (0, 0, 0), (70, 70, 70)),
    light=(ord("┌"), (0, 0, 0), (100, 100, 100)),
)
bottom_left_corner_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("└"), (0, 0, 0), (70, 70, 70)),
    light=(ord("└"), (0, 0, 0), (100, 100, 100)),
)
top_right_corner_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("┐"), (0, 0, 0), (70, 70, 70)),
    light=(ord("┐"), (0, 0, 0), (100, 100, 100)),
)
bottom_right_corner_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("┘"), (0, 0, 0), (70, 70, 70)),
    light=(ord("┘"), (0, 0, 0), (100, 100, 100)),
)


door = new_tile(
    walkable=True,
    transparent=False,
    dark=(ord("+"), (255, 255, 255), (70, 70, 70)),
    light=(ord("+"), (255, 255, 255), (100, 100, 100)),
)

EMPTY_TILES = [cement, floor, None]

INTERSECTION_WALL_TILES = [
    bottom_left_corner_wall,
    bottom_right_corner_wall,
    top_left_corner_wall,
    top_right_corner_wall,
    cross_wall,
    down_t_wall,
    up_t_wall,
    left_t_wall,
    right_t_wall,
]

FLAT_WALL_TILES = [
    vertical_wall,
    horizontal_wall,
]

WALL_TILES = INTERSECTION_WALL_TILES + FLAT_WALL_TILES
