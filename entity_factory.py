from components.ai import HostileEnemy
from components.consumable import (
    HealingConsumable,
    LightningDamageConsumable,
    ConfusionConsumable,
)
from components.fighter import Fighter
from entity import Actor, Item
from components.inventory import Inventory


player = Actor(
    char="J",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defense=2, power=5),
    inventory=Inventory(capacity=26),
)

orc = Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3),
    inventory=Inventory(capacity=0),
)
troll = Actor(
    char="↨",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=4),
    inventory=Inventory(capacity=0),
)
health_potion = Item(
    char="*",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=HealingConsumable(amount=4),
)

lightning_scroll = Item(
    char="α",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=LightningDamageConsumable(damage=20, maximum_range=5),
)
confusion_scroll = Item(
    char="α",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=ConfusionConsumable(number_of_turns=10),
)
