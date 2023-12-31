from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import components.ai
import color
import components.inventory
from components.base_component import BaseComponent
from exceptions import Impossible
from input_handlers import (
  ActionOrHandler,
  SingleRangedAttackHandler,
  AreaRangedAttackHandler
)
import dice_roller as droll

if TYPE_CHECKING:
  from entity import Actor, Item
  
class Consumable(BaseComponent):
  parent: Item
  
  def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
    return actions.ItemAction(consumer, self.parent)
    
  def activate(self, action: actions.ItemAction) -> None:
    raise NotImplementedError()
    
  def consume(self) -> None:
    entity = self.parent
    inventory = entity.parent
    if isinstance(inventory, components.inventory.Inventory):
      inventory.items.remove(entity)
    
class ConfusionConsumable(Consumable):
  def __init__(self, number_of_turns: int):
    self.number_of_turns = number_of_turns
    
  def get_action(self, consumer: Actor) -> SingleRangedAttackHandler:
    self.engine.message_log.add_message(
      "Select a target location.", color.needs_target
    )
    return SingleRangedAttackHandler(
      self.engine,
      callback=lambda xy: actions.ItemAction(consumer, self.parent, xy)
    )
  
  def activate(self, action: actions.ItemAction) -> None:
    consumer = action.entity
    target = action.target_actor
    
    if not self.engine.game_map.visible[action.target_xy]:
      raise Impossible("You cannot target an area that you cannot see.")
    if not target:
      raise Impossible("You must select an enemy to target.")
    if target is consumer:
      raise Impossible("You cannot confuse yourself!")
      
    self.engine.message_log.add_message(
      f"The eyes of the {target.name} look vacant, as it starts to stumble around!",
      color.status_effect_applied
    )
    target.ai = components.ai.ConfusedEnemy(
      entity=target, previous_ai=target.ai, turns_remaining=self.number_of_turns
    )
    self.consume()

class HealingConsumable(Consumable):
  def __init__(self, min_heal: int, max_heal: int, damage_type: List[str] = ["healing"]):
    self.min_heal = min_heal
    self.max_heal = max_heal
    self.damage_type = damage_type
  
  def activate(self, action: actions.ItemAction) -> None:
    amount = droll.damage_roll(0, self.min_heal, self.max_heal)
    consumer = action.entity
    amount_recovered = consumer.fighter.take_damage(amount, self.damage_type)
    amount_recovered = abs(amount_recovered)
    
    if amount_recovered > 0:
      self.engine.message_log.add_message(
        f"You consume the {self.parent.name} and recover {amount_recovered} HP!"
      )
      self.consume()
    else:
      raise Impossible(f"Your health is already full.")

class FireballDamageConsumable(Consumable):
  def __init__(self, min_damage: int, max_damage: int, radius: int, damage_type: List[str] = ["fire"]):
    self.min_damage = min_damage
    self.max_damage = max_damage
    self.radius = radius
    self.damage_type = damage_type
    
  def get_action(self, consumer: Actor) -> AreaRangedAttackHandler:
    self.engine.message_log.add_message(
      "Select a target location.", color.needs_target
    )
    return AreaRangedAttackHandler(
      self.engine,
      radius=self.radius,
      callback=lambda xy: actions.ItemAction(consumer, self.parent, xy)
    )
    
  def activate(self, action: actions.ItemAction) -> None:
    target_xy = action.target_xy
    
    if not self.engine.game_map.visible[target_xy]:
      raise Impossible("You cannot target an area that you cannot see.")
      
    targets_hit = False
    for actor in self.engine.game_map.actors:
      if actor.distance(*target_xy) <= self.radius:
        rolled_damage = droll.damage_roll(0, self.min_damage, self.max_damage)
        final_damage = actor.fighter.take_damage(rolled_damage, self.damage_type)
        self.engine.message_log.add_message(
          f"The {actor.name} is engulfed in a fiery explosion, taking {final_damage} damage!"
        )
        targets_hit = True
        
    if not targets_hit:
      raise Impossible("There are no targets in the radius.")
    self.consume()

class LightningDamageConsumable(Consumable):
  def __init__(self, min_damage: int, max_damage: int, maximum_range: int, damage_type: List[str] = ["electric"]):
    self.min_damage = min_damage
    self.max_damage = max_damage
    self.maximum_range = maximum_range
    self.damage_type = damage_type
    
  def activate(self, action: actions.ItemAction) -> None:
    consumer = action.entity
    target = None
    closest_distance = self.maximum_range + 1.0
    
    for actor in self.engine.game_map.actors:
      if actor is not consumer and self.parent.game_map.visible[actor.x, actor.y]:
        distance = consumer.distance(actor.x, actor.y)
        
        if distance < closest_distance:
          target = actor
          closest_distance = distance
    
    if target:
      rolled_damage = droll.damage_roll(0, self.min_damage, self.max_damage)
      final_damage = target.fighter.take_damage(rolled_damage, self.damage_type)
      self.engine.message_log.add_message(
        f"A lightning bolt strikes the {target.name} with a loud thunder, for {final_damage} damage!"
      )
      self.consume()
    else:
      raise Impossible("No enemy is close enough to strike.")