#!/usr/bin/env python3
import tcod
import traceback
from pathlib import Path


import color
import input_handlers
import exceptions
import setup_game


FONTS_FOLDER = Path("fonts")
SAVE_FOLDER = Path("save_data")


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(SAVE_FOLDER / filename)
        print("Game saved.")


def main() -> None:
    terminal_width = 80
    terminal_height = 50

    tileset = tcod.tileset.load_tilesheet(
        FONTS_FOLDER / "JK_Fnord_16x16.png",
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    with tcod.context.new(
        columns=terminal_width,
        rows=terminal_height,
        tileset=tileset,
        title="Data Rogue",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(terminal_width, terminal_height, order="F")

        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)

                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            save_game(handler, "savegame.sav")
            raise
        except BaseException:  # Save on any other unexpected exception.
            save_game(handler, "savegame.sav")
            raise


if __name__ == "__main__":
    main()
