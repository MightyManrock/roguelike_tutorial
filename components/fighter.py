from __future__ import annotations
from typing import List, Set, TYPE_CHECKING
import color
from components.base_component import BaseComponent
from render_order import RenderOrder

if TYPE_CHECKING:
  from entity import Actor

class Fighter(BaseComponent):
  
  parent: Actor
  
  def __init__(self, hp: int, base_power: int, base_armor: int, min_dam: int, max_dam: int, damage_type: str = "bludgeoning", dam_resist: Set = set(), dam_immune: Set = set(), dam_absorb: Set = set(["healing"]), dam_vulnerable: Set = set()):
    self.max_hp = hp
    self._hp = hp
    self.base_power = base_power
    self.base_armor = base_armor
    self.base_min_dam = min_dam
    self.base_max_dam = max_dam
    self.base_damage_type = damage_type
    self.base_dam_resist = dam_resist
    self.base_dam_immune = dam_immune
    self.base_dam_absorb = dam_absorb
    self.base_dam_vulnerable = dam_vulnerable
    
  @property
  def hp(self) -> int:
    return self._hp
  
  @hp.setter
  def hp(self, value: int) -> None:
    self._hp = max(0, min(value, self.max_hp))
    if self._hp == 0 and self.parent.ai:
      self.die()

  @property
  def power(self) -> int:
    return self.base_power + self.power_bonus
    
  @property
  def armor(self) -> int:
    return self.base_armor + self.armor_bonus
  
  @property
  def min_dam(self) -> int:
    if self.parent.equipment:
      return self.parent.equipment.min_dam
    else:
      return self.base_min_dam
  
  @property
  def max_dam(self) -> int:
    if self.parent.equipment:
      return self.parent.equipment.max_dam
    else:
      return self.base_max_dam
    
  @property
  def power_bonus(self) -> int:
    if self.parent.equipment:
      return self.parent.equipment.power_bonus
    else:
      return 0
      
  @property
  def armor_bonus(self) -> int:
    if self.parent.equipment:
      return self.parent.equipment.armor_bonus
    else:
      return 0
  
  @property
  def damage_type(self) -> str:
    if self.parent.equipment:
      return self.parent.equipment.damage_type
    else:
      return self.base_damage_type
  
  @property
  def dam_resist(self) -> Set:
    if self.parent.equipment and self.parent.equipment.dam_resist:
      self.base_dam_resist.union(self.parent.equipment.dam_resist)
    return self.base_dam_resist

  @property
  def dam_immune(self) -> Set:
    if self.parent.equipment and self.parent.equipment.dam_immune:
      self.base_dam_immune.union(self.parent.equipment.dam_immune)
    return self.base_dam_immune
  
  @property
  def dam_absorb(self) -> Set:
    if self.parent.equipment and self.parent.equipment.dam_absorb:
      self.base_dam_absorb.union(self.parent.equipment.dam_absorb)
    return self.base_dam_absorb

  @property
  def dam_vulnerable(self) -> Set:
    if self.parent.equipment and self.parent.equipment.dam_vulnerable:
      self.base_dam_vulnerable.union(self.parent.equipment.dam_vulnerable)
    return self.base_dam_vulnerable
  
  #def heal(self, amount: int) -> int:
  #  if self.hp == self.max_hp:
  #    return 0
    #  
  #  new_hp_value = self.hp + amount
    #  
  #  if new_hp_value > self.max_hp:
  #    new_hp_value = self.max_hp
    #    
  #  amount_recovered = new_hp_value - self.hp
    #  
  #  self.hp = new_hp_value
    #  
  #  return amount_recovered

  def take_damage(self, amount: int, damage_type: str = "") -> int:
    final_amount = amount
    if damage_type in self.dam_absorb:
      print("Damage absorbed!")
      if final_amount + self.hp > self.max_hp:
        final_amount = (self.max_hp - self.hp) * -1
      else:
        final_amount = final_amount * -1
    elif damage_type in self.dam_immune:
      print("Immune to damage!")
      final_amount = 0
    elif damage_type in self.dam_vulnerable:
      print("Damage triggered weakness!")
      if final_amount == 0:
        final_amount = 2
      else:
        final_amount = final_amount * 2
    elif damage_type in self.dam_resist:
      print("Damage resisted!")
      if final_amount / 2 < 1:
        final_amount = 0
      else:
        final_amount = int(final_amount / 2)
    self.hp -= final_amount
    return final_amount

  def die(self) -> None:
    if self.engine.player is self.parent:
      death_message = "You died!"
      death_message_color = color.player_die
    else:
      death_message = f"{self.parent.name} is dead!"
      death_message_color = color.enemy_die
    
    self.parent.char = "%"
    self.parent.color = (191, 0, 0)
    self.parent.blocks_movement = False
    self.parent.ai = None
    self.parent.name = f"remains of {self.parent.name}"
    self.parent.render_order = RenderOrder.CORPSE
    
    self.engine.message_log.add_message(death_message, death_message_color)
    
    self.engine.player.level.add_xp(self.parent.level.xp_given)