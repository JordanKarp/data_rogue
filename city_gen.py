from typing import List, Tuple
import random

from game_map import GameMap
from rectangular_structure import RectangularStructure
from rectangular_road import RectangularRoad
from rectangular_room import RectangularRoom
import tile_types
import entity_factory
from utility import slices_to_xys

CITY_DEFAULTS = {
    "MAP_WIDTH": 80,
    "MAP_HEIGHT": 43,
    "MIN_BLOCK_SIZE": 10,
    "TREE_BORDER_WIDTH": 6,
    "ROAD_WIDTH": 3,
}


def generate_city(
    engine,
    map_width=CITY_DEFAULTS["MAP_WIDTH"],
    map_height=CITY_DEFAULTS["MAP_HEIGHT"],
    city_details=CITY_DEFAULTS,
):
    player = engine.player
    city = GameMap(engine, map_width, map_height, entities=[player])

    # generate_tree_border(city=city, border_width=CITY_DEFAULTS["TREE_BORDER_WIDTH"])
    border_width = CITY_DEFAULTS["TREE_BORDER_WIDTH"]
    generate_tree_border(city=city, border_width=border_width)
    blocks, road_spots = divide_cityspace(
        city, border_width, CITY_DEFAULTS["MIN_BLOCK_SIZE"]
    )
    road_spots = generate_city_out_road(city, road_spots, border_width)
    roads = generate_roads(city, road_spots)
    structures = generate_structures(city, blocks)
    for structure in structures:
        rooms, doors = split_and_place_doors(structure)
        for room in rooms:
            generate_walls(city, room)
        place_tiles(city, doors, [tile_types.door])
        # for door in doors:
        #     city.tiles[door] = tile_types.door
        generate_outer_doors(city, structure)
    generate_actors(city, player, structures, roads)
    player.place(20, 20, city)

    return city


def split_rectangle(rect: RectangularStructure, min_size=3, split_chance=0.6):
    """
    Split a rectangle into rooms of various sizes.
    Returns a list of RectangularStructure rooms.
    """
    rooms = []

    def _split(r: RectangularStructure):
        # Stop if too small
        if r.width <= min_size and r.height <= min_size:
            rooms.append(r)
            return

        # Randomly decide to split vertically or horizontally
        if random.random() < split_chance:
            # Vertical split (two side-by-side rooms)
            if r.width > min_size * 2 and (
                random.choice([True, False]) or r.height <= min_size * 2
            ):
                split_at = random.randint(min_size, r.width - min_size)
                left = RectangularStructure(r.x, r.y, split_at, r.height)
                right = RectangularStructure(
                    r.x + split_at, r.y, r.width - split_at, r.height
                )
                _split(left)
                _split(right)
                return

            # Horizontal split (two stacked rooms)
            if r.height > min_size * 2:
                split_at = random.randint(min_size, r.height - min_size)
                top = RectangularStructure(r.x, r.y, r.width, split_at)
                bottom = RectangularStructure(
                    r.x, r.y + split_at, r.width, r.height - split_at
                )
                _split(top)
                _split(bottom)
                return

        # No split — keep as is
        rooms.append(r)

    _split(rect)
    return rooms


def split_and_place_doors(rect: RectangularStructure, min_size=4):
    """Split the rectangle into rooms and place doors during each split."""
    rooms = []
    doors = []

    def _split(r: RectangularStructure):
        # Stop if too small
        if r.width <= min_size and r.height <= min_size:
            rooms.append(r)
            return

        # Decide split direction
        if r.width > r.height and r.width >= min_size * 2:
            # Vertical split
            split_at = random.randint(min_size, r.width - min_size)
            left = RectangularStructure(r.x, r.y, split_at, r.height)
            right = RectangularStructure(
                r.x + split_at, r.y, r.width - split_at, r.height
            )

            # Place door in the shared wall
            door_y = random.randint(r.y + 1, r.y + r.height - 2)
            door_x = r.x + split_at
            doors.append((door_x, door_y))

            _split(left)
            _split(right)

        elif r.height >= min_size * 2:
            # Horizontal split
            split_at = random.randint(min_size, r.height - min_size)
            top = RectangularStructure(r.x, r.y, r.width, split_at)
            bottom = RectangularStructure(
                r.x, r.y + split_at, r.width, r.height - split_at
            )

            # Place door in the shared wall
            door_x = random.randint(r.x + 1, r.x + r.width - 2)
            door_y = r.y + split_at
            doors.append((door_x, door_y))

            _split(top)
            _split(bottom)

        else:
            # No further split
            rooms.append(r)

    _split(rect)
    return rooms, doors


