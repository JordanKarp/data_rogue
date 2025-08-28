from __future__ import annotations

from typing import Callable, Tuple, Optional, TYPE_CHECKING, Union

import os
import tcod.event
from tcod import libtcodpy
import actions
import keys
from utility import change_text_color

import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Item


ActionOrHandler = Union[actions.Action, "BaseEventHandler"]
"""An event handler return value which can trigger an action or switch active handlers.

If a handler is returned then it will become the active handler for future events.
If an action is returned it will be attempted and if it's valid then
MainGameEventHandler will become the active handler.
"""


class BaseEventHandler(tcod.event.EventDispatch[ActionOrHandler]):
    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle an event and return the next active event handler."""
        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        assert not isinstance(
            state, actions.Action
        ), f"{self!r} can not handle actions."
        return self

    def on_render(self, console: tcod.Console) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[ActionOrHandler]:
        raise SystemExit()


class PopupMessage(BaseEventHandler):
    """Display a popup text window."""

    def __init__(self, parent_handler: BaseEventHandler, text: str):
        self.parent = parent_handler
        self.text = text

    def on_render(self, console: tcod.Console, fade: int = 8) -> None:
        """Render the parent and dim the result, then print the message on top."""
        self.parent.on_render(console)
        console.rgb["fg"] //= fade
        console.rgb["bg"] //= fade

        console.draw_frame(
            x=console.width // 4,
            y=console.height // 4,
            width=(console.width + 1) // 2,
            height=(console.height + 1) // 2,
            fg=color.white,
            bg=color.black,
            clear=True,
        )

        console.print_box(
            x=console.width // 4,
            y=console.height // 3,
            width=(console.width + 1) // 2,
            height=(console.height + 1) // 2,
            string=self.text,
            fg=color.white,
            bg=color.black,
            alignment=libtcodpy.CENTER,
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[BaseEventHandler]:
        """Any key returns to the parent handler."""
        return self.parent


class ItemPopupMessage(PopupMessage):
    def __init__(self, parent_handler: BaseEventHandler, engine, text: str):
        super().__init__(parent_handler, text)
        self.engine = engine

    def on_render(self, console, fade=2):
        return super().on_render(console, fade)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[BaseEventHandler]:
        """Any key returns to the parent handler."""
        # ! TODO fix inventory use/drop on display item
        # key = event.sym
        # if key == keys.KEY_MAPPING['DROP']
        #     return InventoryDropHandler(self.engine).on_item_selected()
        # elif key == keys.KEY_MAPPING['USE']:
        #     return InventoryActivateHandler(self.engine)
        return self.parent


class EventHandler(BaseEventHandler):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, event: tcod.event.Event) -> BaseEventHandler:
        """Handle events for input handlers with an engine."""
        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state
        # result = self.handle_action(action_or_state)
        if result := self.handle_action(action_or_state):
            # A valid action was performed.
            if isinstance(result, dict):
                if "information" in result:
                    return InformationHandler(self.engine, result["information"])
                elif "dialog" in result:
                    return DialogHandler(self.engine, result["dialog"])

            if not self.engine.player.is_alive:
                # The player was killed sometime during or after the action.
                return GameOverEventHandler(self.engine)
            elif self.engine.player.experience.requires_level_up:
                return LevelUpEventHandler(self.engine)
            return MainGameEventHandler(self.engine)  # Return to the main handler.
        return self

    def handle_action(self, action: Optional[actions.Action]) -> bool:
        """Handle actions returned from event methods.

        Returns True if the action will advance a turn.
        """
        if action is None:
            return False

        try:
            result = action.perform()

        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], color.impossible)
            return False  # Skip enemy turn on exceptions.

        self.engine.handle_enemy_turns()
        self.engine.update_gameclock()
        self.engine.update_fov()

        return result

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y

    def on_render(self, console: tcod.Console) -> None:
        self.engine.render(console)


class AskUserEventHandler(EventHandler):
    """Handles user input for actions which require special input."""

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        """By default any key exits this input handler."""
        return None if event.sym in keys.MODIFIER_KEYS else self.on_exit()

    def ev_mousebuttondown(
        self, event: tcod.event.MouseButtonDown
    ) -> Optional[actions.ActionOrHandler]:
        """By default any mouse click exits this input handler."""
        return self.on_exit()

    def on_exit(self) -> Optional[actions.ActionOrHandler]:
        """Called when the user is trying to exit or cancel an action.

        By default this returns to the main event handler.
        """
        return MainGameEventHandler(self.engine)


class DialogHandler(AskUserEventHandler):
    def __init__(self, engine, npc):
        super().__init__(engine)
        self.npc = npc

    def on_render(self, console):
        super().on_render(console)
        self.engine.change_hud(2)
        node_text = self.npc.dialog.get_current_text()
        console.print(self.engine.X_POS, self.engine.Y_POS + 1, node_text)

        for i, choice in enumerate(self.npc.dialog.get_choices()):
            console.print(
                self.engine.X_POS, self.engine.Y_POS + 2 + i, f"{i+1}. {choice['text']}"
            )

    def ev_keydown(self, event):
        if event.sym in (tcod.event.KeySym.ESCAPE, tcod.event.KeySym.q):
            self.engine.event_handler = MainGameEventHandler(self.engine)
            return

        index = event.sym - tcod.event.K_1
        choices = self.npc.dialog.get_choices()

        if 0 <= index < len(choices):
            action = self.npc.dialog.choose(index)
            if action == "open_shop":
                # TODO Shop
                print("OPEN SHOP HERE")
                # self.engine.event_handler = MerchantHandler(self.engine, self.npc)
            elif self.npc.dialog.current_node is None:
                self.engine.event_handler = MainGameEventHandler(self.engine)


class LevelUpEventHandler(AskUserEventHandler):
    TITLE = "Level Up"

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        x = 40 if self.engine.player.x <= 30 else 0
        console.draw_frame(
            x=x,
            y=0,
            width=35,
            height=8,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        console.print(x=x + 1, y=1, string="Congratulations! You level up!")
        console.print(x=x + 1, y=2, string="Select an attribute to increase.")

        console.print(
            x=x + 1,
            y=4,
            string=f"a) Constitution (+20 HP, from {self.engine.player.fighter.max_hp})",
        )
        console.print(
            x=x + 1,
            y=5,
            string=f"b) Strength (+1 attack, from {self.engine.player.fighter.power})",
        )
        console.print(
            x=x + 1,
            y=6,
            string=f"c) Agility (+1 defense, from {self.engine.player.fighter.defense})",
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        key = event.sym
        index = key - tcod.event.KeySym.a

        if 0 <= index <= 2:
            player = self.engine.player
            if index == 0:
                player.experience.increase_max_hp()
            elif index == 1:
                player.experience.increase_power()
            else:
                player.experience.increase_defense()
        else:
            self.engine.message_log.add_message("Invalid entry.", color.invalid)

            return None

        return super().ev_keydown(event)

    def ev_mousebuttondown(
        self, event: tcod.event.MouseButtonDown
    ) -> Optional[ActionOrHandler]:
        """
        Don't allow the player to click to exit the menu, like normal.
        """
        return None


class InventoryEventHandler(AskUserEventHandler):
    """This handler lets the user select an item.

    What happens then depends on the subclass.
    """

    TITLE = "<missing title>"

    def on_render(self, console: tcod.console.Console) -> None:
        """Render an inventory menu, which displays the items in the inventory, and the letter to select them.
        Will move to a different position based on where the player is located, so the player can always see where
        they are.
        """
        super().on_render(console)
        self.engine.change_hud(1)

        console.print(
            self.engine.X_POS,
            max(
                self.engine.Y_POS + 1,
                min(
                    self.engine.mouse_location[1],
                    len(self.engine.player.inventory.items) + 3,
                ),
            ),
            "→",
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        key = event.sym
        if key in keys.UP_DOWN_DIRECTIONS:
            return self.move_cursor(event, key)
        elif key in keys.CONFIRM_KEYS:
            return self.get_item_from_selected()
        # TODO FIX return inventory popup
        # wx, wy = self.engine.camera.screen_to_world(*self.engine.mouse_location)
        # return self.on_index_selected(wx, wy)

        return super().ev_keydown(event)

        # key = event.sym
        # index = key - tcod.event.KeySym.a

        # if 0 <= index <= 26:
        #     player = self.engine.player
        #     try:
        #         selected_item = player.inventory.items[index]
        #     except IndexError:
        #         self.engine.message_log.add_message("Invalid entry.", color.invalid)
        #         return None
        #     return self.on_item_selected(selected_item)
        # return super().ev_keydown(event)

    def move_cursor(self, event, key):
        y = self.engine.mouse_location[1]
        _, dy = keys.UP_DOWN_DIRECTIONS[key]
        y += dy

        # Clamp the cursor index to the map size.
        y = max(
            self.engine.Y_POS,
            min(y, self.engine.Y_POS + len(self.engine.player.inventory.items)),
        )
        self.engine.mouse_location = self.engine.mouse_location[0], y
        return None

    def ev_mousebuttondown(
        self, event: tcod.event.MouseButtonDown
    ) -> Optional[ActionOrHandler]:
        """By default any mouse click exits this input handler."""
        try:
            return self.get_item_from_selected()
        except IndexError:
            return self.on_exit()

    # TODO Rename this here and in `ev_keydown` and `ev_mousebuttondown`
    def get_item_from_selected(self):
        index = self.engine.mouse_location[1] - self.engine.Y_POS - 1
        item_dict = list(self.engine.player.inventory.items.values())[index]
        return self.on_item_selected(item_dict["object"])
        # return self.on_exit()

    def on_item_selected(self, item: Item) -> Optional[ActionOrHandler]:
        """Called when the user selects a valid item."""
        raise NotImplementedError()


class InventoryDisplayHandler(InventoryEventHandler):
    """Displaying an inventory item."""

    TITLE = "Item Information"

    def on_item_selected(self, item: Item) -> Optional[actions.ActionOrHandler]:
        """Display the selected item."""

        text = change_text_color(item.char, item.color)
        text += "\n" + "\n" + item.name + "\n" + "\n"

        text += item.description + "\n"
        text += f"Consumable: {bool(item.consumable)}" + "\n"
        text += f"Equippable: {bool(item.equippable)}" + "\n" + "\n" + "\n"
        return ItemPopupMessage(MainGameEventHandler(self.engine), self.engine, text)


class InventoryActivateHandler(InventoryEventHandler):
    """Handle using an inventory item."""

    TITLE = "Select an item to use"

    def on_item_selected(self, item: Item) -> Optional[actions.ActionOrHandler]:
        """Return the action for the selected item."""
        if item.consumable:
            # Return the action for the selected item.
            return item.consumable.get_action(self.engine.player)
        elif item.equippable:
            return actions.EquipAction(self.engine.player, item)
        else:
            return None


class InventoryDropHandler(InventoryEventHandler):
    """Handle dropping an inventory item."""

    TITLE = "Select an item to drop"

    def on_item_selected(self, item: Item) -> Optional[actions.ActionOrHandler]:
        """Drop this item."""
        return actions.DropItemAction(self.engine.player, item)


class SelectIndexHandler(AskUserEventHandler):
    """Handles asking the user for an index on the map."""

    def __init__(self, engine: Engine):
        """Sets the cursor to the player when this handler is constructed."""
        super().__init__(engine)
        # player = self.engine.player
        # engine.mouse_location = player.x, player.y

    def on_render(self, console: tcod.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)
        x, y = self.engine.mouse_location
        console.rgb["bg"][x, y] = color.white
        console.rgb["fg"][x, y] = color.black

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[actions.ActionOrHandler]:
        """Check for key movement or confirmation keys."""
        key = event.sym
        if key in keys.MOVE_DIRECTIONS:
            return self.move_cursor(event, key)
        elif key in keys.CONFIRM_KEYS:
            wx, wy = self.engine.camera.screen_to_world(*self.engine.mouse_location)
            return self.on_index_selected(wx, wy)
        return super().ev_keydown(event)

    def move_cursor(self, event, key):
        modifier = 1  # Holding modifier keys will speed up key movement.
        if event.mod & (tcod.event.Modifier.LSHIFT | tcod.event.Modifier.RSHIFT):
            modifier *= 5
        if event.mod & (tcod.event.Modifier.LCTRL | tcod.event.Modifier.RCTRL):
            modifier *= 10
        if event.mod & (tcod.event.Modifier.LALT | tcod.event.Modifier.RALT):
            modifier *= 20

        x, y = self.engine.mouse_location
        dx, dy = keys.MOVE_DIRECTIONS[key]
        x += dx * modifier
        y += dy * modifier
        # Clamp the cursor index to the map size.
        x = max(0, min(x, self.engine.game_map.width - 1))
        y = max(0, min(y, self.engine.game_map.height - 1))
        self.engine.mouse_location = x, y
        return None

    def ev_mousebuttondown(
        self, event: tcod.event.MouseButtonDown
    ) -> Optional[ActionOrHandler]:
        """Left click confirms a selection."""
        if self.engine.game_map.in_bounds(*event.tile) and event.button == 1:
            wx, wy = self.engine.camera.screen_to_world(*event.tile)
            return self.on_index_selected(wx, wy)
        return super().ev_mousebuttondown(event)

    def on_index_selected(self, x: int, y: int) -> Optional[actions.ActionOrHandler]:
        """Called when an index is selected."""
        raise NotImplementedError()


class InformationHandler(AskUserEventHandler):
    # TODO make handle multiple types of text
    def __init__(self, engine: Engine, information: str):
        super().__init__(engine)
        self.information = information
        self.cursor = 0
        self.spacing = 4

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)

        title_text = f"{self.information.parent.name} info"
        multi = len(self.information.pages) > 1
        if multi:
            title_text += f" - {self.information.idx+1}/{self.information.total_pages}"
        console.draw_frame(
            x=self.spacing,
            y=self.spacing,
            width=console.width - (self.spacing * 2),
            height=console.height - (self.spacing * 2),
            title=title_text,
            clear=True,
            bg=color.black,
            fg=color.white,
        )
        console.print_box(
            x=self.spacing + 1,
            y=self.spacing + 1,
            width=console.width - ((self.spacing + 1) * 2),
            height=console.height - (self.spacing * 2),
            string=self.information.text,
            bg=color.black,
        )

        exit_text = (
            "ESC to exit       ◄ and ► to cycle pages" if multi else "ESC to exit"
        )
        console.print(
            x=self.spacing + 1,
            y=console.height * 3 // 4 + 1,
            string=exit_text,
            bg=color.asphalt,
        )

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        # FIX infor cursor useless
        key = event.sym
        if key == keys.KEY_MAPPING["LEFT"]:
            self.information.increment_prev_page()
        elif key == keys.KEY_MAPPING["RIGHT"]:
            self.information.increment_next_page()
        elif key == tcod.event.KeySym.ESCAPE:
            return MainGameEventHandler(self.engine)


class LookHandler(SelectIndexHandler):
    """Lets the player look around using the keyboard."""

    def on_index_selected(self, x: int, y: int) -> None:
        """Return to main handler."""
        self.engine.event_handler = MainGameEventHandler(self.engine)


class SingleRangedAttackHandler(SelectIndexHandler):
    """Handles targeting a single enemy. Only the enemy selected will be affected."""

    def __init__(
        self,
        engine: Engine,
        callback: Callable[[Tuple[int, int]], Optional[actions.Action]],
    ):
        super().__init__(engine)

        self.callback = callback

    def on_index_selected(self, x: int, y: int) -> Optional[ActionOrHandler]:
        return self.callback((x, y))


class AreaRangedAttackHandler(SelectIndexHandler):
    """Handles targeting an area within a given radius. Any entity within the area will be affected."""

    def __init__(
        self,
        engine: Engine,
        radius: int,
        callback: Callable[[Tuple[int, int]], Optional[actions.Action]],
    ):
        super().__init__(engine)

        self.radius = radius
        self.callback = callback

    def on_render(self, console: tcod.Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)

        x, y = self.engine.mouse_location

        # Draw a rectangle around the targeted area, so the player can see the affected tiles.
        console.draw_frame(
            x=x - self.radius - 1,
            y=y - self.radius - 1,
            width=self.radius**2,
            height=self.radius**2,
            fg=color.red,
            clear=False,
        )

    def on_index_selected(self, x: int, y: int) -> Optional[ActionOrHandler]:
        return self.callback((x, y))


class MainGameEventHandler(EventHandler):

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[ActionOrHandler]:
        action: Optional[actions.Action] = None

        key = event.sym
        player = self.engine.player
        if key in keys.MOVE_DIRECTIONS:
            dx, dy = keys.MOVE_DIRECTIONS[key]
            action = actions.BumpAction(player, dx, dy)
        elif key in keys.CONFIRM_KEYS:
            action = actions.EnterAction(player)
        elif key == keys.KEY_MAPPING["WAIT"]:
            action = actions.WaitAction(player)
        elif key == keys.KEY_MAPPING["HISTORY"]:
            return HistoryViewer(self.engine)
        elif key == keys.KEY_MAPPING["PICKUP"]:
            action = actions.PickupAction(player)
        elif key == keys.KEY_MAPPING["USE"]:
            return InventoryActivateHandler(self.engine)
        elif key == keys.KEY_MAPPING["DROP"]:
            return InventoryDropHandler(self.engine)
        elif key == keys.KEY_MAPPING["DISPLAY"]:
            return InventoryDisplayHandler(self.engine)
        elif key == keys.KEY_MAPPING["LOOK"]:
            return LookHandler(self.engine)
        elif key == keys.KEY_MAPPING["LEAVE"]:
            action = actions.LeaveMapAction(player)
        elif key == keys.KEY_MAPPING["STAIRS"]:
            action = actions.TakeStairsAction(player)
        elif key == keys.KEY_MAPPING["NOTES"]:
            return self.engine.change_hud(3)
        elif key == keys.KEY_MAPPING["CYCLE_HUD"]:
            return self.engine.change_hud()

        elif key == tcod.event.KeySym.ESCAPE:
            raise SystemExit()

        # No valid key was pressed
        return action


class GameOverEventHandler(EventHandler):

    def on_quit(self) -> None:
        """Handle exiting out of a finished game."""
        if os.path.exists("savegame.sav"):
            os.remove("savegame.sav")  # Deletes the active save file.
        raise exceptions.QuitWithoutSaving()  # Avoid saving a finished game.

    def ev_quit(self, event: tcod.event.Quit) -> None:
        self.on_quit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.KeySym.ESCAPE:
            self.on_quit()


class HistoryViewer(EventHandler):
    """Print the history on a larger window which can be navigated."""

    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

    def on_render(self, console: tcod.Console) -> None:
        super().on_render(console)  # Draw the main state as the background.

        log_console = tcod.console.Console(console.width - 6, console.height - 6)

        # Draw a frame with a custom banner title.
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(
            0, 0, log_console.width, 1, "┤Message history├", alignment=libtcodpy.CENTER
        )

        # Render the message log using the cursor parameter.
        self.engine.message_log.render_messages(
            log_console,
            1,
            1,
            log_console.width - 2,
            log_console.height - 2,
            self.engine.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[MainGameEventHandler]:
        # Fancy conditional movement to make it feel right.
        if event.sym in keys.CURSOR_Y_KEYS:
            adjust = keys.CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor == 0:
                # Only move from the top to the bottom when you're on the edge.
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                # Same with bottom to top movement.
                self.cursor = 0
            else:
                # Otherwise move while staying clamped to the bounds of the history log.
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
        elif event.sym == keys.KEY_MAPPING["HOME"]:
            self.cursor = 0  # Move directly to the top message.
        elif event.sym == keys.KEY_MAPPING["END"]:
            self.cursor = self.log_length - 1  # Move directly to the last message.
        else:  # Any other key moves back to the main game state.
            return MainGameEventHandler(self.engine)
        return None
