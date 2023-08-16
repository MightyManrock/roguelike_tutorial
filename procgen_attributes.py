import random
from typing import Dict, List, Tuple, TYPE_CHECKING
import entity_factories
from entity import Entity

max_monsters_by_floor = [
  (0, 5),
  (6, 4),
  (12, 3),
  (18, 2),
  (24, 3),
  (30, 4),
  (34, 5)
]

max_items_by_floor = [
  (0, 3),
  (12, 2),
  (18, 1),
  (24, 2),
  (34, 3)
]

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
  #Need more monsters for lower floors
  0: [(entity_factories.orc, 5), (entity_factories.troll, 5)],
  9: [(entity_factories.troll, 60)],
  11: [(entity_factories.orc, 80)],
  13: [(entity_factories.troll, 30)],
  15: [(entity_factories.troll, 15)],
  18: [(entity_factories.troll, 0)],
  21: [(entity_factories.troll, 15)],
  23: [(entity_factories.troll, 30)],
  25: [(entity_factories.troll, 60)],
  28: [(entity_factories.orc, 5)]
  #Need more monsters for higher floors
}

item_chances: Dict[int, List[Tuple[Entity, int]]] = {
  0: [(entity_factories.confusion_scroll, 10), (entity_factories.lightning_scroll, 25), (entity_factories.fireball_scroll, 25), (entity_factories.dagger, 0), (entity_factories.leather_armor, 0), (entity_factories.sword, 5), (entity_factories.chainmail, 5)],
  1: [(entity_factories.health_potion, 5)],
  3: [(entity_factories.health_potion, 10)],
  8: [(entity_factories.health_potion, 15), (entity_factories.sword, 10), (entity_factories.chainmail, 10)],
  12: [(entity_factories.fireball_scroll, 10), (entity_factories.dagger, 5), (entity_factories.leather_armor, 5)],
  14: [(entity_factories.health_potion, 35), (entity_factories.lightning_scroll, 10), (entity_factories.sword, 25), (entity_factories.chainmail, 25)],
  17: [(entity_factories.fireball_scroll, 0), (entity_factories.dagger, 10), (entity_factories.leather_armor, 10), (entity_factories.sword, 5), (entity_factories.chainmail, 5)],
  19: [(entity_factories.confusion_scroll, 0), (entity_factories.lightning_scroll, 0), (entity_factories.dagger, 25), (entity_factories.leather_armor, 25), (entity_factories.sword, 0), (entity_factories.chainmail, 0)],
  21: [(entity_factories.confusion_scroll, 10), (entity_factories.dagger, 10), (entity_factories.leather_armor, 10)],
  22: [(entity_factories.lightning_scroll, 10), (entity_factories.sword, 10), (entity_factories.chainmail, 10)],
  23: [(entity_factories.fireball_scroll, 10)],
  25: [(entity_factories.lightning_scroll, 25)],
  27: [(entity_factories.fireball_scroll, 25), (entity_factories.dagger, 5), (entity_factories.leather_armor, 5)],
  28: [(entity_factories.health_potion, 15), (entity_factories.sword, 25), (entity_factories.chainmail, 25)],
  32: [(entity_factories.health_potion, 10), (entity_factories.sword, 10), (entity_factories.chainmail, 10)],
  37: [(entity_factories.health_potion, 5), (entity_factories.dagger, 0), (entity_factories.leather_armor, 0), (entity_factories.sword, 5), (entity_factories.chainmail, 5)],
  39: [(entity_factories.health_potion, 0)]
}

def get_max_value_for_floor(
  max_value_by_floor: List[Tuple[int, int]], floor: int
) -> int:
  current_value = 0
  
  for floor_minimum, value in max_items_by_floor:
    if floor_minimum > floor:
      break
    else:
      current_value = value
  
  return current_value

def get_entities_at_random(
  weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
  number_of_entities: int,
  floor: int
) -> List[Entity]:
  entity_weighted_chances = {}
  
  for key, values in weighted_chances_by_floor.items():
    if key > floor:
      break
    else:
      for value in values:
        entity = value[0]
        weighted_chance = value[1]
        entity_weighted_chances[entity] = weighted_chance
    
  entities = list(entity_weighted_chances.keys())
  entity_weighted_chance_values = list(entity_weighted_chances.values())
  
  chosen_entities = random.choices(
    entities, weights=entity_weighted_chance_values, k=number_of_entities
  )

  return chosen_entities

def set_procgen_attributes():
  map_width = 80
  map_height = 43
  
  room_max_size = 16
  room_min_size = 4
  max_rooms = 30
  big_room_quotient = 6
  small_room_quotient = 8

  return map_width, map_height, room_max_size, room_min_size, max_rooms, big_room_quotient, small_room_quotient
  
#def randomize_procgen_attributes(current_floor):
#  map_width = random.randint(40, 80)
#  map_height = random.randint(26, 43)
#  
#  room_max_size = random.randint(8, 16)
#  room_min_size = random.randint(3, 6)
#  
#  if room_min_size >= room_max_size:
#    room_max_size = room_min_size
#    room_max_size += 2
#    room_min_size -= 1
#  
#  max_rooms = random.randint(5, 30)
#  big_room_quotient = random.randint(3, 9)
#  small_room_quotient = random.randint(2, 10)
#  
#  if big_room_quotient == small_room_quotient:
#    big_room_quotient -= 1
#    small_room_quotient += 1
#  
#  max_monsters_per_room = random.randint(1, int(2 + (abs(current_floor - 20) // 4)))
#  max_items_per_room = random.randint(1, int(1 + (abs(current_floor - 20) // 6)))
#  
#  return map_width, map_height, room_max_size, room_min_size, max_rooms, big_room_quotient, small_room_quotient, max_monsters_per_room, max_items_per_room