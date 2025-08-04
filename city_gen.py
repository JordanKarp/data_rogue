from typing import List, Tuple
import random

from game_map import GameMap
from rectangular_structure import RectangularStructure
from rectangular_road import RectangularRoad
from rectangular_room import RectangularRoom
import tile_types
import entity_factory
from utility import slices_to_xys


def new_generate_city(engine, map_width, map_height):
    MIN_BLOCK_SIZE = 10
    BLOCK_DIVISION_DEPTH = 9

    player = engine.player
    city = GameMap(engine, map_width, map_height, entities=[player])

    # city_blocks, road_dimensions = generate_city_blocks(
    #     city_width=map_width,
    #     city_height=map_height,
    #     block_min=10,
    #     block_max=15,
    # )
    city_blocks, road_dimensions = subdivide_grid_with_roads(
        map_width, map_height, MIN_BLOCK_SIZE, BLOCK_DIVISION_DEPTH
    )
    roads = generate_roads(city, road_dimensions)
    structures = generate_structures(city, city_blocks)
    generate_actors(city, player, structures, roads)

    return city


def subdivide_grid_with_roads(
    width: int = 40, height: int = 20, min_size: int = 6, max_depth: int = 4
) -> Tuple[List[Tuple[int, int, int, int]], List[Tuple[int, int, int, int]]]:
    """
    Returns two lists of rectangles:
      - blocks: (x, y, width, height) for city blocks
      - roads:  (x, y, width, height) for roads
    """
    ROAD_WIDTH = 3
    blocks: List[RectangularStructure] = []
    roads: List[RectangularStructure] = []

    def split(x: int, y: int, w: int, h: int, depth: int):
        # Stop splitting if block is too small or depth limit is reached
        if depth == 0 or (
            w < min_size * 2 + ROAD_WIDTH and h < min_size * 2 + ROAD_WIDTH
        ):
            blocks.append(RectangularStructure(x + 1, y + 1, w - 3, h - 3))
            return

        split_horizontally = random.choice([True, False])
        if w < min_size * 2 + ROAD_WIDTH:
            split_horizontally = True
        elif h < min_size * 2 + ROAD_WIDTH:
            split_horizontally = False

        if split_horizontally:
            # Horizontal split
            split_line = random.randint(min_size, h - min_size - ROAD_WIDTH)
            # Add the horizontal road
            roads.append(RectangularStructure(x, y + split_line, w, ROAD_WIDTH))
            # Split the two sub-blocks
            split(x, y, w, split_line, depth - 1)
            split(
                x,
                y + split_line + ROAD_WIDTH,
                w,
                h - split_line - ROAD_WIDTH,
                depth - 1,
            )
        else:
            # Vertical split
            split_line = random.randint(min_size, w - min_size - ROAD_WIDTH)
            # Add the vertical road
            roads.append(RectangularStructure(x + split_line, y, ROAD_WIDTH, h))
            # Split the two sub-blocks
            split(x, y, split_line, h, depth - 1)
            split(
                x + split_line + ROAD_WIDTH,
                y,
                w - split_line - ROAD_WIDTH,
                h,
                depth - 1,
            )

    split(0, 0, width, height, max_depth)
    roads = merge_continuous_roads(roads)
    return [block.as_tuple for block in blocks], [road.as_tuple for road in roads]


def merge_continuous_roads(
    roads: list[RectangularStructure],
) -> list[RectangularStructure]:
    merged = roads[:]
    changed = True

    while changed:
        changed = False
        new_list = []
        skip = set()

        for i, r1 in enumerate(merged):
            if i in skip:
                continue
            merged_this = False
            for j, r2 in enumerate(merged):
                if j <= i or j in skip:
                    continue

                # Horizontal merge (same y, same width)
                if (
                    r1.y1 == r2.y1
                    and r1.height == r2.height
                    and r1.x1 + r1.width == r2.x1
                ):
                    new_list.append(
                        RectangularStructure(
                            r1.x1, r1.y1, r1.width + r2.width, r1.height
                        )
                    )
                    skip.add(j)
                    merged_this = True
                    changed = True
                    break

                # Vertical merge (same x, same width)
                if (
                    r1.x1 == r2.x1
                    and r1.width == r2.width
                    and r1.y1 + r1.height == r2.y1
                ):
                    new_list.append(
                        RectangularStructure(
                            r1.x1, r1.y1, r1.width, r1.height + r2.height
                        )
                    )
                    skip.add(j)
                    merged_this = True
                    changed = True
                    break

            if not merged_this:
                new_list.append(r1)

        merged = new_list

    return merged


