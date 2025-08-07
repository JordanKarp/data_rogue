from engine import Engine
from game_map import GameMap

from city_gen import generate_city


class GameWorld:
    """
    Holds the settings for the GameMap, and generates new maps when moving down the stairs.
    """

    def __init__(
        self,
        *,
        engine: Engine,
    ):
        self.engine = engine
        self.map_index = -1
        self.maps = {}

    def generate_new_map(self, city_details=None) -> None:
        if city_details is None:
            city_details = {}
        self.map_index += 1

        self.engine.game_map = generate_city(
            engine=self.engine, city_details=city_details
        )
        self.maps[self.map_index] = self.engine.game_map

    def open_game_map(self, index):
        self.engine.game_map = self.map[index]
