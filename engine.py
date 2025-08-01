from __future__ import annotations

from typing import TYPE_CHECKING
from tcod.console import Console
from tcod.map import compute_fov
from libtcodpy import FOV_SYMMETRIC_SHADOWCAST, FOV_BASIC

# from actions import EscapeAction, MovementAction
from camera import Camera
from input_handlers import MainGameEventHandler
from game_clock import GameClock
from message_log import MessageLog
from render_functions import render_bar, render_names_at_mouse_location
import exceptions

if TYPE_CHECKING:
    from entity import Actor
    from input_handlers import EventHandler
    from game_map import GameMap


class Engine:
    game_map: GameMap

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

        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=10,
            algorithm=FOV_BASIC,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible

    def update_camera(self, map_width, map_height) -> None:
        self.camera.update(
            target_x=self.player.x,
            target_y=self.player.y,
            map_width=map_width,
            map_height=map_height,
        )

    def update_gameclock(self) -> None:
        self.clock.increment()

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        console.print(
            x=1,
            y=46,
            string=f"{self.clock.time.strftime('%b %d - %H:%M %p')}",
        )

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_names_at_mouse_location(console=console, x=21, y=44, engine=self)
