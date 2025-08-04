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
        self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.cement, order="F")
        self.camera = self.engine.camera

        # Tiles the player can currently see
        self.visible = np.full((width, height), fill_value=False, order="F")
        # Tiles the player has seen before
        self.explored = np.full((width, height), fill_value=False, order="F")

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
        for entity in self.entities:
            if entity.blocks_movement and entity.x == loc_x and entity.y == loc_y:
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

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
        # console.rgb[0 : self.width, 0 : self.height] = np.select(
        #     condlist=[self.visible, self.explored],
        #     choicelist=[self.tiles["light"], self.tiles["dark"]],
        #     default=tile_types.SHROUD,
        # )
        vx, vy = self.camera.viewport()

        # Slice world arrays in (x, y) order
        visible_slice = self.visible[vx, vy]
        explored_slice = self.explored[vx, vy]
        light_tiles = self.tiles["light"][vx, vy]
        dark_tiles = self.tiles["dark"][vx, vy]

        console.rgb[0 : self.camera.screen_width, 0 : self.camera.screen_height] = (
            np.select(
                condlist=[visible_slice, explored_slice],
                choicelist=[light_tiles, dark_tiles],
                default=tile_types.SHROUD,
            )
        )

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        for sx, sy, ent in self.camera.entities_to_screen(
            entities_sorted_for_rendering
        ):
            if self.visible[ent.x, ent.y]:
                console.print(x=sx, y=sy, string=ent.char, fg=ent.color)

        # for entity in entities_sorted_for_rendering:
        #     # Only print entities that are in the FOV
        #     pos_x, pos_y = self.camera.world_to_screen(entity.x, entity.y)
        #     if self.visible[e, pos_y] or entity.char == "J":
        #         # if self.visible[entity.x, entity.y] or entity.char == "J":
        #         console.print(x=pos_x, y=pos_y, string=entity.char, fg=entity.color)
