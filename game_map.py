from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING
import numpy as np  # type: ignore
from tcod.console import Console

import tile_types
from entity import Actor, Item


if TYPE_CHECKING:
    from entity import Entity
    from engine import Engine


class GameMap:
    def __init__(
        self,
        engine: Engine,
        width: int,
        height: int,
        levels: int,
        entities: Iterable[Entity] = (),
    ):

        self.engine = engine
        self.width, self.height = width, height
        self.max_levels = levels
        self.entities = set(entities)
        self.tiles = np.full(
            (self.max_levels, width, height), fill_value=tile_types.cement, order="F"
        )
        self.camera = self.engine.camera
        self.exit_locations = []
        self.stair_locations = {"UP": [], "DOWN": []}
        self.current_level = 1

        # Tiles the player can currently see
        self.visible = np.full(
            (self.max_levels, width, height), fill_value=False, order="F"
        )
        # Tiles the player has seen before
        self.explored = np.full(
            (self.max_levels, width, height), fill_value=False, order="F"
        )

    @property
    def gamemap(self) -> GameMap:
        return self

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    @property
    def items(self) -> Iterator[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    def get_blocking_entity_at_location(
        self, loc_x: int, loc_y: int
    ) -> Optional[Entity]:
        return next(
            (
                entity
                for entity in self.entities
                if entity.blocks_movement and entity.x == loc_x and entity.y == loc_y
            ),
            None,
        )

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        return next(
            (actor for actor in self.actors if actor.x == x and actor.y == y), None
        )

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """

        vx, vy = self.camera.viewport()
        floor = self.current_level

        # Current floor data
        visible_map = self.visible[floor]
        explored_map = self.explored[floor]
        tiles_map = self.tiles[floor]

        # Clamp viewport to map bounds
        map_x1, map_x2 = vx.start, min(vx.stop, self.width)
        map_y1, map_y2 = vy.start, min(vy.stop, self.height)

        # Actual visible size from map
        slice_w = map_x2 - map_x1
        slice_h = map_y2 - map_y1

        # Create a full SHROUD screen buffer
        render_output = np.full(
            (self.camera.screen_width, self.camera.screen_height),
            tile_types.SHROUD,
            dtype=tiles_map["light"].dtype,
        )

        # Visible area
        visible_render = np.select(
            condlist=[
                visible_map[map_x1:map_x2, map_y1:map_y2],
                explored_map[map_x1:map_x2, map_y1:map_y2],
            ],
            choicelist=[
                tiles_map[map_x1:map_x2, map_y1:map_y2]["light"],  # light
                tiles_map[map_x1:map_x2, map_y1:map_y2]["dark"],  # dark (placeholder)
            ],
            default=tile_types.SHROUD,
        )

        render_output[0:slice_w, 0:slice_h] = visible_render

        # Assign to console
        console.rgb[0 : self.camera.screen_width, 0 : self.camera.screen_height] = (
            render_output
        )

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        for sx, sy, ent in self.camera.entities_to_screen(
            entities_sorted_for_rendering
        ):
            if visible_map[ent.x, ent.y]:
                background_color = tuple(tiles_map[(ent.x, ent.y)]["light"][2])
                console.print(
                    x=sx,
                    y=sy,
                    string=ent.char,
                    fg=ent.color,
                    bg=background_color,
                )
        # vx, vy = self.camera.viewport()

        # # Clamp viewport to map bounds
        # map_x1, map_x2 = vx.start, min(vx.stop, self.width)
        # map_y1, map_y2 = vy.start, min(vy.stop, self.height)

        # # Actual visible size from map
        # slice_w = map_x2 - map_x1
        # slice_h = map_y2 - map_y1

        # # Create a full SHROUD screen buffer
        # render_output = np.full(
        #     (self.camera.screen_width, self.camera.screen_height),
        #     tile_types.SHROUD,
        #     dtype=self.tiles["light"].dtype,
        # )

        # # Fill only the valid map area
        # render_output[0:slice_w, 0:slice_h] = np.select(
        #     condlist=[
        #         self.visible[map_x1:map_x2, map_y1:map_y2],
        #         self.explored[map_x1:map_x2, map_y1:map_y2],
        #     ],
        #     choicelist=[
        #         self.tiles["light"][map_x1:map_x2, map_y1:map_y2],
        #         self.tiles["dark"][map_x1:map_x2, map_y1:map_y2],
        #     ],
        #     default=tile_types.SHROUD,
        # )

        # # Assign to console
        # console.rgb[0 : self.camera.screen_width, 0 : self.camera.screen_height] = (
        #     render_output
        # )

        # entities_sorted_for_rendering = sorted(
        #     self.entities, key=lambda x: x.render_order.value
        # )

        # for sx, sy, ent in self.camera.entities_to_screen(
        #     entities_sorted_for_rendering
        # ):
        #     if self.visible[ent.x, ent.y]:
        #         background_color = tuple(self.tiles[(ent.x, ent.y)]["light"][2])
        #         console.print(
        #             x=sx,
        #             y=sy,
        #             string=ent.char,
        #             fg=ent.color,
        #             bg=background_color,
        #         )
