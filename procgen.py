from typing import List
from random import random, randint, sample, choice

from engine import Engine

import entity_factory
from game_map import GameMap
import tile_types
from rectangular_structure import RectangularStructure
from rectangular_room import RectangularRoom
from road import Road

MAX_WINDOWS = 6
MAX_DOORS = 1

# def generate_dungeon(
#     max_rooms: int,
#     room_min_size: int,
#     room_max_size: int,
#     max_monsters_per_room: int,
#     map_width: int,
#     map_height: int,
#     engine: Engine,
# ) -> GameMap:
#     """Generate a new dungeon map."""

#     player = engine.player
#     dungeon = GameMap(engine, map_width, map_height, entities=[player])
#     rooms: List[RectangularStructure] = []

#     road = generate_road(5, False, dungeon)
#     rooms.append(road)
#     road = generate_road(15, True, dungeon)
#     rooms.append(road)
#     # dungeon.tiles[(15, 5)] = tile_types.road
#     # dungeon.tiles[(14, 5)] = tile_types.road
#     # dungeon.tiles[(16, 5)] = tile_types.road_divider_vert
#     # dungeon.tiles[(15, 4)] = tile_types.road_divider_vert
#     # dungeon.tiles[(15, 6)] = tile_types.road_divider_vert
#     dungeon.tiles[(13, 6)] = tile_types.stop_line_vert
#     dungeon.tiles[(16, 4)] = tile_types.stop_line_vert
#     dungeon.tiles[(14, 3)] = tile_types.stop_line_horiz
#     dungeon.tiles[(16, 6)] = tile_types.stop_line_horiz

#     for r in range(max_rooms):
#         room_width = randint(room_min_size, room_max_size)
#         room_height = randint(room_min_size, room_max_size)

#         x = randint(0, dungeon.width - room_width - 1)
#         y = randint(0, dungeon.height - room_height - 1)

#         # "RectangularRoom" class makes rectangles easier to work with
#         new_room = RectangularRoom(x, y, room_width, room_height)

#         # Run through the other rooms and see if they intersect with this one.
#         if any(new_room.intersects(other_room) for other_room in rooms):
#             continue  # This room intersects, so go to the next attempt.
#         # If there are no intersections then the room is valid.

#         # Dig out this rooms inner area.
#         generate_walls(new_room, dungeon)

#         if len(rooms) == 2:
#             # The first room, where the player starts.
#             player.place(*new_room.center, dungeon)
#         else:
#             place_entities(new_room, dungeon, max_monsters_per_room)

#         # Finally, append the new room to the list.
#         rooms.append(new_room)

#     return dungeon


def generate_city(
    max_buildings: int,
    building_min_size: int,
    building_max_size: int,
    num_roads: int,
    max_monsters_per_room: int,
    max_items_per_room: int,
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""

    player = engine.player
    city = GameMap(engine, map_width, map_height, entities=[player])
    structures: List[RectangularStructure] = []
    roads_left = num_roads
    road_orientation_percent = 0.5
    while roads_left > 0:
        is_vertical = random() < road_orientation_percent
        if is_vertical:
            road_orientation_percent -= 0.1
        else:
            road_orientation_percent += 0.1

        side = map_width if is_vertical else map_height
        pos = randint(int(side * 0.1), int(side * 0.9))
        road = generate_road(pos, is_vertical, city)

        for other_road in structures:
            if road.intersects(other_road):
                generate_intersection(road, other_road)

        structures.append(road)
        roads_left -= 1

    for r in range(max_buildings):
        room_width = randint(building_min_size, building_max_size)
        room_height = randint(building_min_size, building_max_size)

        x = randint(0, city.width - room_width - 1)
        y = randint(0, city.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in structures):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        generate_floor(new_room, city, tile_types.floor)

        # Dig out this rooms inner area.
        generate_outer_walls(new_room, city)

        if len(structures) == num_roads + 1:
            # The first room, where the player starts.
            player.place(*new_room.center, city)
        else:
            place_entities(new_room, city, max_monsters_per_room, max_items_per_room)

        # Finally, append the new room to the list.
        structures.append(new_room)

    city.tiles[(16, 5)] = tile_types.wall
    city.tiles[(16, 6)] = tile_types.wall
    city.tiles[(15, 5)] = tile_types.chair_horiz
    city.tiles[(15, 6)] = tile_types.chair_horiz
    city.tiles[(17, 5)] = tile_types.chair_horiz
    city.tiles[(17, 6)] = tile_types.chair_horiz

    return city


def place_entities(
    room: RectangularRoom,
    dungeon: GameMap,
    maximum_monsters: int,
    maximum_items: int,
):
    number_of_monsters = randint(0, maximum_monsters)
    number_of_items = randint(0, maximum_items)

    for i in range(number_of_monsters):
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random() < 0.8:
                entity_factory.orc.spawn(dungeon, x, y)
            else:
                entity_factory.troll.spawn(dungeon, x, y)

    for i in range(number_of_items):
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity_factory.health_potion.spawn(dungeon, x, y)


def generate_outer_walls(room, dungeon):

    # Walls
    for wall in room.vertical_edges:
        dungeon.tiles[wall] = tile_types.vertical_wall
    for wall in room.horizontal_edges:
        dungeon.tiles[wall] = tile_types.horizontal_wall

    # Corners
    dungeon.tiles[room.top_left_corner] = tile_types.top_left_corner_wall
    dungeon.tiles[room.bottom_left_corner] = tile_types.bottom_left_corner_wall
    dungeon.tiles[room.top_right_corner] = tile_types.top_right_corner_wall
    dungeon.tiles[room.bottom_right_corner] = tile_types.bottom_right_corner_wall

    generate_windows(room, dungeon, MAX_WINDOWS)
    generate_doors(room, dungeon, MAX_DOORS)


def generate_floor(room, game_map, floor_tile_type):
    game_map.tiles[room.inner] = floor_tile_type


def generate_doors(room, game_map, max_doors=MAX_DOORS):
    # Door
    door_tile = choice(room.edges)
    game_map.tiles[door_tile] = tile_types.door


def generate_windows(room, game_map, max_windows=MAX_WINDOWS):
    # Windows
    h_window_spots = sample(room.horizontal_edges, k=3)
    for window in h_window_spots:
        game_map.tiles[window] = tile_types.horizontal_window
    v_windows = sample(room.vertical_edges, k=3)
    for window in v_windows:
        game_map.tiles[window] = tile_types.vertical_window


def generate_road(pos, is_vert, dungeon):
    divider_tile = (
        tile_types.road_divider_vert if is_vert else tile_types.road_divider_horiz
    )
    length = dungeon.height if is_vert else dungeon.width
    road = Road(pos, length, is_vert)

    dungeon.tiles[road.center_line] = divider_tile
    dungeon.tiles[road.lanes] = tile_types.road

    # print(dungeon.tiles[road.lanes])

    return road


def generate_intersection(road, other_road):
    pass
