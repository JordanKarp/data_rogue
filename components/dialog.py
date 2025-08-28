from __future__ import annotations

import json
from typing import Optional

# from components.base_component import BaseComponent

# if TYPE_CHECKING:
#     pass
# from entity import Actor


class Dialog:
    def __init__(self, dialog_file: Optional[str] = None):
        self.nodes = {}
        if dialog_file:
            self.nodes = Dialog.dict_from_file(dialog_file)
        self.current_node = "start"

    def get_current_text(self):
        return self.nodes[self.current_node]["text"]

    def get_choices(self):
        return self.nodes[self.current_node]["choices"]

    def choose(self, index):
        choice = self.get_choices()[index]
        self.current_node = choice.get("next")
        return choice.get("action")

    @staticmethod
    def dict_from_file(dialog_file):
        with open(dialog_file, "r") as f:
            return json.load(f)


# class DialogNode:
#     def __init__(self, text: str, options: list[dict]):
#         self.text = text
#         self.options = options  # Each option is {"text": str, "next": str|None}


# class Dialog(BaseComponent):
#     parent: Actor

#     def __init__(self, dialog_file: Optional[str] = None):
#         if dialog_file:
#             self.load_dialog(dialog_file)

#     def load_dialog(self, dialog_file):
#         self.nodes, self.current_node_id = Dialog.nodes_from_file(dialog_file)

#     def get_current_node(self) -> DialogNode:
#         return self.nodes[self.current_node_id]

#     def choose_option(self, index: int) -> bool:
#         node = self.get_current_node()
#         if 0 <= index < len(node.options):
#             next_id = node.options[index]["next"]
#             if next_id is None:
#                 return False  # Conversation ends
#             self.current_node_id = next_id
#             return True
#         return False

#     @staticmethod
#     def nodes_from_file(dialog_file):
#         with open(dialog_file, "r") as f:
#             data = json.load(f)

#             nodes = {
#                 node_id: DialogNode(node_data["text"], node_data.get("options", []))
#                 for node_id, node_data in data["nodes"].items()
#             }
#             return (nodes, data["start_node"])