def generate_tree_border(city, border_width):
    rows = city.height
    cols = city.width
    for t in range(border_width):
        # Top and bottom row border
        for x in range(cols):
            place_tile(city, (x, t), tile_types.TREE_TILES)
            place_tile(city, (x, rows - 1 - t), tile_types.TREE_TILES)

        # Left and right column border
        for y in range(rows - t):
            place_tile(city, (t, y), tile_types.TREE_TILES)
            place_tile(city, (cols - 1 - t, y), tile_types.TREE_TILES)


def divide_cityspace(city, border_width, min_block_size):
    x = border_width
    y = border_width
    width = city.width - (2 * border_width)
    height = city.height - (2 * border_width)

    roads = []
    blocks = []

    queue = [RectangularStructure(x, y, width, height)]

    while queue:
        block = queue.pop(0)
        w, h = block.w, block.h

        # Check if we can split further
        if (
            w < min_block_size * 2 + CITY_DEFAULTS["ROAD_WIDTH"]
            and h < min_block_size * 2 + CITY_DEFAULTS["ROAD_WIDTH"]
        ):
            blocks.append(RectangularStructure(block.x + 1, block.y + 1, w - 3, h - 3))
            continue

        # Decide split direction
        split_horizontally = random.choice([True, False])
        if w < min_block_size * 2 + CITY_DEFAULTS["ROAD_WIDTH"]:
            split_horizontally = True
        elif h < min_block_size * 2 + CITY_DEFAULTS["ROAD_WIDTH"]:
            split_horizontally = False

        if split_horizontally:
            # Horizontal split
            split_line = random.randint(
                min_block_size, h - min_block_size - CITY_DEFAULTS["ROAD_WIDTH"]
            )
            roads.append(
                RectangularStructure(
                    block.x, block.y + split_line, w, CITY_DEFAULTS["ROAD_WIDTH"]
                )
            )

            # Top block
            queue.append(RectangularStructure(block.x, block.y, w, split_line))
            # Bottom block
            queue.append(
                RectangularStructure(
                    block.x,
                    block.y + split_line + CITY_DEFAULTS["ROAD_WIDTH"],
                    w,
                    h - split_line - CITY_DEFAULTS["ROAD_WIDTH"],
                )
            )
        else:
            # Vertical split
            split_line = random.randint(
                min_block_size, w - min_block_size - CITY_DEFAULTS["ROAD_WIDTH"]
            )
            roads.append(
                RectangularStructure(
                    block.x + split_line, block.y, CITY_DEFAULTS["ROAD_WIDTH"], h
                )
            )

            # Left block
            queue.append(RectangularStructure(block.x, block.y, split_line, h))
            # Right block
            queue.append(
                RectangularStructure(
                    block.x + split_line + CITY_DEFAULTS["ROAD_WIDTH"],
                    block.y,
                    w - split_line - CITY_DEFAULTS["ROAD_WIDTH"],
                    h,
                )
            )

    # Remaining blocks go to final list
    blocks.extend(
        RectangularStructure(block.x + 1, block.y + 1, block.w - 3, block.h - 3)
        for block in queue
    )
    return [b.as_tuple for b in blocks], [r.as_tuple for r in roads]


