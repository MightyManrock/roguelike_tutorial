from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

player = Actor(
  char="@",
  color=(255, 255, 255),
  name="Player",
  ai_cls=HostileEnemy,
  equipment=Equipment(),
  fighter=Fighter(hp=30, base_power=0, base_armor=0, min_dam=1, max_dam=3, damage_type="bludgeoning"),
  inventory=Inventory(capacity=26),
  level=Level(level_up_base=200)
)
kobold = Actor(
  char="k",
  color=(75, 127, 63),
  name="Kobold",
  ai_cls=HostileEnemy,
  equipment=Equipment(),
  fighter=Fighter(hp=6, base_power=0, base_armor=0, min_dam=1, max_dam=4, damage_type="piercing"),
  inventory=Inventory(capacity=0),
  level=Level(xp_given=20)
)
orc = Actor(
  char="o",
  color=(63, 127, 63),
  name="Orc",
  ai_cls=HostileEnemy,
  equipment=Equipment(),
  fighter=Fighter(hp=10, base_power=1, base_armor=1, min_dam=2, max_dam=5, damage_type="slashing"),
  inventory=Inventory(capacity=0),
  level=Level(xp_given=35)
)
troll = Actor(
  char="T",
  color=(0, 127, 0),
  name="Troll",
  ai_cls=HostileEnemy,
  equipment=Equipment(),
  fighter=Fighter(hp=16, base_power=3, base_armor=2, min_dam=2, max_dam=6, damage_type="bludgeoning", dam_vulnerable=["fire", "acid"]),
  inventory=Inventory(capacity=0),
  level=Level(xp_given=100)
)

confusion_scroll = Item(
  char="~",
  color=(207, 63, 255),
  name="Confusion Scroll",
  consumable=consumable.ConfusionConsumable(number_of_turns=10)
)
fireball_scroll = Item(
  char="~",
  color=(255, 0, 0),
  name="Fireball Scroll",
  consumable=consumable.FireballDamageConsumable(min_damage=8, max_damage=14, radius=3, damage_type="fire")
)
health_potion = Item(
  char="!",
  color=(127, 0, 255),
  name="Health Potion",
  consumable=consumable.HealingConsumable(min_heal=2, max_heal=6, damage_type="healing")
)
lightning_scroll = Item(
  char="~",
  color=(255, 255, 0),
  name="Lightning Scroll",
  consumable=consumable.LightningDamageConsumable(min_damage=12, max_damage=24, maximum_range=5, damage_type="electric")
)

club = Item(
  char="/",
  color=(139, 69, 19),
  name="Club",
  equippable=equippable.Club()
)
dagger = Item(
  char="/",
  color=(0, 191, 255),
  name="Dagger",
  equippable=equippable.Dagger()
)
sword = Item(
  char="/",
  color=(0, 191, 255),
  name="Sword",
  equippable=equippable.Sword()
)

padded_armor = Item(
  char="[",
  color=(159, 89, 39),
  name="Padded Armor",
  equippable=equippable.PaddedArmor(dam_resist= ["bludgeoning"])
)
leather_armor = Item(
  char="[",
  color=(139, 69, 19),
  name="Leather Armor",
  equippable=equippable.LeatherArmor()
)
chainmail = Item(
  char="[",
  color=(142, 191, 255),
  name="Chainmail",
  equippable=equippable.ChainMail(dam_resist = ["slashing"])
)