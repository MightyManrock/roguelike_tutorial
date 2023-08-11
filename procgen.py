from __future__ import annotations

import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

import entity_factories
from game_map import GameMap
import tile_types

if TYPE_CHECKING:
  from engine import Engine

class RectangularRoom:
  def __init__(self, x: int, y: int, width: int, height: int):
    self.x1 = x
    self.y1 = y
    self.x2 = x + width
    self.y2 = y + height
    
  @property
  def center(self) -> Tuple[int, int]:
    center_x = int((self.x1 + self.x2) / 2)
    center_y = int((self.y1 + self.y2) / 2)
    
    return center_x, center_y
  
  @property
  def inner(self) -> Tuple[slice, slice]:
    return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

  def intersects(self, other: RectangularRoom) -> bool:
    return (
      self.x1 <= other.x2
      and self.x2 >= other.x1
      and self.y1 <= other.y2
      and self.y2 >= other.y1
    )

def tunnel_between(
  start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
  x1, y1 = start
  x2, y2 = end
  
  if random.random() < 0.5:
    corner_x, corner_y = x2, y1
    
  else:
    corner_x, corner_y = x1, y2
    
  for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
    yield x, y
  
  for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
    yield x, y

def randomize_entity_numbers(
  rooms: List[RectangularRoom],
  maximum_monsters: int,
  maximum_items: int,
  big_room_quotient: int,
  small_room_quotient: int,
) -> int:
  if len(rooms) == 0:
    number_of_monsters = 0
    number_of_items = random.randint(1, maximum_items)
  elif len(rooms) > 0 and len(rooms) % big_room_quotient == 0:
    if random.random() >= 0.2:
      number_of_monsters = random.randint(1, int(maximum_monsters * 1.5))
    else:
      number_of_monsters = random.randint(0, int(maximum_monsters * 2))
    number_of_items = random.randint(1, maximum_items)
  elif len(rooms) % small_room_quotient == 0:
    number_of_monsters = random.randint(0, int(maximum_monsters) / 2)
    number_of_items = random.randint(0, int(maximum_items / 2))
  else:
    number_of_monsters = random.randint(0, maximum_monsters)
    if random.random() >= 0.7:
      number_of_items = random.randint(0, maximum_items)
    else:
      number_of_items = random.randint(0, int(maximum_items / 2))
  return number_of_monsters, number_of_items

def place_entities(
  rooms: List[RectangularRoom],
  room: RectangularRoom,
  dungeon: GameMap,
  maximum_monsters: int,
  maximum_items: int,
  big_room_quotient: int,
  small_room_quotient: int
) -> None:
  number_of_monsters, number_of_items = randomize_entity_numbers(rooms, maximum_monsters, maximum_items, big_room_quotient, small_room_quotient)
  
  for i in range(number_of_monsters):
    x = random.randint(room.x1 + 1, room.x2 - 1)
    y = random.randint(room.y1 + 1, room.y2 - 1)
    
    if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
      if random.random() < 0.8:
        entity_factories.orc.spawn(dungeon, x, y)
      else:
        entity_factories.troll.spawn(dungeon, x, y)
  
  for i in range(number_of_items):
    x = random.randint(room.x1 + 1, room.x2 - 1)
    y = random.randint(room.y1 + 1, room.y2 - 1)
    if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
      item_chance = random.random()
      
      if item_chance < 0.6:
        entity_factories.health_potion.spawn(dungeon, x, y)
      elif item_chance < 0.7:
        entity_factories.fireball_scroll.spawn(dungeon, x, y)
      elif item_chance < 0.9:
        entity_factories.confusion_scroll.spawn(dungeon, x, y)
      else:
        entity_factories.lighting_scroll.spawn(dungeon, x, y)

def place_hallway_entities(
  rooms: List[RectangularRoom], dungeon: GameMap
) -> None:
  number_of_hallway_monsters = random.randint(int(len(rooms) / 4), int(len(rooms) / 2) + 1)
  number_of_hallway_items = random.randint(int(len(rooms) / 8), int(len(rooms) / 6) + 1)
  
  hallway_orcs = 0
  hallway_trolls = 0
  hallway_potions = 0
  hallway_scrolls = 0
  
  for i in range(number_of_hallway_monsters):
    x = random.randint(2, dungeon.width - 2)
    y = random.randint(2, dungeon.height - 2)
    
    if not any(entity.x == x and entity.y == y for entity in dungeon.entities) and [x, y] not in [range(any(room.x2 - room.x1 for room in rooms)), range(any(room.y2 - room.y1 for room in rooms))] and dungeon.tiles[x, y] != tile_types.wall:
      if random.random() < 0.8:
        entity_factories.orc.spawn(dungeon, x, y)
        hallway_orcs += 1
      else:
        entity_factories.troll.spawn(dungeon, x, y)
        hallway_trolls += 1

  for i in range(number_of_hallway_items):
    x = random.randint(2, dungeon.width - 2)
    y = random.randint(2, dungeon.height - 2)

    if not any(entity.x == x and entity.y == y for entity in dungeon.entities) and [x, y] not in [range(any(room.x2 - room.x1 for room in rooms)), range(any(room.y2 - room.y1 for room in rooms))] and dungeon.tiles[x, y] != tile_types.wall:
      item_chance = random.random()
      
      if item_chance < 0.6:
        entity_factories.health_potion.spawn(dungeon, x, y)
        hallway_potions += 1
      elif item_chance < 0.7:
        entity_factories.fireball_scroll.spawn(dungeon, x, y)
        hallway_scrolls += 1
      elif item_chance < 0.9:
        entity_factories.confusion_scroll.spawn(dungeon, x, y)
        hallway_scrolls += 1
      else:
        entity_factories.lighting_scroll.spawn(dungeon, x, y)
        hallway_scrolls += 1

  if hallway_orcs > 0:
    print(f"{hallway_orcs} orcs spawned in hallways!")
  if hallway_trolls > 0:
    print(f"{hallway_trolls} trolls spawned in hallways!")
  if hallway_potions > 0:
    print(f"{hallway_potions} potions spawned in hallways!")
  if hallway_scrolls > 0:
    print(f"{hallway_scrolls} scrolls spawned in hallways!")

def randomize_room_size(
  rooms: List[RectangularRoom],
  room_min_size: int,
  room_max_size: int,
  small_room_quotient: int,
  big_room_quotient: int
) -> int:
  if len(rooms) == 0 or len(rooms) % small_room_quotient == 0:
    room_width = random.randint(int(room_min_size * 0.75), int(room_max_size / 2))
    room_height = random.randint(int(room_min_size * 0.75), int(room_max_size / 2))
  elif len(rooms) > 0 and len(rooms) % big_room_quotient == 0:
    room_width = random.randint(int(room_min_size * 1.5), room_max_size)
    room_height = random.randint(int(room_min_size * 1.5), room_max_size)
  else:
    room_width = random.randint(room_min_size, int(room_max_size * 0.75))
    room_height = random.randint(room_min_size, int(room_max_size * 0.75))
  return room_width, room_height

def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    big_room_quotient: int,
    small_room_quotient: int,
    map_width: int,
    map_height: int,
    max_monsters_per_room: int,
    max_items_per_room: int,
    engine: Engine,
) -> GameMap:
  player = engine.player
  dungeon = GameMap(engine, map_width, map_height, entities=[player])

  rooms: List[RectangularRoom] = []

  for r in range(max_rooms):
    room_width, room_height = randomize_room_size(rooms, room_min_size, room_max_size, small_room_quotient, big_room_quotient)

    if len(rooms) == 0 or len(rooms) % small_room_quotient == 0:
      room_width = random.randint(int(room_min_size * 0.75), int(room_max_size / 2))
      room_height = random.randint(int(room_min_size * 0.75), int(room_max_size / 2))
    elif len(rooms) > 0 and len(rooms) % big_room_quotient == 0:
      room_width = random.randint(int(room_min_size * 1.5), room_max_size)
      room_height = random.randint(int(room_min_size * 1.5), room_max_size)
    else:
      room_width = random.randint(room_min_size, int(room_max_size * 0.75))
      room_height = random.randint(room_min_size, int(room_max_size * 0.75))

    x = random.randint(0, dungeon.width - room_width - 1)
    y = random.randint(0, dungeon.height - room_height - 1)

    new_room = RectangularRoom(x, y, room_width, room_height)

    if any(new_room.intersects(other_room) for other_room in rooms):
      continue

    dungeon.tiles[new_room.inner] = tile_types.floor

    if len(rooms) == 0:
      player.place(*new_room.center, dungeon)
    else:
      for x, y in tunnel_between(rooms[-1].center, new_room.center):
          dungeon.tiles[x, y] = tile_types.floor
    place_entities(rooms, new_room, dungeon, max_monsters_per_room, max_items_per_room, big_room_quotient, small_room_quotient)

    rooms.append(new_room)

  place_hallway_entities(rooms, dungeon)
  return dungeon