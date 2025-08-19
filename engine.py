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
        # self.game_map.visible[:] = compute_fov(
        #     self.game_map.tiles["transparent"],
        #     (self.player.x, self.player.y),
        #     radius=10,
        #     algorithm=FOV_BASIC,
        # )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def update_camera(self) -> None:
        self.camera.update(target_x=self.player.x, target_y=self.player.y)

    def update_gameclock(self) -> None:
        self.clock.increment()

    def render(self, console: Console) -> None:
        self.update_camera()

        self.game_map.render(console)

        console.print(
            x=51,
            y=1,
            string=f"{self.clock.time.strftime('%b %d - %H:%M %p')}",
        )
        console.print(
            x=51, y=2, string=f"Level: {self.player.experience.current_level}"
        )
        console.print(
            x=51,
            y=3,
            string=f"X: {self.player.x:3d}     Y: {self.player.y:3d}",
        )

        render_hline(
            console=console,
            x=50,
            y=29,
            width=30,
            text="─",
        )

        self.message_log.render(console=console, x=51, y=30, width=28, height=20)

        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=28,
            x=51,
            y=4,
            display_text="HP: ",
            bar_color=color.red,
        )
        render_bar(
            console=console,
            current_value=self.player.experience.current_xp,
            maximum_value=self.player.experience.experience_to_next_level,
            total_width=28,
            x=51,
            y=5,
            display_text=" XP: ",
            bar_color=color.blue,
        )

        render_names_at_mouse_location(console=console, x=51, y=6, engine=self)

        render_hline(
            console=console,
            x=50,
            y=7,
            width=30,
            text="─",
        )

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
