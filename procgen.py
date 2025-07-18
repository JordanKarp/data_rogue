from typing import List
from random import random, randint

# from entity import Entity
from engine import Engine

import entity_factory
from game_map import GameMap
from random import choice, sample, randint
import tile_types
from rectangular_room import RectangularRoom


# def generate_dungeon(map_width, map_height) -> GameMap:
#     dungeon = GameMap(map_width, map_height)

#     room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
#     room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

#     generate_walls(room_1, dungeon)
#     generate_walls(room_2, dungeon)

#     return dungeon


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    max_monsters_per_room: int,
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""

    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])
    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = randint(room_min_size, room_max_size)
        room_height = randint(room_min_size, room_max_size)

        x = randint(0, dungeon.width - room_width - 1)
        y = randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        generate_walls(new_room, dungeon)

        if len(rooms) == 0:
            # The first room, where the player starts.
            player.place(*new_room.center, dungeon)
        else:
            place_entities(new_room, dungeon, max_monsters_per_room)
        # else:  # All rooms after the first.
        #     # Dig out a tunnel between this room and the previous one.
        #     for x, y in tunnel_between(rooms[-1].center, new_room.center):
        #         dungeon.tiles[x, y] = tile_types.floor

        # Finally, append the new room to the list.
        rooms.append(new_room)

    return dungeon


def place_entities(room: RectangularRoom, dungeon: GameMap, maximum_monsters: int):
    number_of_monsters = randint(0, maximum_monsters)

    for i in range(number_of_monsters):
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random() < 0.8:
                entity_factory.orc.spawn(dungeon, x, y)
            else:
                entity_factory.troll.spawn(dungeon, x, y)


def generate_walls(room, dungeon):
    # Floors
    dungeon.tiles[room.inner] = tile_types.floor

    # Walls
    for wall in room.vertical_walls:
        dungeon.tiles[wall] = tile_types.vertical_wall
    for wall in room.horizontal_walls:
        dungeon.tiles[wall] = tile_types.horizontal_wall

    # Corners
    dungeon.tiles[room.top_left_corner] = tile_types.top_left_corner_wall
    dungeon.tiles[room.bottom_left_corner] = tile_types.bottom_left_corner_wall
    dungeon.tiles[room.top_right_corner] = tile_types.top_right_corner_wall
    dungeon.tiles[room.bottom_right_corner] = tile_types.bottom_right_corner_wall

    # Windows
    h_windows = sample(room.horizontal_walls, k=3)
    for window in h_windows:
        dungeon.tiles[window] = tile_types.horizontal_window
    v_windows = sample(room.vertical_walls, k=3)
    for window in v_windows:
        dungeon.tiles[window] = tile_types.vertical_window

    # Door
    door_tile = choice(room.walls)
    dungeon.tiles[door_tile] = tile_types.door
