from __future__ import annotations

import random
from typing import Iterator, List, Tuple, Union, TYPE_CHECKING

import tcod
import math

import entity_factories
from game_map import GameMap
import tile_types

if TYPE_CHECKING:
  from engine import Engine

class Room:
  
  def intersects(self, other: Room) -> bool:
    return (
      self.x1 <= other.x2
      and self.x2 >= other.x1
      and self.y1 <= other.y2
      and self.y2 >= other.y1
    )

class RectangularRoom(Room):
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
  
  @property
  def expand_inner(self) -> List[Tuple[int, int]]:
    expanded_inner = []
    for x in range(self.x1 + 1, self.x2):
      for y in range(self.y1 + 1, self.y2):
        expanded_inner.append((x, y))
    return expanded_inner

#class CircularRoom(Room):
#  def __init__(self, x: int, y: int, diameter: int):
#    self.x1 = x
#    self.y1 = y
#    self.x2 = x + diameter
#    self.y2 = y + diameter
#  
#  @property
#  def center(self) -> Tuple[int, int]:
#    center_x = int((self.x1 + self.x2) / 2)
#    center_y = int((self.y1 + self.y2) / 2)
#    return center_x, center_y
#  
#  @property
#  def inner(self) -> List[Tuple[int, int]]:
#    inner_tiles = []
#    for x in range(self.x1 + 1, self.x2):
#      for y in range(self.y1 + 1, self.y2):
#        if (x, y) not in [(self.x1 + 1, self.y1 + 1), (self.x1 + 1, self.y2),
#          (self.x2, self.y1 + 1), (self.x2, self.y2)]:
#          inner_tiles.append((x, y))
#    return inner_tiles

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
  rooms: List[Room],
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
    number_of_monsters = random.randint(0, int(maximum_monsters / 2))
    number_of_items = random.randint(0, int(maximum_items / 2))
  else:
    number_of_monsters = random.randint(0, maximum_monsters)
    if random.random() >= 0.7:
      number_of_items = random.randint(0, maximum_items)
    else:
      number_of_items = random.randint(0, int(maximum_items / 2))
  return number_of_monsters, number_of_items

def place_entities(
  rooms: List[Room],
  room: Room,
  dungeon: GameMap,
  big_room_quotient: int,
  small_room_quotient: int,
  current_floor: int
) -> None:
  
  import procgen_attributes as proca
  
  if current_floor > 20:
    current_floor -= 1
  elif current_floor < 20:
    current_floor += 1
  
  maximum_monsters = proca.get_max_value_for_floor(proca.max_monsters_by_floor, current_floor)
  maximum_items = proca.get_max_value_for_floor(proca.max_items_by_floor, current_floor)
  
  number_of_monsters, number_of_items = randomize_entity_numbers(rooms, maximum_monsters, maximum_items, big_room_quotient, small_room_quotient)
  
  if number_of_monsters > 0:
    monsters: List[Entity] = proca.get_entities_at_random(
      proca.enemy_chances, number_of_monsters, current_floor
    )
  else: monsters = []

  if number_of_items > 0:
    items: List[Entity] = proca.get_entities_at_random(
      proca.item_chances, number_of_items, current_floor
    )
  else: items = []

  for entity in [x for x in (monsters + items) if x]:
    if isinstance(room, RectangularRoom):
      x = random.randint(room.x1 + 1, room.x2 - 1)
      y = random.randint(room.y1 + 1, room.y2 - 1)
    #elif isinstance(room, CircularRoom):
    #  available_tiles = room.inner
    #  x, y = random.choice(available_tiles)
    
    if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
      entity.spawn(dungeon, x, y)
      print(f"{entity.name} spawned!")

