from __future__ import annotations


import lzma
import pickle
from typing import TYPE_CHECKING
from tcod.console import Console
from tcod.map import compute_fov
from libtcodpy import FOV_SYMMETRIC_SHADOWCAST, FOV_BASIC

# from actions import EscapeAction, MovementAction
import color
from camera import Camera
from input_handlers import MainGameEventHandler
from game_clock import GameClock
from message_log import MessageLog
from render_functions import render_bar, render_names_at_mouse_location, render_hline
import exceptions

if TYPE_CHECKING:
    from entity import Actor
    from input_handlers import EventHandler
    from game_map import GameMap
    from game_world import GameWorld


X_POS = 25
Y_POS = 3

DISPLAYS = ["Character", "Inventory", "Dialog", "Notes", "History"]
DIALOG_INDEX = 2


class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor, camera: Camera):
        self.event_handler: EventHandler = MainGameEventHandler(self)
        self.player = player
        self.mouse_location = (0, 0)

        self.message_log = MessageLog()
        self.clock = GameClock()
        self.camera = camera
        self.active_hud_index = 0
        self.X_POS, self.Y_POS = X_POS, Y_POS

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        level = self.game_map.current_level

        self.game_map.visible[level][:] = compute_fov(
            transparency=self.game_map.tiles[level]["transparent"],
            pov=(self.player.x, self.player.y),
            radius=10,
            algorithm=FOV_BASIC,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def update_camera(self) -> None:
        self.camera.update(target_x=self.player.x, target_y=self.player.y)

    def update_gameclock(self) -> None:
        self.clock.increment()

    def change_hud(self, hud_index=None):
        if hud_index:
            self.active_hud_index = hud_index
            return
        self.active_hud_index = (self.active_hud_index + 1) % len(DISPLAYS)

    def render(self, console: Console) -> None:
        self.update_camera()
        self.game_map.render(console)

        # self.message_log.render(console=console, x=X_POS + 1, y=20, width=24, height=1)
        render_names_at_mouse_location(console, X_POS + 1, y=1, engine=self)

        render_hline(console, X_POS, Y_POS, 30)
        console.print(x=X_POS + 1, y=Y_POS, string=DISPLAYS[self.active_hud_index])

        if DISPLAYS[self.active_hud_index] == "Character":
            self.render_character_details(console)
        elif DISPLAYS[self.active_hud_index] == "Inventory":
            self.render_inventory(console)
        elif DISPLAYS[self.active_hud_index] == "Dialog":
            self.render_dialog(console)
        elif DISPLAYS[self.active_hud_index] == "Notes":
            self.render_notes(console)
        elif DISPLAYS[self.active_hud_index] == "History":
            self.message_log.render(
                console=console, x=X_POS, y=Y_POS + 1, width=25, height=20
            )
        else:
            print("render error")

    def render_character_details(self, console):
        console.print(
            x=X_POS,
            y=Y_POS + 1,
            string=f"X:{self.player.x} Y:{self.player.y}",
        )
        console.print(
            x=X_POS,
            y=Y_POS + 2,
            string=f"Level: {self.player.experience.current_level}",
        )
        console.print(
            x=X_POS,
            y=Y_POS + 3,
            string=f"XP: {self.player.experience.current_xp}",
        )
        console.print(
            x=X_POS,
            y=Y_POS + 4,
            string=f"XP for next Level: {self.player.experience.experience_to_next_level}",
        )

        console.print(
            x=X_POS,
            y=Y_POS + 5,
            string=f"Attack: {self.player.fighter.power}",
        )
        console.print(
            x=X_POS,
            y=Y_POS + 6,
            string=f"Defense: {self.player.fighter.defense}",
        )

    def render_inventory(self, console):
        if len(self.player.inventory.items) > 0:
            for i, (item_name, item_dict) in enumerate(
                self.player.inventory.items.items()
            ):

                item = item_dict["object"]
                count = item_dict["count"]
                item_string = f"{item_name.ljust(20)} x{count:02}"
                if self.player.equipment.item_is_equipped(item):
                    item_string = f"(E) {item_name.ljust(16)} x{count:02}"
                console.print(X_POS + 1, Y_POS + i + 1, item_string)
        else:
            console.print(X_POS + 1, Y_POS + 2, " (Empty) ")

        console.print(
            X_POS + 20,
            Y_POS,
            f"{(self.player.inventory.capacity - self.player.inventory.remaining):02}/{self.player.inventory.capacity}",
        )

    def render_dialog(self, console):
        pass

    def render_notes(self, console):
        pass

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
