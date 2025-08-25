from __future__ import annotations

from collections import Counter
from typing import Dict, List, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item


class Inventory(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Item] = []

    def drop(self, item: Item) -> None:
        """
        Removes an item from the inventory and restores it to the game map, at the player's current location.
        """
        self.items.remove(item)
        item.place(self.parent.x, self.parent.y, self.parent.level, self.gamemap)

        self.engine.message_log.add_message(f"You dropped the {item.name}.")

    @property
    def item_counts(self):
        item_counts = {}
        for item in self.items:
            if item.name in item_counts:
                item_counts[item.name] += 1
            else:
                item_counts[item.name] = 1
        return item_counts

    # def use(self, item: Item) -> None:
    #     if self.items[item] > 1:
    #         self.items[item] -= 1
    #     elif self.items[item] == 1:
    #         self.items.pop(item, None)

    # def drop(self, item: Item) -> None:
    #     """
    #     Removes an item from the inventory and restores it to the game map, at the player's current location.
    #     """
    #     if not self.items.get(item, None):
    #         return

    #     self.use(item)
    #     item.place(self.parent.x, self.parent.y, self.parent.level, self.gamemap)

    #     self.engine.message_log.add_message(f"You dropped a {item.name}.")

    # def add_item(self, item: Item) -> None:
    #     """
    #     Adds an item from the inventory.
    #     """

    #     if item.name not in [item.name for item in self.items]:
    #         self.items[item] = 1
    #     else:
    #         self.items[item] += 1

    #     print(self.items)
    #     self.engine.message_log.add_message(f"You picked a {item.name}.")
