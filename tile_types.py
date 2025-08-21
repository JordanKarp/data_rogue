from typing import Tuple

import color
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
        ("walkable", np.bool_),  # True if this tile can be walked over.
        ("transparent", np.bool_),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when this tile is in FOV.
        ("name", "U20"),  # Graphics for when this tile is in FOV.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    name: str,
) -> np.ndarray:
    """Helper function for defining individual tile types"""
    return np.array((walkable, transparent, dark, light, name), dtype=tile_dt)


SHROUD = np.array((ord(" "), (255, 255, 255), (20, 20, 20)), dtype=graphic_dt)


sink = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord("Θ"), color.white, color.dark_cement),
    light=(ord("Θ"), color.white, color.cement),
    name="sink",
)
underground = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), color.black, color.black),
    light=(ord(" "), color.black, color.black),
    name="underground",
)
underground = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), color.black, color.black),
    light=(ord(" "), color.black, color.black),
    name="underground",
)
sky = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord(" "), color.white, color.white),
    light=(ord(" "), color.white, color.white),
    name="sky",
)
tree = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord("↨"), (0, 65, 0), color.dark_soil),
    light=(ord("↨"), (0, 205, 0), color.soil),
    name="trees",
)
tree_2 = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord("▬"), (0, 65, 0), color.dark_soil),
    light=(ord("▬"), (0, 205, 0), color.soil),
    name="trees",
)
green_tree = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord("↨"), (0, 65, 0), color.dark_soil),
    light=(ord("↨"), (0, 155, 0), color.soil),
    name="trees",
)
green_tree_2 = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord("▬"), (0, 65, 0), color.dark_soil),
    light=(ord("▬"), (0, 155, 0), color.soil),
    name="trees",
)
dark_green_tree = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord("↨"), (0, 65, 0), color.dark_soil),
    light=(ord("↨"), (0, 105, 0), color.soil),
    name="trees",
)
dark_green_tree_2 = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord("▬"), (0, 65, 0), color.dark_soil),
    light=(ord("▬"), (0, 105, 0), color.soil),
    name="trees",
)
grass = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (0, 135, 0), (0, 135, 0)),
    light=(ord(" "), (0, 165, 0), (0, 165, 0)),
    name="grass",
)
green_grass = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (0, 125, 0), (0, 125, 0)),
    light=(ord(" "), (0, 155, 0), (0, 155, 0)),
    name="grass",
)
dark_green_grass = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (0, 115, 0), (0, 115, 0)),
    light=(ord(" "), (0, 145, 0), (0, 145, 0)),
    name="grass",
)


chair_horiz = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("¥"), (225, 225, 225), (100, 100, 100)),
    light=(ord("¥"), (255, 255, 255), (130, 130, 130)),
    name="chair",
)
table = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord("₧"), (87, 66, 66), (100, 100, 100)),
    light=(ord("₧"), (117, 96, 96), (130, 130, 130)),
    name="table",
)

up_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("τ"), (255, 255, 255), (100, 100, 100)),
    light=(ord("τ"), (255, 255, 255), (130, 130, 130)),
    name="stairs",
)
down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("Φ"), (255, 255, 255), (100, 100, 100)),
    light=(ord("Φ"), (255, 255, 255), (130, 130, 130)),
    name="stairs",
)
floor_num_1 = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("1"), (255, 255, 255), (100, 100, 100)),
    light=(ord("1"), (255, 255, 255), (130, 130, 130)),
    name="number 1",
)


road = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (225, 225, 255), color.dark_asphalt),
    light=(ord(" "), (255, 255, 255), (70, 70, 70)),
    name="road",
)

