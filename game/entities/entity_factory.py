from game.components import ai
from game.components import consumable, equippable


from game.entities.entity import Actor, Item, Fixture
from game.components.equipment import Equipment
from game.components.fighter import Fighter
from game.components.inventory import Inventory
from game.components.experience import Experience
from game.components.dialog import Dialog
from game.components.information import Information

from game.data.dialog_data.dialog_data import DEFAULT_NPC_DIALOG

player = Actor(
    char="σ",
    color=(127, 255, 127),
    name="Player",
    ai_cls=ai.HostileEnemy,
    equipment=Equipment(),
    dialog=Dialog(DEFAULT_NPC_DIALOG),
    fighter=Fighter(hp=30, base_defense=2, base_power=5),
    inventory=Inventory(capacity=26),
    experience=Experience(level_up_base=200),
)

orc = Actor(
    char="µ",
    color=(140, 234, 96),
    name="Orc",
    ai_cls=ai.HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    experience=Experience(xp_given=135),
)

npc = Actor(
    char="σ",
    color=(230, 230, 100),
    name="NPC",
    ai_cls=ai.WandererAI,
    equipment=Equipment(),
    dialog=Dialog(DEFAULT_NPC_DIALOG),
    fighter=Fighter(hp=30, base_defense=5, base_power=5),
    inventory=Inventory(capacity=5),
    experience=Experience(xp_given=0),
)
troll = Actor(
    char="↨",
    color=(0, 255, 0),
    name="Troll",
    ai_cls=ai.HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    experience=Experience(xp_given=100),
)


# FIXTURES

computer = Fixture(
    char="Γ",
    color=(121, 246, 192),
    name="Computer",
    description="a DataCorp Laptop",
    information=Information(
        [
            "This is a computer. With two text pages.",
            "This is a really long sentence to be able to test the length of the read information event handler. This is a bit more to that last sentence, cause I dont think it's enough yet.This is a really long sentence to be able to test the length of the read information event handler. This is a bit more to that last sentence, cause I dont think it's enough yet.This is a really long sentence to be able to test the length of the read information event handler. This is a bit more to that last sentence, cause I dont think it's enough yet.",
        ]
    ),
)

sign = Fixture(
    char="ß",
    color=(150, 45, 0),
    name="Sign",
    description="a wooden sign",
    information=Information(["This is a sign."]),
)


# ITEMS

health_potion = Item(
    char="*",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
    description="Heals 4 points of HP",
)

lightning_scroll = Item(
    char="α",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
    description="Shoots lightning and does 20 damage /nto all within 5 tiles of the user",
)
confusion_scroll = Item(
    char="α",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
    description="Confuses another for 10 turns",
)
fireball_scroll = Item(
    char="α",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
    description="Shoots fire and does 12 damage to all within 3 tiles of selected spot",
)


dagger = Item(
    char="/",
    color=(0, 191, 255),
    name="Dagger",
    equippable=equippable.Dagger(),
    description="Provides a bonus to attack",
)

sword = Item(
    char="/",
    color=(0, 191, 255),
    name="Sword",
    equippable=equippable.Sword(),
    description="Provides a large bonus to attack ",
)

leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
    description="Provides a bonus to defense",
)

chain_mail = Item(
    char="[",
    color=(139, 69, 19),
    name="Chain Mail",
    equippable=equippable.ChainMail(),
    description="Provides a large bonus to defense",
)
