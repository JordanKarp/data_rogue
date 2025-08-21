from __future__ import annotations

from typing import TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap


def get_entities_at_location(x: int, y: int, game_map: GameMap) -> str:
    if (
        not game_map.in_bounds(x, y)
        or not game_map.visible[game_map.current_level][x, y]
    ):
        return ""
    return [entity for entity in game_map.entities if entity.x == x and entity.y == y]


def entitys_to_name_list(entities):
    names = ", ".join(entity.name for entity in entities)
    return names.capitalize()


def get_tile_at_location(x: int, y: int, game_map: GameMap) -> str:
    if (
        not game_map.in_bounds(x, y)
        or not game_map.explored[game_map.current_level][x, y]
    ):
        return ""

    return game_map.tiles[game_map.current_level][x, y]


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
) -> None:  # sourcery skip: extract-method
    # ! FIX renders tiles under mouse when mouse is in non map section
    mouse_x, mouse_y = engine.mouse_location
    # print(mouse_x, mouse_y, engine.game_map.in_bounds(mouse_x, mouse_y))
    # print(mouse_x, mouse_y)
    world_x, world_y = engine.camera.screen_to_world(mouse_x, mouse_y)
    entities = get_entities_at_location(x=world_x, y=world_y, game_map=engine.game_map)
    tile = get_tile_at_location(world_x, world_y, engine.game_map)

    if len(entities) >= 1:
        console.print(x=x + 1, y=y, string=entitys_to_name_list(entities))
        console.print(
            x=x - 1,
            y=y,
            string=entities[0].char,
            fg=entities[0].color,
            bg=tuple(tile["light"][2]),
        )

    elif tile := get_tile_at_location(world_x, world_y, engine.game_map):
        name = tile["name"].capitalize()
        char = chr(tile["light"][0].item())
        fg_color = tuple(tile["light"][1])
        bg_color = tuple(tile["light"][2])
        console.print(x=x + 1, y=y, string=name)
        console.print(x=x - 1, y=y, string=char, fg=fg_color, bg=bg_color)
