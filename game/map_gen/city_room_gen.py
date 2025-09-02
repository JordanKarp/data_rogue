import random

from game.entities import tile_types
from game.entities import entity_factory
from game.map_gen.rectangular_room import RectangularRoom
from game.map_gen.city_gen_utility import place_tile, place_tiles, place_entity
from game.utils.utility import slices_to_xys


def generate_half_bathroom(city, level, structure):

    spot = random.choice(structure.along_inside_walls)
    place_tile(city, level, spot, [tile_types.bookcase_empty], False)

    spot_1 = random.choice(structure.inside_wall_opposite_door)
    spot_2 = random.choice(structure.inside_wall_opposite_door)
    place_tile(city, level, spot_1, [tile_types.sink], True)
    place_tile(city, level, spot_2, [tile_types.toilet], True)


def generate_office(city, level, structure):
    size = len(slices_to_xys(*structure.inner))
    bookshelf_spots = random.choices(structure.along_inside_walls, k=max(1, size // 3))
    x, y = structure.center
    place_tiles(city, level, bookshelf_spots, tile_types.BOOKCASE_TILES, False)
    place_tiles(city, level, [(x, y - 1)], [tile_types.chair_horiz], True)

    if computer_desk := place_entity(
        city, level, (x, y), entity_factory.computer, False
    ):
        computer_desk.information.add_page("Hello! I should be on page 3!")


def generate_conference_room(city, level, structure):
    size = len(slices_to_xys(*structure.inner))
    room = structure
    if structure.width >= 9 and structure.height >= 9:
        room = RectangularRoom(
            structure.x + 2,
            structure.y + 2,
            structure.width - 4,
            structure.height - 4,
        )
        bookshelf_spots = random.choices(
            structure.along_inside_walls, k=max(1, size // 3)
        )
        place_tiles(city, level, bookshelf_spots, tile_types.BOOKCASE_TILES, False)
    elif structure.width >= 7 and structure.height >= 7:
        room = RectangularRoom(
            structure.x + 1,
            structure.y + 1,
            structure.width - 2,
            structure.height - 2,
        )
    xs = [x for x, y in room.along_inside_walls]
    ys = [y for x, y in room.along_inside_walls]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    corners = {(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)}

    along_wo_corners = [spot for spot in room.along_inside_walls if spot not in corners]
    place_tiles(city, level, along_wo_corners, [tile_types.chair_horiz])
    place_tiles(city, level, room.inner_away_from_walls, [tile_types.table])


def generate_library(city, level, structure):
    inner = slices_to_xys(*structure.inner)
    ys = [y for x, y in inner]
    min_y, max_y = min(ys), max(ys)
    bookshelf_spots = [
        s for s in inner if s[0] % 2 == 0 and s[1] != min_y and s[1] != max_y
    ]
    place_tiles(city, level, bookshelf_spots, tile_types.BOOKCASE_TILES, False)


def generate_park(city, level, structure):
    num_trees = 5
    place_tiles(city, level, structure.area, tile_types.GRASS_TILES)
    spots = random.choices(slices_to_xys(*structure.area), k=num_trees)
    place_tiles(city, level, spots, tile_types.TREE_TILES)


ROOM_FUNCTIONS = {
    "Conference Room": generate_conference_room,
    "Library": generate_library,
    "Office": generate_office,
    "Half Bathroom": generate_half_bathroom,
    "Park": generate_park,
}
