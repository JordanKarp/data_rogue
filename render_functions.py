from __future__ import annotations

from typing import TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap


def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    if (
        not game_map.in_bounds(x, y)
        or not game_map.visible[game_map.current_level][x, y]
    ):
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()


def get_tile_at_location(x: int, y: int, game_map: GameMap) -> str:
    if (
        not game_map.in_bounds(x, y)
        or not game_map.visible[game_map.current_level][x, y]
    ):
        return ""

    tile = game_map.tiles[game_map.current_level][x, y]
    return tile["name"].capitalize()


def render_hline(console, x, y, width, text="─"):
    console.print(x, y, string=text * width)


def render_bar(
    console: Console,
    current_value: int,
    maximum_value: int,
    total_width: int,
    x: int,
    y: int,
    display_text: str,
    bar_color,
):
    if not bar_color:
        bar_color = color.bar_filled
    bar_width = int(float(current_value) / maximum_value * total_width)
    console.draw_rect(x=x, y=y, width=total_width, height=1, ch=1, bg=color.bar_empty)
    if bar_width > 0:
        console.draw_rect(x=x, y=y, width=bar_width, height=1, ch=1, bg=bar_color)
    console.print(
        x=x + 1,
        y=y,
        string=f"{display_text}{current_value}/{maximum_value}",
        fg=color.bar_text,
    )


def render_names_at_mouse_location(
    console: Console, x: int, y: int, engine: Engine
) -> None:
    mouse_x, mouse_y = engine.mouse_location
    # print(mouse_x, mouse_y)
    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )
    if len(names_at_mouse_location) > 1:
        console.print(x=x, y=y, string=names_at_mouse_location)

    else:
        console.print(
            x=x, y=y, string=get_tile_at_location(mouse_x, mouse_y, engine.game_map)
        )
