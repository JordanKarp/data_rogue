#!/usr/bin/env python3
import tcod
import copy
import traceback


# from actions import EscapeAction, MovementAction
from engine import Engine
from entity import Entity
import entity_factory
import color


# from input_handlers import EventHandler
from game_map import GameMap
from procgen import generate_city


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    MAX_ROOMS = 20
    ROOM_MIN_SIZE = 3
    ROOM_MAX_SIZE = 7
    NUM_ROADS = 5
    MAX_MONSTERS_PER_ROOM = 2
    MAX_ITEMS_PER_ROOM = 2

    tileset = tcod.tileset.load_tilesheet(
        "JK_Raving_1280x400.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

    player = copy.deepcopy(entity_factory.player)
    # player = Entity(int(screen_width / 2), int(screen_height / 2), "J", (255, 0, 0))
    engine = Engine(player=player)

    # engine.game_map = generate_dungeon(
    #     max_rooms=MAX_ROOMS,
    #     room_min_size=ROOM_MIN_SIZE,
    #     room_max_size=ROOM_MAX_SIZE,
    #     max_monsters_per_room=MAX_MONSTERS_PER_ROOM,
    #     map_width=map_width,
    #     map_height=map_height,
    #     engine=engine,
    # )
    engine.game_map = generate_city(
        max_buildings=MAX_ROOMS,
        building_min_size=ROOM_MIN_SIZE,
        building_max_size=ROOM_MAX_SIZE,
        num_roads=NUM_ROADS,
        max_monsters_per_room=MAX_MONSTERS_PER_ROOM,
        max_items_per_room=MAX_ITEMS_PER_ROOM,
        map_width=map_width,
        map_height=map_height,
        engine=engine,
    )
    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)
            try:
                for event in tcod.event.wait():
                    context.convert_event(event)
                    engine.event_handler.handle_events(event)
            except Exception:  # Handle exceptions in game.
                traceback.print_exc()  # Print error to stderr.
                # Then print the error to the message log.
                engine.message_log.add_message(traceback.format_exc(), color.error)


if __name__ == "__main__":
    main()
