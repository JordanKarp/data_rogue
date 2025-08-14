from components import ai
from components import consumable

from components.fighter import Fighter
from entity import Actor, Item
from components.inventory import Inventory
from components.experience import Experience


player = Actor(
    char="σ",
    color=(127, 255, 127),
    name="Player",
    ai_cls=ai.HostileEnemy,
    fighter=Fighter(hp=30, defense=2, power=5),
    inventory=Inventory(capacity=26),
    experience=Experience(level_up_base=200),
)

orc = Actor(
    char="µ",
    color=(140, 234, 96),
    name="Orc",
    ai_cls=ai.HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3),
    inventory=Inventory(capacity=0),
    experience=Experience(xp_given=135),
)

npc = Actor(
    char="σ",
    color=(230, 230, 100),
    name="NPC",
    ai_cls=ai.WandererAI,
    fighter=Fighter(hp=30, defense=5, power=5),
    inventory=Inventory(capacity=5),
    experience=Experience(xp_given=0),
)
troll = Actor(
    char="↨",
    color=(0, 255, 0),
    name="Troll",
    ai_cls=ai.HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=4),
    inventory=Inventory(capacity=0),
    experience=Experience(xp_given=100),
)
health_potion = Item(
    char="*",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)

lightning_scroll = Item(
    char="α",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)
confusion_scroll = Item(
    char="α",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="α",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