road_divider_horiz = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("═"), (225, 225, 0), color.dark_asphalt),
    light=(ord("═"), (255, 255, 0), color.asphalt),
    name="road",
)
road_divider_vert = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("║"), (225, 225, 0), color.dark_asphalt),
    light=(ord("║"), (255, 255, 0), color.asphalt),
    name="road",
)
road_divider_intersection = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("╬"), (225, 225, 0), color.dark_asphalt),
    light=(ord("╬"), (255, 255, 0), color.asphalt),
    name="road",
)
stop_line_vert = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("▐"), (225, 225, 225), color.dark_asphalt),
    light=(ord("▐"), (255, 255, 255), color.asphalt),
    name="road",
)
stop_line_horiz = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("_"), (255, 255, 255), color.dark_asphalt),
    light=(ord("_"), (255, 255, 255), color.asphalt),
    name="road",
)
cement = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (225, 225, 225), color.dark_cement),
    light=(ord(" "), (255, 255, 255), color.cement),
    name="cement",
)
floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (225, 225, 225), (100, 100, 100)),
    light=(ord(" "), (255, 255, 255), (130, 130, 130)),
    name="floor",
)
reserved_floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (225, 225, 225), (100, 99, 100)),
    light=(ord(" "), (255, 255, 255), (130, 130, 130)),
    name="floor",
)
reserved_cement = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (225, 225, 225), (70, 69, 70)),
    light=(ord(" "), (255, 255, 255), color.cement),
    name="floor",
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("█"), (225, 225, 225), (30, 30, 30)),
    light=(ord("█"), (255, 255, 255), (50, 50, 150)),
    name="wall",
)
vertical_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("║"), color.dark_wall, (70, 70, 70)),
    light=(ord("║"), color.wall, (100, 100, 100)),
    name="wall",
)
vertical_window = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord("│"), color.dark_wall, (70, 70, 70)),
    light=(ord("│"), color.wall, (100, 100, 100)),
    name="window",
)

horizontal_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("═"), color.dark_wall, (70, 70, 70)),
    light=(ord("═"), color.wall, (100, 100, 100)),
    name="wall",
)
horizontal_window = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord("─"), color.dark_wall, (70, 70, 70)),
    light=(ord("─"), color.wall, (100, 100, 100)),
    name="window",
)

cross_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("╬"), color.dark_wall, (70, 70, 70)),
    light=(ord("╬"), color.wall, (100, 100, 100)),
    name="wall",
)
left_t_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("╣"), color.dark_wall, (70, 70, 70)),
    light=(ord("╣"), color.wall, (100, 100, 100)),
    name="wall",
)
right_t_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("╠"), color.dark_wall, (70, 70, 70)),
    light=(ord("╠"), color.wall, (100, 100, 100)),
    name="wall",
)
up_t_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("╩"), color.dark_wall, (70, 70, 70)),
    light=(ord("╩"), color.wall, (100, 100, 100)),
    name="wall",
)
down_t_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("╦"), color.dark_wall, (70, 70, 70)),
    light=(ord("╦"), color.wall, (100, 100, 100)),
    name="wall",
)
top_left_corner_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("╔"), color.dark_wall, (70, 70, 70)),
    light=(ord("╔"), color.wall, (100, 100, 100)),
    name="wall",
)
bottom_left_corner_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("╚"), color.dark_wall, (70, 70, 70)),
    light=(ord("╚"), color.wall, (100, 100, 100)),
    name="wall",
)
top_right_corner_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("╗"), color.dark_wall, (70, 70, 70)),
    light=(ord("╗"), color.wall, (100, 100, 100)),
    name="wall",
)
bottom_right_corner_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("╝"), color.dark_wall, (70, 70, 70)),
    light=(ord("╝"), color.wall, (100, 100, 100)),
    name="wall",
)


door = new_tile(
    walkable=True,
    transparent=False,
    dark=(ord("+"), color.dark_wall, (70, 70, 70)),
    light=(ord("+"), color.wall, (100, 100, 100)),
    name="door",
)

bookcase_full = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("π"), color.wall, (70, 70, 70)),
    light=(ord("π"), (139, 115, 85), (100, 100, 100)),
    name="bookcase",
)
bookcase_empty = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("Σ"), color.wall, (70, 70, 70)),
    light=(ord("Σ"), (139, 115, 85), (100, 100, 100)),
    name="bookcase",
)

BOOKCASE_TILES = [bookcase_empty, bookcase_full]

TREE_TILES = [
    tree,
    green_tree,
    dark_green_tree,
    tree_2,
    green_tree_2,
    dark_green_tree_2,
]

GRASS_TILES = [
    grass,
    green_grass,
    dark_green_grass,
]

EMPTY_TILES = [cement, floor, None]

ROAD_TILES = [road, road_divider_intersection, road_divider_horiz, road_divider_vert]

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
