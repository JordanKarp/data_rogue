from __future__ import annotations

from collections import OrderedDict
from typing import TYPE_CHECKING

from game.components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item


class Inventory(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.remaining = capacity
        # self.items: List[Item] = []
        self.items = OrderedDict()

    def remove_item(self, item: Item) -> None:
        if self.items[item.name]:
            if self.items[item.name].get("count", None) > 1:
                self.items[item.name]["count"] -= 1
            elif self.items[item.name].get("count", None) == 1:
                del self.items[item.name]
            self.remaining += 1
        else:
            print("No item to drop")

    def drop(self, item: Item, add_message: bool = True) -> None:
        """
        Removes an item from the inventory and restores it to the game map, at the player's current location.
        """
        self.remove_item(item)

        item.place(self.parent.x, self.parent.y, self.parent.level, self.gamemap)

        if add_message:
            self.engine.message_log.add_message(f"You dropped the {item.name}.")

    @property
    def item_counts(self):
        item_counts = OrderedDict()
        for item in self.items:
            if item.name in item_counts:
                item_counts[item.name] += 1
            else:
                item_counts[item.name] = 1
        return item_counts

    def add_item(self, item: Item, add_message: bool = True) -> None:
        """
        Adds an item from the inventory.
        """
        if self.remaining:
            if item.name not in self.items:
                self.items[item.name] = {"object": item, "count": 1}
            else:
                self.items[item.name]["count"] += 1
            self.remaining -= 1

            if add_message:
                self.engine.message_log.add_message(f"You picked a {item.name}.")
