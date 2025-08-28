from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from components.base_component import BaseComponent

# from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Fixture


class Information(BaseComponent):
    parent: Fixture

    def __init__(self, text=""):
        self.text = text

    def add_text(self, text):
        if self.text:
            text += " "
        self.text += text
