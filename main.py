#!/usr/bin/env python3
import tcod
import copy
import traceback


# from actions import EscapeAction, MovementAction
from camera import Camera
from engine import Engine
import entity_factory
import color


# from procgen import generate_city
from city_gen import new_generate_city


def main() -> None:
    terminal_width = 80
    terminal_height = 50

    map_screen_width = 80
    map_screen_height = 43

    map_width = 300
    map_height = 260

    # MAX_ROOMS = 20
    # ROOM_MIN_SIZE = 3
    # ROOM_MAX_SIZE = 7
    # NUM_ROADS = 5
    # MAX_MONSTERS_PER_ROOM = 2
    # MAX_ITEMS_PER_ROOM = 2

    tileset = tcod.tileset.load_tilesheet(
        # "JK_Raving_1280x400.png", 16, 16, tcod.tileset.CHARMAP_CP437
        "JK_Fnord_16x16.png",
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )

    player = copy.deepcopy(entity_factory.player)
    camera = Camera(screen_width=map_screen_width, screen_height=map_screen_height)
    engine = Engine(player=player, camera=camera)

    # engine.game_map = generate_dungeon(
    #     max_rooms=MAX_ROOMS,
    #     room_min_size=ROOM_MIN_SIZE,
    #     room_max_size=ROOM_MAX_SIZE,
    #     max_monsters_per_room=MAX_MONSTERS_PER_ROOM,
    #     map_width=map_width,
    #     map_height=map_height,
    #     engine=engine,
    # )
    engine.game_map = new_generate_city(
        map_width=map_width,
        map_height=map_height,
        # map_width=map_screen_width,
        # map_height=map_screen_height,
        engine=engine,
    )
    engine.update_fov()
    # engine.update_camera(map_screen_width, map_screen_height)

    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )

    with tcod.context.new(
        columns=terminal_width,
        rows=terminal_height,
        tileset=tileset,
        title="Data Rogue",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(terminal_width, terminal_height, order="F")
        while True:
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)
            try:
                for event in tcod.event.wait():
                    context.convert_event(event)
                    engine.event_handler.handle_events(event)
                    engine.update_camera(map_width, map_height)
            except Exception:  # Handle exceptions in game.
                traceback.print_exc()  # Print error to stderr.
                # Then print the error to the message log.
                engine.message_log.add_message(traceback.format_exc(), color.error)


if __name__ == "__main__":
    main()
