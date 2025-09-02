from __future__ import annotations

import json
import random
from typing import Optional, TYPE_CHECKING

import game.render.color as color
from game.components.base_component import BaseComponent
from game.utils.utility import change_text_color

# if TYPE_CHECKING:
#     from entity import Actor


class Dialog(BaseComponent):
    def __init__(
        self, dialog_data: Optional[dict] = None, start_node="greeting", context=None
    ):
        self.message_log = []
        self.nodes = dialog_data or {}
        self.context = context or {}
        self.current_node = start_node
        self.active_text = ""
        self.active_choices = []
        self._prepare_node(self.current_node)

    def _prepare_node(self, node_name: str):
        """Pick a random NPC line and randomize choices for this node."""
        node = self.nodes[node_name]
        self.active_text = self._format(random.choice(node["text"]))
        self.active_choices = []
        self.add_to_log("NPC", self.active_text)
        for choice in node["choices"]:
            selected_text = self._format(random.choice(choice["text"]))
            self.active_choices.append(
                {
                    "text": selected_text,
                    "next": choice.get("next"),
                    "action": choice.get("action"),
                }
            )

    def get_current_text(self):
        return self.active_text

    def get_choices(self):
        return self.active_choices

    def choose(self, index):
        choice = self.active_choices[index]
        self.add_to_log("Player", choice.get("text"))
        if next_node := choice.get("next"):
            self.current_node = next_node
            self._prepare_node(next_node)
        else:
            self.current_node = "annoy"
            self.active_choices = []
        return choice.get("action")

    def add_to_log(self, sender, message):
        self.message_log.append((sender, message))

    def display_log(self):
        log = ""

        for sender, message in self.message_log:
            msg = f"{sender}: {message}\n"
            if sender == "Player":
                log += change_text_color(msg, color.dialog_player)
            else:
                log += change_text_color(msg, color.dialog_npc)
        return log
        # return "".join(
        #     f"{sender}: {message.ljust(10)}\n" for sender, message in self.message_log
        # )

    def set_context(self, context: dict):
        """Update or replace context dynamically (e.g., after quest updates)."""
        self.context.update(context)

    def _format(self, text: str) -> str:
        try:
            return text.format(**self.context)
        except KeyError:
            return text  # If a placeholder is missing, leave it as-is

    @classmethod
    def from_file(cls, dialog_file: str):
        with open(dialog_file, "r") as f:
            return cls(json.load(f))