def generate_roads(city, road_dimensions):
    # Determine road sizes and number

    roads = []

    for x, y, w, h in road_dimensions:
        is_vertical = True if w < h else False
        road = RectangularRoad(x, y, w, h, is_vertical)
        divider_tile = (
            tile_types.road_divider_vert
            if is_vertical
            else tile_types.road_divider_horiz
        )

        city.tiles[road.center_line] = divider_tile
        city.tiles[road.lanes] = tile_types.road

        for other_road in roads:
            if road.intersects(other_road):
                generate_intersection(city, road, other_road)

        roads.append(road)

    return roads


def generate_intersection(city, road, other_road):
    pass


def generate_structures(city, block_dimensions):
    # Determine lot sizes and type
    structures = []

    for x, y, w, h in block_dimensions:
        # determine size
        structure = RectangularRoom(x, y, w, h)

        if any(structure.intersects(other_structure) for other_structure in structures):
            continue

        generate_flooring(city, structure, tile_types.floor)
        # generate_outer_walls(city, structure)
        generate_walls(city, structure)

        rooms = subdivide_structure(structure)
        for room in rooms:
            generate_walls(city, room)
            generate_outer_doors(city, room)

        # generate_windows(city, structure)
        generate_outer_doors(city, structure)

        chair_spot = random.choices(structure.along_inside_walls, k=12)
        for spot in chair_spot:
            if city.tiles[spot] in tile_types.EMPTY_TILES:
                city.tiles[spot] = tile_types.chair_horiz

        structures.append(structure)

    return structures


def subdivide_structure(structure: RectangularStructure) -> list[RectangularRoom]:
    aspect_ratio = structure.width / structure.height

    # Adjust grid based on shape
    if aspect_ratio > 1.5:
        # Very wide
        cols = random.randint(3, 4)
        rows = random.randint(1, 2)
    elif aspect_ratio < 0.67:
        # Very tall
        cols = random.randint(1, 2)
        rows = random.randint(3, 4)
    else:
        # More balanced
        cols = random.randint(2, 3)
        rows = random.randint(2, 3)

    room_width = structure.width // cols
    room_height = structure.height // rows

    rooms = []
    for r in range(rows):
        for c in range(cols):
            x = structure.x1 + c * room_width
            y = structure.y1 + r * room_height

            # Possibly vary room size slightly (last row/col gets remainder)
            w = room_width if c < cols - 1 else structure.x1 + structure.width - x
            h = room_height if r < rows - 1 else structure.y1 + structure.height - y

            rooms.append(RectangularRoom(x, y, w, h))

    return rooms


def generate_walls(city, structure: RectangularStructure, wall_type=None):
    for spot in structure.edges_and_corners:
        if spot in structure.vertical_edges:
            city.tiles[spot] = tile_types.vertical_wall
            continue
        if spot in structure.horizontal_edges:
            city.tiles[spot] = tile_types.horizontal_wall
            continue

        if spot == structure.top_left_corner:
            if city.tiles[spot] in [
                tile_types.bottom_left_corner_wall,
                tile_types.right_t_wall,
            ]:
                city.tiles[spot] = tile_types.right_t_wall
            elif city.tiles[spot] in [
                tile_types.top_right_corner_wall,
                tile_types.down_t_wall,
            ]:
                city.tiles[spot] = tile_types.down_t_wall
            elif city.tiles[spot] in [
                tile_types.bottom_right_corner_wall,
                tile_types.cross_wall,
                tile_types.left_t_wall,
                tile_types.up_t_wall,
            ]:
                city.tiles[spot] = tile_types.cross_wall
            else:
                city.tiles[spot] = tile_types.top_left_corner_wall
            continue
        elif spot == structure.top_right_corner:
            if city.tiles[spot] in [
                tile_types.bottom_right_corner_wall,
                tile_types.left_t_wall,
            ]:
                city.tiles[spot] = tile_types.left_t_wall
            elif city.tiles[spot] in [
                tile_types.top_left_corner_wall,
                tile_types.down_t_wall,
            ]:
                city.tiles[spot] = tile_types.down_t_wall
            elif city.tiles[spot] in [
                tile_types.bottom_left_corner_wall,
                tile_types.cross_wall,
                tile_types.right_t_wall,
                tile_types.up_t_wall,
            ]:
                city.tiles[spot] = tile_types.cross_wall
            else:
                city.tiles[spot] = tile_types.top_right_corner_wall
        elif spot == structure.bottom_left_corner:
            if city.tiles[spot] in [
                tile_types.top_left_corner_wall,
                tile_types.right_t_wall,
            ]:
                city.tiles[spot] = tile_types.right_t_wall
            elif city.tiles[spot] in [
                tile_types.bottom_right_corner_wall,
                tile_types.up_t_wall,
            ]:
                city.tiles[spot] = tile_types.up_t_wall
            elif city.tiles[spot] in [
                tile_types.top_right_corner_wall,
                tile_types.cross_wall,
                tile_types.left_t_wall,
                tile_types.down_t_wall,
            ]:
                city.tiles[spot] = tile_types.cross_wall
            else:
                city.tiles[spot] = tile_types.bottom_left_corner_wall
        elif spot == structure.bottom_right_corner:
            if city.tiles[spot] in [
                tile_types.top_right_corner_wall,
                tile_types.left_t_wall,
            ]:
                city.tiles[spot] = tile_types.left_t_wall
            elif city.tiles[spot] in [
                tile_types.bottom_left_corner_wall,
                tile_types.up_t_wall,
            ]:
                city.tiles[spot] = tile_types.up_t_wall
            elif city.tiles[spot] in [
                tile_types.top_left_corner_wall,
                tile_types.cross_wall,
                tile_types.right_t_wall,
                tile_types.down_t_wall,
            ]:
                city.tiles[spot] = tile_types.cross_wall
            else:
                city.tiles[spot] = tile_types.bottom_right_corner_wall
        else:
            city.tiles[spot] = tile_types.wall


