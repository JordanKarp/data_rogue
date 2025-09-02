from __future__ import annotations

import copy
import math
from typing import Optional, Type, Tuple, TypeVar, TYPE_CHECKING, Union

from game.render.render_order import RenderOrder

if TYPE_CHECKING:
    from game.components.ai import BaseAI
    from game.world.game_map import GameMap
    from game.components.experience import Experience
    from game.components.equipment import Equipment
    from game.components.fighter import Fighter
    from game.components.inventory import Inventory
    from game.components.consumable import Consumable
    from game.components.equippable import Equippable
    from game.components.dialog import Dialog
    from game.components.information import Information


T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    parent: Union[GameMap, Inventory]

    def __init__(
        self,
        parent: Optional[GameMap] = None,
        x: int = 0,
        y: int = 0,
        level: int = 1,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.level = level
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order

        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    def spawn(self: T, gamemap: GameMap, level: int, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.level = level
        clone.parent = gamemap

        gamemap.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def place(
        self, x: int, y: int, level: int = 1, gamemap: Optional[GameMap] = None
    ) -> None:
        """Place this entity at a new location.  Handles moving across GameMaps."""
        self.x = x
        self.y = y
        self.level = level
        if gamemap:
            if hasattr(self, "parent") and self.parent is self.gamemap:
                self.gamemap.entities.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)

    def distance(self, x: int, y: int) -> float:
        """
        Return the distance between the current entity and the given (x, y) coordinate.
        """
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)


class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        level: int = 1,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai_cls: Type[BaseAI],
        equipment: Equipment,
        fighter: Fighter,
        inventory: Inventory,
        experience: Experience,
        dialog: Optional[Dialog] = None,
    ):
        super().__init__(
            x=x,
            y=y,
            level=level,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.equipment = equipment
        self.equipment.parent = self

        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self

        self.experience = experience
        self.experience.parent = self

        if dialog:
            self.dialog = dialog
            self.dialog.parent = self
            self.dialog.set_context({"name": self.name})

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)


class Item(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        level: int = 1,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        consumable: Optional[Consumable] = None,
        equippable: Optional[Equippable] = None,
        description: str = "",
    ):
        super().__init__(
            x=x,
            y=y,
            level=level,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )
        self.description = description

        self.consumable = consumable
        if self.consumable:
            self.consumable.parent = self

        self.equippable = equippable
        if self.equippable:
            self.equippable.parent = self


class Fixture(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        level: int = 1,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        information: Optional[Information] = None,
        description: str = "",
    ):
        super().__init__(
            x=x,
            y=y,
            level=level,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.FIXTURE,
        )
        self.description = description

        self.information = information
        if self.information:
            self.information.parent = self
