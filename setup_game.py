"""Handle the loading and initialization of game sessions."""

from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod
from tcod import libtcodpy


import color
from camera import Camera
from engine import Engine
import entity_factory
from game_world import GameWorld
import input_handlers


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""

    map_screen_width = 25
    map_screen_height = 25

    map_width = 100
    map_height = 100

    player = copy.deepcopy(entity_factory.player)
    camera = Camera(
        screen_width=map_screen_width,
        screen_height=map_screen_height,
        map_width=map_width,
        map_height=map_height,
    )
    engine = Engine(player=player, camera=camera)

    engine.game_world = GameWorld(engine=engine)
    engine.game_world.generate_new_map()
    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome to Data Rogue!", color.welcome_text
    )

    dagger = copy.deepcopy(entity_factory.dagger)
    leather_armor = copy.deepcopy(entity_factory.leather_armor)

    dagger.parent = player.inventory
    leather_armor.parent = player.inventory

    player.inventory.add_item(dagger, add_message=False)
    player.equipment.toggle_equip(dagger, add_message=False)

    player.inventory.add_item(leather_armor, add_message=False)
    player.equipment.toggle_equip(leather_armor, add_message=False)

    return engine


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine


class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        # console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "DATA_ROGUE",
            fg=color.menu_title,
            alignment=libtcodpy.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By Jordan Karp",
            fg=color.menu_title,
            alignment=libtcodpy.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=libtcodpy.CENTER,
                bg_blend=libtcodpy.BKGND_ALPHA(64),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.KeySym.q, tcod.event.KeySym.ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.KeySym.c:
            try:
                return input_handlers.MainGameEventHandler(
                    load_game("save_data/savegame.sav")
                )
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.KeySym.n:
            return input_handlers.MainGameEventHandler(new_game())

        return None
