#!/usr/bin/env python3
import tcod
import copy


# from actions import EscapeAction, MovementAction
from engine import Engine
from entity import Entity
import entity_factory

# from input_handlers import EventHandler
from game_map import GameMap
from procgen import generate_dungeon


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    MAX_ROOMS = 12
    ROOM_MIN_SIZE = 4
    ROOM_MAX_SIZE = 15
    MAX_MONSTERS_PER_ROOM = 2

    tileset = tcod.tileset.load_tilesheet(
        "JK_Raving_1280x400.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

    player = copy.deepcopy(entity_factory.player)
    # player = Entity(int(screen_width / 2), int(screen_height / 2), "J", (255, 0, 0))
    engine = Engine(player=player)

    engine.game_map = generate_dungeon(
        max_rooms=MAX_ROOMS,
        room_min_size=ROOM_MIN_SIZE,
        room_max_size=ROOM_MAX_SIZE,
        max_monsters_per_room=MAX_MONSTERS_PER_ROOM,
        map_width=map_width,
        map_height=map_height,
        engine=engine,
        # player=player,
    )
    engine.update_fov()

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)
            engine.event_handler.handle_events()


if __name__ == "__main__":
    main()
