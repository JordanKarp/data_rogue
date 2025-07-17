#!/usr/bin/env python3
import tcod

# from actions import EscapeAction, MovementAction
from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from game_map import GameMap
from procgen import generate_dungeon


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    tileset = tcod.tileset.load_tilesheet(
        "JK_Raving_1280x400.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )

    event_handler = EventHandler()

    player = Entity(int(screen_width / 2), int(screen_height / 2), "J", (255, 0, 0))

    game_map = generate_dungeon(
        max_rooms=12,
        room_min_size=4,
        room_max_size=15,
        map_width=map_width,
        map_height=map_height,
        player=player,
    )

    engine = Engine(event_handler=event_handler, game_map=game_map, player=player)

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
            events = tcod.event.wait()
            engine.handle_events(events)


if __name__ == "__main__":
    main()
