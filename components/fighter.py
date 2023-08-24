from __future__ import annotations
from typing import List, TYPE_CHECKING
import color
from components.base_component import BaseComponent
from render_order import RenderOrder
from random import random

if TYPE_CHECKING:
  from entity import Actor

def strip_dam_affinities(dam_affinity: List[str]) -> List[str]:
  if dam_affinity is None or len(dam_affinity) == len(set(dam_affinity)):
    return [x for x in dam_affinity if x != ""]
  no_dupe_affinities = list(set(dam_affinity))
  return [x for x in no_dupe_affinities if x != ""]

class Fighter(BaseComponent):
  
  parent: Actor
  
  def __init__(self, hp: int, base_power: int, base_armor: int, min_dam: int, max_dam: int, damage_type: List[str] = ["bludgeoning"], dam_resist: List[str] = [""], dam_immune: List[str] = [""], dam_absorb: List[str] = ["healing"], dam_vulnerable: List[str] = [""], base_crit_chance: int = 97, base_miss_chance: int = 5):
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
    self.base_crit_chance = base_crit_chance
    self.base_miss_chance = base_miss_chance
    
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
    return self.base_min_dam
  
  @property
  def max_dam(self) -> int:
    if self.parent.equipment:
      return self.parent.equipment.max_dam
    return self.base_max_dam
  
  @property
  def crit_chance(self) -> int:
    return self.base_crit_chance

  # Equipment to provide bonus/penalty?

  @property
  def miss_chance(self) -> int:
    return self.base_miss_chance
  
  # Equipment to provide bonus/penalty?
  
  @property
  def power_bonus(self) -> int:
    if self.parent.equipment is not None and self.parent.equipment.power_bonus:
      return self.parent.equipment.power_bonus
    return 0
      
  @property
  def armor_bonus(self) -> int:
    if self.parent.equipment is not None and self.parent.equipment.armor_bonus:
      return self.parent.equipment.armor_bonus
    return 0
  
  @property
  def damage_type(self) -> List[str]:
    if self.parent.equipment is not None and self.parent.equipment.damage_type:
      stripped_dam_types = strip_dam_affinities(self.parent.equipment.damage_type)
      return stripped_dam_types
    return self.base_damage_type
  
  @property
  def dam_resist(self) -> List[str]:
    if self.parent.equipment is not None and self.parent.equipment.dam_resist:
      combined_resists = self.base_dam_resist.copy()
      combined_resists.extend(self.parent.equipment.dam_resist)
      stripped_combined_resists = strip_dam_affinities(combined_resists)
      return stripped_combined_resists
    return self.base_dam_resist

  @property
  def dam_immune(self) -> List[str]:
    if self.parent.equipment is not None and self.parent.equipment.dam_immune:
      combined_immunes = self.base_dam_immune.copy()
      combined_immunes.extend(self.parent.equipment.dam_immune)
      stripped_combined_immunes = strip_dam_affinities(combined_immunes)
      return stripped_combined_immunes
    return self.base_dam_immune
  
  @property
  def dam_absorb(self) -> List[str]:
    if self.parent.equipment is not None and self.parent.equipment.dam_absorb:
      combined_absorbs = self.base_dam_absorb.copy()
      combined_absorbs.extend(self.parent.equipment.dam_absorb)
      stripped_combined_absorbs = strip_dam_affinities(combined_absorbs)
      return stripped_combined_absorbs
    return self.base_dam_absorb

  @property
  def dam_vulnerable(self) -> List[str]:
    if self.parent.equipment is not None and self.parent.equipment.dam_vulnerable:
      combined_vulnerables = self.base_dam_vulnerable.copy()
      combined_vulnerables.extend(self.parent.equipment.dam_vulnerable)
      stripped_combined_vulnerables = strip_dam_affinities(combined_vulnerables)
      return stripped_combined_vulnerables
    return self.base_dam_vulnerable

  def take_damage(self, amount: int, damage_types: List[str] = [""]) -> int:
    final_amount = amount
    will_absorb = False
    is_immune = False
    is_vulnerable = False
    will_resist = False
    for damage_type in damage_types:
      if damage_type in self.dam_absorb:
        print("Will absorb!")
        will_absorb = True
        break
    if will_absorb:
      print("Damage absorbed!")
      if final_amount + self.hp > self.max_hp:
        final_amount = (self.max_hp - self.hp) * -1
      else:
        final_amount = final_amount * -1
    else:
      final_amount -= self.armor
      if final_amount < 0:
        final_amount = 0
      for damage_type in damage_types:
        if damage_type in self.dam_vulnerable:
          is_vulnerable = True
          break
      if is_vulnerable:
        print("Damage triggered weakness!")
        if final_amount == 0:
          final_amount = 2
        else:
          final_amount = final_amount * 2
      else:
        for damage_type in damage_types:
          if damage_type in self.dam_immune:
            is_immune = True
            break
        if is_immune:
          print("Immune to damage!")
          final_amount = 0
        else:
          for damage_type in damage_types:
            if damage_type in self.dam_resist:
              will_resist = True
              break
          if will_resist:
            print("Damage resisted!")
            if final_amount / 2 < 1:
              final_amount = 0
            else:
              final_amount = int(final_amount / 2)
    if final_amount == 0 and (not will_absorb or not will_resist or not is_immune) and random() >= 0.5:
      final_amount = 1
    #if not will_absorb:
    #  print(f"{self.parent.name} is taking {final_amount} damage!")
    #elif will_absorb and "healing" not in damage_types:
    #  print(f"{self.parent.name} absorbs {final_amount * -1} damage!")
    #elif will_absorb and "healing" in damage_types:
    #  print(f"{self.parent.name} heals {final_amount * -1} damage!")
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