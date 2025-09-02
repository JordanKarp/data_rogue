import random
from typing import List, Tuple

import game.entities.tile_types as tile_types
from game.utils.utility import slices_to_xys


def place_entity(city, level, spot, entity, override=False):
    if city.tiles[level][spot] in tile_types.EMPTY_TILES or override:
        return entity.spawn(city, level, *spot)


def place_tile(city, level, spot, tile_list, override=True):
    # TODO improve to handle reseved tiles?
    tile = random.choice(tile_list)
    if city.tiles[level][spot] in tile_types.EMPTY_TILES or override:
        if city.tiles[level][spot] not in tile_types.RESERVED_TILES:
            city.tiles[level][spot] = tile


def place_tiles(city, level, spots, tile_list, override=True):
    locations = []
    if isinstance(spots, (List, list)):
        locations = spots
    elif isinstance(spots, Tuple):
        if isinstance(spots[0], slice) and isinstance(spots[1], slice):
            locations = slices_to_xys(*spots)
        else:
            locations = [spots]
    else:
        print(f"error placing tile from: {type(spots)}:")
        print(spots)

    for spot in locations:
        place_tile(city, level, spot, tile_list, override)