# def generate_inner_walls(city, structure, room):
#     for spot in room.edges_and_corners:
#         if spot in structure.edges_and_corners:
#             continue
#         if spot in room.vertical_edges:
#             city.tiles[spot] = tile_types.vertical_wall
#         elif spot in room.horizontal_edges:
#             city.tiles[spot] = tile_types.horizontal_wall


def generate_flooring(city, structure, floor_tile=tile_types.floor):
    city.tiles[structure.inner] = floor_tile


# def generate_outer_walls(city, structure):
#     # Walls
#     for wall in structure.vertical_edges:
#         city.tiles[wall] = tile_types.vertical_wall
#     for wall in structure.horizontal_edges:
#         city.tiles[wall] = tile_types.horizontal_wall

#     # Corners
#     city.tiles[structure.top_left_corner] = tile_types.top_left_corner_wall
#     city.tiles[structure.bottom_left_corner] = tile_types.bottom_left_corner_wall
#     city.tiles[structure.top_right_corner] = tile_types.top_right_corner_wall
#     city.tiles[structure.bottom_right_corner] = tile_types.bottom_right_corner_wall


def generate_windows(city, structure, number_of_windows=4):
    windows_each = max(0, number_of_windows // 2)

    if len(structure.horizontal_edges) > windows_each:
        h_window_spots = random.sample(structure.horizontal_edges, k=windows_each)
        for spot in h_window_spots:
            if city.tiles[spot] in tile_types.FLAT_WALL_TILES:
                city.tiles[spot] = tile_types.horizontal_window

    if len(structure.vertical_edges) > windows_each:
        v_windows = random.sample(structure.vertical_edges, k=windows_each)
        for spot in v_windows:
            if city.tiles[spot] in tile_types.FLAT_WALL_TILES:
                city.tiles[spot] = tile_types.vertical_window


def generate_outer_doors(city, structure):
    while True:
        door_spot = random.choice(structure.edges)
        if city.tiles[door_spot] in tile_types.FLAT_WALL_TILES:
            city.tiles[door_spot] = tile_types.door
            return


def generate_living_room():
    pass


def generate_kitchen():
    pass


def generate_bathroom():
    pass


def generate_office():
    pass


def generate_retail():
    pass


def generate_park():
    pass


def generate_actors(city, player, structures, roads):
    generate_player(city, player, structures)
    generate_npcs(city, structures, roads)
    generate_items(city, structures)


def generate_player(city, player, structures):
    while True:
        random_room = random.choice(structures)
        spot = random.choice(slices_to_xys(*(random_room.inner)))
        if city.tiles[spot] not in tile_types.WALL_TILES:
            player.place(*spot, city)
            return


def generate_npcs(city, structures, roads):
    npcs_to_generate = 46
    while npcs_to_generate:
        random_room = random.choice(structures)
        x, y = random.choice(slices_to_xys(*(random_room.inner)))
        if city.tiles[(x, y)] in tile_types.EMPTY_TILES:
            entity_factory.troll.spawn(city, x, y)
            npcs_to_generate -= 1


def generate_items(city, structures):
    items_to_place = len(structures)
    while items_to_place:
        random_room = random.choice(structures)
        x, y = random.choice(slices_to_xys(*(random_room.inner)))
        if city.tiles[(x, y)] in tile_types.EMPTY_TILES:
            val = random.random()
            if val <= 0.2:
                entity_factory.lightning_scroll.spawn(city, x, y)
            if val <= 0.5:
                entity_factory.confusion_scroll.spawn(city, x, y)
            else:
                entity_factory.fireball_scroll.spawn(city, x, y)
            items_to_place -= 1
