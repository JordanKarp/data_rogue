from __future__ import annotations

import dialog_data.dialog_data as dialog_data
import color
import exceptions

import random
from typing import Optional, Tuple, TYPE_CHECKING


if TYPE_CHECKING:
    from input_handlers import DialogHandler

    from engine import Engine
    from entity import Actor, Entity, Item


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EnterAction(Action):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        ent_loc = self.entity.x, self.entity.y
        if ent_loc in self.engine.game_map.exit_locations:
            return LeaveMapAction(self.entity).perform()
        elif (
            self.engine.game_map.current_level,
            ent_loc,
        ) in self.engine.game_map.stair_locations["UP"] or (
            self.engine.game_map.current_level,
            ent_loc,
        ) in self.engine.game_map.stair_locations[
            "DOWN"
        ]:
            return TakeStairsAction(self.entity).perform()
        else:
            return PickupAction(self.entity).perform()


class LeaveMapAction(Action):
    def perform(self) -> None:
        """
        Leave the map, if any possible at the entity's location.
        """
        if (
            self.entity.x,
            self.entity.y,
        ) not in self.engine.game_map.exit_locations:
            raise exceptions.Impossible("There is no exit here.")
        self.engine.game_world.generate_new_map()
        self.engine.message_log.add_message("You leave this city.", color.white)


class TakeStairsAction(Action):
    def perform(self) -> None:
        """
        Take stairs up or down, if any possible at the entity's location.
        """
        if (
            self.engine.game_map.current_level,
            (self.entity.x, self.entity.y),
        ) in self.engine.game_map.stair_locations["UP"]:
            self.engine.game_map.current_level += 1
            self.entity.level += 1
        elif (
            self.engine.game_map.current_level,
            (self.entity.x, self.entity.y),
        ) in self.engine.game_map.stair_locations["DOWN"]:
            self.engine.game_map.current_level -= 1
            self.entity.level -= 1

        else:
            raise exceptions.Impossible("There are no stairs here.")

        if (
            self.engine.game_map.current_level < 0
            or self.engine.game_map.current_level > self.engine.game_map.max_levels
        ):
            self.engine.game_map.current_level = 1
            self.entity.level = 1
            raise exceptions.Impossible("You've gone out of bounds")


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        actor_location_level = self.entity.level
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if (
                actor_location_x == item.x
                and actor_location_y == item.y
                and actor_location_level == item.level
            ):
                if inventory.remaining >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")

                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.add_item(item)

                self.engine.message_log.add_message(f"You picked up the {item.name}!")
                return

        raise exceptions.Impossible("There is nothing here to pick up.")


class ItemAction(Action):
    def __init__(
        self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None
    ):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(
            *self.target_xy, self.entity.level
        )

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            self.item.consumable.activate(self)


class DropItemAction(ItemAction):
    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

        self.entity.inventory.drop(self.item)


class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)
        self.item = item

    def perform(self) -> None:
        self.entity.equipment.toggle_equip(self.item)


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy
        self.level = entity.level

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(
            *self.dest_xy, self.level
        )

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy, self.level)

    def perform(self) -> None:
        raise NotImplementedError()


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy
        floor = self.engine.game_map.current_level

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            if (
                self.entity.x,
                self.entity.y,
            ) not in self.engine.game_map.exit_locations:
                # Destination is out of bounds.
                raise exceptions.Impossible("That way is blocked.")
            return LeaveMapAction(self.entity).perform()
        if not self.engine.game_map.tiles[floor]["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y, floor):
            # Destination is blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")

        self.entity.move(self.dx, self.dy)


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor

        if not target:
            # No entity to attack.
            raise exceptions.Impossible("Nothing to attack.")

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"

        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} hit points.", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} but does no damage.", attack_color
            )


class SpeakAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor

        if not target:
            # No entity to attack.
            raise exceptions.Impossible("No one to speak to.")

        # self.engine.event_handler = DialogHandler(self.engine, target)
        # print(self.engine.event_handler)
        return DialogHandler(self.engine, target)

        # msg = random.choice(dialog_data.GREETINGS)
        # msg = f"{target.name}: {msg}"
        # self.engine.message_log.add_message(
        #     msg.format(player_name=self.entity.name), color.white
        # )


class ReadAction(ActionWithDirection):
    def perform(self) -> None:
        # target = self.target_actor

        # if not target:
        #     # No entity to attack.
        #     raise exceptions.Impossible("Nothing to speak to.")

        # msg = random.choice(dialog.GREETINGS)
        # msg = f"{target.name}: {msg}"
        self.engine.message_log.add_message("Reading goes here", color.white)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        # TODO
        if not self.target_actor:
            return MovementAction(self.entity, self.dx, self.dy).perform()
        if self.target_actor.name == "NPC":
            print("testBUMP")
            return
            # return SpeakAction(self.entity, self.dx, self.dy).perform()
        return MeleeAction(self.entity, self.dx, self.dy).perform()


class WaitAction(Action):
    def perform(self) -> None:
        pass