def generate_roads(city, road_dimensions):
    # Determine road sizes and number
    roads = []

    for x, y, w, h in road_dimensions:
        is_vertical = w < h
        road = RectangularRoad(x, y, w, h, is_vertical)
        divider_tile = (
            tile_types.road_divider_vert
            if is_vertical
            else tile_types.road_divider_horiz
        )

        place_tiles(city, road.center_line, [divider_tile])
        place_tiles(city, road.lanes, [tile_types.road])
        # city.tiles[road.center_line] = divider_tile
        # city.tiles[road.lanes] = tile_types.road

        for other_road in roads:
            if road.abuts(other_road):
                for idx, spot in enumerate(road.abuts(other_road)):
                    if idx <= 2:
                        place_tile(city, spot, [tile_types.road])
                        # city.tiles[spot] = tile_types.chair_horiz
        roads.append(road)
    return roads


def generate_city_out_road(city, roads, border_width):
    w = city.width - (2 * border_width)
    h = city.height - (2 * border_width)

    random.shuffle(roads)
    for road in roads:
        if road[0] == border_width:
            road[0] = 0
            road[2] += border_width
            city.exit_locations = [(0, road[1]), (0, road[1] + 1), (0, road[1] + 2)]
            return roads
        elif road[1] == border_width:
            road[1] = 0
            road[3] += border_width
            city.exit_locations = [(road[0], 0), (road[0] + 1, 0), (road[0] + 2, 0)]
            return roads
        elif road[0] + road[2] + border_width == w:
            road[2] += border_width
            city.exit_locations = [
                (road[0] + road[2], road[1]),
                (road[0] + road[2], road[1] + 1),
                (road[0] + road[2], road[1] + 2),
            ]

            return roads
        elif road[1] + road[3] + border_width == h:
            road[3] += border_width
            city.exit_locations = [
                (road[0], road[1] + road[3]),
                (road[0] + 1, road[1] + road[3]),
                (road[0] + 2, road[1] + road[3]),
            ]

            return roads


def rect_touch_or_overlap(rects: List[Tuple[int, int, int, int]]):
    """Return (x, y, w, h) intersections or touching edges between rects."""
    results = []
    for i, (x1, y1, w1, h1) in enumerate(rects):
        for x2, y2, w2, h2 in rects[i + 1 :]:
            ix, iy = max(x1, x2), max(y1, y2)
            iw, ih = min(x1 + w1, x2 + w2) - ix, min(y1 + h1, y2 + h2) - iy
            if iw >= 0 and ih >= 0:  # allow touching (== 0) or overlapping (> 0)
                results.append((ix, iy, iw, ih))
    return results


def generate_structures(city, block_dimensions):
    # Determine lot sizes and type
    structures = []

    for x, y, w, h in block_dimensions:
        # determine size
        structure = RectangularRoom(x, y, w, h)

        if any(structure.intersects(other_structure) for other_structure in structures):
            continue

        generate_flooring(city, structure, tile_types.floor)
        generate_walls(city, structure)

        # rooms = subdivide_structure(structure)
        # for room in rooms:
        #     generate_walls(city, room)
        #     generate_outer_doors(city, room)

        generate_windows(city, structure)
        generate_outer_doors(city, structure)

        # TODO FIX
        chair_spot = random.choices(structure.along_inside_walls, k=12)
        for spot in chair_spot:
            if city.tiles[spot] in tile_types.EMPTY_TILES:
                tile = random.choice(tile_types.BOOKCASE_TILES)
                city.tiles[spot] = tile

        structures.append(structure)

    return structures


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
    generate_npcs(city, structures, roads)
    generate_items(city, structures)
    generate_player(city, player, structures)


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
            entity_factory.orc.spawn(city, x, y)
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


def place_tile(city, spot, tile_list, override=True):
    tile = random.choice(tile_list)
    if city.tiles[spot] in tile_types.EMPTY_TILES or override:
        city.tiles[spot] = tile


def place_tiles(city, spots, tile_list, override=True):
    locations = []
    if isinstance(spots, (List, list)):
        locations = spots
    elif isinstance(spots, Tuple):
        locations = slices_to_xys(*spots)
    else:
        print(f"error placing tile from: {type(spots)}:")
        print(spots)

    for spot in locations:
        place_tile(city, spot, tile_list, override)