def place_hallway_entities(
  rooms: List[Room], dungeon: GameMap, current_floor: int
) -> None:
  
  import procgen_attributes as proca
  
  maximum_monsters = proca.get_max_value_for_floor(proca.max_monsters_by_floor, current_floor)
  maximum_items = proca.get_max_value_for_floor(proca.max_items_by_floor, current_floor)

  number_of_hallway_monsters = random.randint(int(len(rooms) / 4), int(len(rooms) / 2) + int(maximum_monsters / 2))
  number_of_hallway_items = random.randint(int(len(rooms) / 8), int(len(rooms) / 6) + int(maximum_monsters / 2))

  monsters: List[Entity] = proca.get_entities_at_random(
    proca.enemy_chances, number_of_hallway_monsters, current_floor
  )

  items: List[Entity] = proca.get_entities_at_random(
    proca.item_chances, number_of_hallway_items, current_floor
  )
  
  room_areas = []
  for room in rooms:
    if isinstance(room, RectangularRoom):
      room_areas.extend(room.expand_inner)
    elif isinstance(room, CircularRoom):
      room_areas.extend(room.inner)

  for entity in [x for x in (monsters + items) if x]:
    x = random.randint(2, dungeon.width - 2)
    y = random.randint(2, dungeon.height - 2)
    if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
      if (x, y) not in room_areas and dungeon.tiles[x, y] != tile_types.wall:
        entity.spawn(dungeon, x, y)
        print(f"{entity.name} spawned in hallway!")

def randomize_room_size(
  rooms: List[Room],
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
    engine: Engine,
    current_floor: int
) -> GameMap:
  player = engine.player
  dungeon = GameMap(engine, map_width, map_height, entities=[player])

  rooms: List[Room] = []

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

    x = random.randint(1, dungeon.width - room_width - 1)
    y = random.randint(1, dungeon.height - room_height - 1)
    
    #distance_from_floor_20 = abs(current_floor - 20)
    #decay_factor = 0.06
        #
    #if random.random() <= 0.76 + min(decay_factor * distance_from_floor_20, 0.23):
    new_room = RectangularRoom(x, y, room_width, room_height)
    #else:
    #  diameter = min(int((room_width + room_height) / 2), 6)
    #  new_room = CircularRoom(x, y, diameter)

    if any(new_room.intersects(other_room) for other_room in rooms):
      continue

    dungeon.tiles[new_room.inner] = tile_types.floor

    if len(rooms) == 0:
      player.place(*new_room.center, dungeon)
    else:
      for x, y in tunnel_between(rooms[-1].center, new_room.center):
        dungeon.tiles[x, y] = tile_types.floor
    
    place_entities(rooms, new_room, dungeon, big_room_quotient, small_room_quotient, current_floor)

    rooms.append(new_room)

  final_room = rooms[-1]
  
  if current_floor == 0:
    dungeon.upstairs_location = rooms[0].center
    dungeon.tiles[rooms[0].center] = tile_types.up_stairs
  elif 0 < current_floor < 20:
    dungeon.upstairs_location = rooms[0].center
    dungeon.tiles[rooms[0].center] = tile_types.up_stairs
    dungeon.downstairs_location = final_room.center
    dungeon.tiles[final_room.center] = tile_types.down_stairs
  elif current_floor == 40:
    dungeon.downstairs_location = rooms[0].center
    dungeon.tiles[rooms[0].center] = tile_types.down_stairs
  elif 40 > current_floor > 20:
    dungeon.downstairs_location = rooms[0].center
    dungeon.tiles[rooms[0].center] = tile_types.down_stairs
    dungeon.upstairs_location = final_room.center
    dungeon.tiles[final_room.center] = tile_types.up_stairs
  elif current_floor == 20:
    random_room_index = random.randint(1, len(rooms) - 1)
    random_upstairs_room = rooms[random_room_index]
    dungeon.tiles[random_upstairs_room.center] = tile_types.up_stairs
    dungeon.upstairs_location = random_upstairs_room.center
    dungeon.downstairs_location = final_room.center
    dungeon.tiles[final_room.center] = tile_types.down_stairs

  place_hallway_entities(rooms, dungeon, current_floor)
  return dungeon