from __future__ import annotations

from typing import List, Set, Optional, TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
  from entity import Actor, Item
  
class Equipment(BaseComponent):
  parent: Actor
  
  def __init__(self, weapon: Optional[Item] = None, armor: Optional[Item] = None):
    self.weapon = weapon
    self.armor = armor
  
  @property
  def armor_bonus(self) -> int:
    bonus = 0
    
    if self.weapon is not None and self.weapon.equippable is not None:
      bonus += self.weapon.equippable.armor_bonus
    
    if self.armor is not None and self.armor.equippable is not None:
      bonus += self.armor.equippable.armor_bonus
    
    return bonus
    
  @property
  def power_bonus(self) -> int:
    bonus = 0
    
    if self.weapon is not None and self.weapon.equippable is not None:
      bonus += self.weapon.equippable.power_bonus
    
    if self.armor is not None and self.armor.equippable is not None:
      bonus += self.armor.equippable.power_bonus
    
    return bonus
  
  @property
  def min_dam(self) -> int:
    if self.weapon is not None and self.weapon.equippable is not None:
      return self.weapon.equippable.min_dam
    else:
      return 1
  
  @property
  def max_dam(self) -> int:
    if self.weapon is not None and self.weapon.equippable is not None:
      return self.weapon.equippable.max_dam
    else:
      return 3
      
  @property
  def damage_type(self) -> str:
    if self.weapon is not None and self.weapon.equippable is not None:
      return self.weapon.equippable.damage_type
    else:
      return ""
  
  @property
  def dam_resist(self) -> Set:
    if self.armor is not None and self.armor.equippable is not None:
      return self.armor.equippable.dam_resist
    else:
      return set()
  
  @property
  def dam_immune(self) -> Set:
    if self.armor is not None and self.armor.equippable is not None:
      return self.armor.equippable.dam_immune
    else:
      return set()
  
  @property
  def dam_absorb(self) -> Set:
    if self.armor is not None and self.armor.equippable is not None:
      return self.armor.equippable.dam_absorb
    else:
      return set()
  
  @property
  def dam_vulnerable(self) -> Set:
    if self.armor is not None and self.armor.equippable is not None:
      return self.armor.equippable.dam_vulnerable
    else:
      return set()
    
  
  def item_is_equipped(self, item: Item) -> bool:
    return self.weapon == item or self.armor == item
  
  def equip_message(self, item_name: str) -> None:
    self.parent.game_map.engine.message_log.add_message(
      f"You equip the {item_name}."
    )
  
  def unequip_message(self, item_name: str) -> None:
    self.parent.game_map.engine.message_log.add_message(
      f"You remove the {item_name}."
    )
  
  def equip_to_slot(self, slot: str, item: Item, add_message: bool) -> None:
    current_item = getattr(self, slot)
    
    if current_item is not None:
      self.unequip_from_slot(slot, add_message)
    
    setattr(self, slot, item)
    
    if add_message:
      self.equip_message(item.name)
  
  def unequip_from_slot(self, slot: str, add_message: bool) -> None:
    current_item = getattr(self, slot)
    
    if add_message:
      self.unequip_message(current_item.name)
    setattr(self, slot, None)
  
  def toggle_equip(self, equippable_item: Item, add_message: bool = True) -> None:
    if (
      equippable_item.equippable
      and equippable_item.equippable.equipment_type == EquipmentType.WEAPON
    ):
      slot = "weapon"
    else:
      slot = "armor"
    
    if getattr(self, slot) == equippable_item:
      self.unequip_from_slot(slot, add_message)
    else:
      self.equip_to_slot(slot, equippable_item, add_message)