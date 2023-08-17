from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING

import color
import exceptions
import dice_roller as droll

if TYPE_CHECKING:
  from engine import Engine
  from entity import Actor, Entity, Item

class Action:

  def __init__(self, entity: Actor) -> None:
    super().__init__()
    self.entity = entity
  
  @property
  def engine(self) -> Engine:
    return self.entity.game_map.engine

  def perform(self) -> None:
    raise NotImplementedError()

class PickupAction(Action):
  def __init__(self, entity: Actor):
    super().__init__(entity)
  
  def perform(self) -> None:
    actor_location_x = self.entity.x
    actor_location_y = self.entity.y
    inventory = self.entity.inventory
    
    for item in self.engine.game_map.items:
      if actor_location_x == item.x and actor_location_y == item.y:
        if len(inventory.items) >= inventory.capacity:
          raise exceptions.Impossible("Your inventory is full.")
          
        self.engine.game_map.entities.remove(item)
        item.parent = self.entity.inventory
        inventory.items.append(item)
        
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
    return self.engine.game_map.get_actor_at_location(*self.target_xy)
    
  def perform(self) -> None:
    if self.item.consumable:
      self.item.consumable.activate(self)

class DropItem(ItemAction):
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

class WaitAction(Action):
  def perform(self) -> None:
    pass

class TakeStairsDownAction(Action):
  def perform(self) -> None:
    if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
      if self.engine.game_world.saved_floors[self.engine.game_world.current_floor - 1]:
        #print(f"Detected {self.engine.game_world.saved_floors[self.engine.game_world.current_floor - 1]}\nin\n{self.engine.game_world.saved_floors}")
        self.engine.game_world.load_game_map(self.engine.game_world.current_floor - 1)
        self.engine.player.place(*self.engine.game_map.upstairs_location, self.engine.game_map)
      else:
        self.engine.game_world.generate_floor(floor_change=-1)
      self.engine.message_log.add_message(
        "You descend the staircase.", color.descend
      )
    else:
      raise exceptions.Impossible("There are no stairs here.")
      
class TakeStairsUpAction(Action):
  def perform(self) -> None:
    if (self.entity.x, self.entity.y) == self.engine.game_map.upstairs_location:
      if self.engine.game_world.saved_floors[self.engine.game_world.current_floor + 1]:
        #print(f"Detected {self.engine.game_world.saved_floors[self.engine.game_world.current_floor + 1]}\nin\n{self.engine.game_world.saved_floors}")
        self.engine.game_world.load_game_map(self.engine.game_world.current_floor + 1)
        self.engine.player.place(*self.engine.game_map.downstairs_location, self.engine.game_map)
      else:
        self.engine.game_world.generate_floor(floor_change=1)
      self.engine.message_log.add_message(
        "You ascend the staircase.", color.ascend
      )
    else:
      raise exceptions.Impossible("There are no stairs here.")

class ActionWithDirection(Action):
  def __init__(self, entity: Actor, dx: int = 0, dy: int = 0):
    super().__init__(entity)
    
    self.dx = dx
    self.dy = dy
    
  @property
  def dest_xy(self) -> Tuple[int, int]:
    return self.entity.x + self.dx, self.entity.y + self.dy
  
  @property
  def blocking_entity(self) -> Optional[Entity]:
    return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)
  
  @property
  def target_actor(self) -> Optional[Actor]:
    return self.engine.game_map.get_actor_at_location(*self.dest_xy)
  
  def perform(self) -> None:
    raise NotImplementedError()

class MeleeAction(ActionWithDirection):

  def perform(self) -> None:
    target = self.target_actor
    if not target:
      raise exceptions.Impossible("Nothing to attack.")

    if self.entity is self.engine.player:
      attack_color = color.player_atk
    else:
      attack_color = color.enemy_atk
    
    roll_to_hit = False
    critical_hit = False
    critical_miss = False
    rand_roll, critical_hit, critical_miss = droll.to_hit_roll()
    mod_roll = rand_roll + self.entity.fighter.to_hit
    if mod_roll >= target.fighter.defense:
      roll_to_hit = True
    
    if critical_miss or not roll_to_hit:
      attack_desc = f"{self.entity.name.capitalize()} attacks {target.name} but misses ({mod_roll} vs. {target.fighter.defense})"
      if critical_miss:
        attack_desc += " critically!"
      else:
        attack_desc += "."
      self.engine.message_log.add_message(
        attack_desc, attack_color
      )
    else:
      attack_desc = f"{self.entity.name.capitalize()} hits {target.name} ({mod_roll} vs. {target.fighter.defense})"
      if critical_hit:
        attack_desc += " and hits critically!"
      damage = droll.damage_roll(self.entity.fighter.power, self.entity.fighter.dam_loc, self.entity.fighter.dam_scale, critical_hit)
      damage -= target.fighter.armor

      if damage > 0:
        self.engine.message_log.add_message(
          f"{attack_desc} for {damage} hit points.", attack_color
        )
        target.fighter.hp -= damage
      else:
        self.engine.message_log.add_message(
          f"{attack_desc} but does no damage.", attack_color
        )

class MovementAction(ActionWithDirection):
  def perform(self) -> None:
    dest_x, dest_y = self.dest_xy
    
    if not self.engine.game_map.in_bounds(dest_x, dest_y):
      raise exceptions.Impossible("That way is blocked.")
    if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
      raise exceptions.Impossible("That way is blocked.")
    if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
      raise exceptions.Impossible("That way is blocked.")
    
    self.entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
  def perform(self) -> None:
    if self.target_actor:
      return MeleeAction(self.entity, self.dx, self.dy).perform()
      
    else:
      return MovementAction(self.entity, self.dx, self.dy).perform()