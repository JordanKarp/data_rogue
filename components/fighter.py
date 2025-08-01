from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from render_order import RenderOrder
from input_handlers import GameOverEventHandler

import color

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    def heal(self, amount: int) -> int:
        amount_recovered = min(self.max_hp - self.hp, amount)
        self.hp += amount_recovered
        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount

    def die(self):
        if self.engine.player is self.parent:
            death_message = "You died!"
            self.engine.event_handler = GameOverEventHandler(self.engine)
            death_message_color = color.player_die

        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die

        # self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)
