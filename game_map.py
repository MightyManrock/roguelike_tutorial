from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np
from tcod.console import Console

from entity import Actor, Item
import tile_types

if TYPE_CHECKING:
  from engine import Engine
  from entity import Entity

class GameMap:
  def __init__(
    self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
  ):
    self.engine = engine
    self.width, self.height = width, height
    self.entities = set(entities)
    self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
    
    self.visible = np.full(
      (width, height), fill_value=False, order="F"
    )
    self.explored = np.full(
      (width, height), fill_value=False, order="F"
    )
    
    self.downstairs_location = (0, 0)
    self.upstairs_location = (0, 0)
  
  @property
  def game_map(self) -> GameMap:
    return self
  
  @property
  def actors(self) -> Iterator[Actor]:
    yield from (
      entity
      for entity in self.entities
      if isinstance(entity, Actor) and entity.is_alive
    )
  
  @property
  def items(self) -> Iterator[Item]:
    yield from (entity for entity in self.entities if isinstance(entity, Item))
  
  def get_blocking_entity_at_location(
    self, location_x: int, location_y: int
  ) -> Optional[Entity]:
    for entity in self.entities:
      if (
        entity.blocks_movement
        and entity.x == location_x
        and entity.y == location_y
      ):
        return entity
    
    return None
  
  def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
    for actor in self.actors:
      if actor.x == x and actor.y == y:
        return actor
    return None
  
  def in_bounds(self, x:int, y:int) -> bool:
    return 0 <= x < self.width and 0 <= y < self.height
  
  def render(self, console: Console) -> None:
    console.rgb[0 : self.width, 0 : self.height] = np.select(
      condlist=[self.visible, self.explored],
      choicelist=[self.tiles["light"], self.tiles["dark"]],
      default=tile_types.SHROUD
    )
    
    entities_sorted_for_rendering = sorted(
      self.entities, key=lambda x: x.render_order.value
    )
    
    for entity in entities_sorted_for_rendering:
      if self.visible[entity.x, entity.y]:
        console.print(
          entity.x, entity.y, string=entity.char, fg=entity.color
        )
        
class GameWorld:
  def __init__(
    self,
    *,
    engine: Engine,
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    big_room_quotient: int,
    small_room_quotient: int,
    map_width: int,
    map_height: int,
    current_floor: int = 0
  ):
    self.engine = engine
    
    self.max_rooms = max_rooms
    
    self.map_width = map_width
    self.map_height = map_height
    
    self.big_room_quotient = big_room_quotient
    self.small_room_quotient = small_room_quotient
    
    self.room_min_size = room_min_size
    self.room_max_size = room_max_size
    
    self.current_floor = current_floor + 20
    
    self.saved_floors = []
    self.saved_floors.extend([""] * 40)
  
  def generate_floor(self, floor_change: int = 0) -> None:
    from procgen import generate_dungeon
    #from procgen_attributes import randomize_procgen_attributes
        #
    #if self.current_floor != 20:
    #  self.map_width, self.map_height, self.room_max_size, self.room_min_size, self.max_rooms, self.big_room_quotient, self.small_room_quotient, self.max_monsters_per_room, self.max_items_per_room = randomize_procgen_attributes(self.current_floor)
    
    self.current_floor += floor_change

    self.engine.game_map = generate_dungeon(
      max_rooms=self.max_rooms,
      room_min_size=self.room_min_size,
      room_max_size=self.room_max_size,
      big_room_quotient=self.big_room_quotient,
      small_room_quotient=self.small_room_quotient,
      map_width=self.map_width,
      map_height=self.map_height,
      engine=self.engine,
      current_floor=self.current_floor
    )
    
    self.saved_floors[self.current_floor] = self.engine.game_map
    #print(f"{self.engine.game_map}\nsaved in\n{self.saved_floors}")
    
  def load_game_map(self, ind_to_load: int) -> None:
    ind_to_load + 20
    self.engine.game_map = self.saved_floors[ind_to_load]
    self.current_floor = ind_to_load