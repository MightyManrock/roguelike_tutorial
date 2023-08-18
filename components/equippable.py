from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
  from entity import Item
  
class Equippable(BaseComponent):
  parent: Item
  
  def __init__(
    self,
    equipment_type: EquipmentType,
    to_hit_bonus: int = 0,
    armor_bonus: int = 0,
    power_bonus: int = 0,
    defense_bonus: int = 0,
    min_dam: int = 0,
    max_dam: int = 0
  ):
    self.equipment_type = equipment_type
    self.to_hit_bonus = to_hit_bonus
    self.armor_bonus = armor_bonus
    self.power_bonus = power_bonus
    self.defense_bonus = defense_bonus
    self.min_dam = min_dam
    self.max_dam = max_dam

class Club(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.WEAPON, min_dam=1, max_dam=4)

class Dagger(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.WEAPON, min_dam=1, max_dam=5)

class Sword(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.WEAPON, min_dam=2, max_dam=7)

class PaddedArmor(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.ARMOR, armor_bonus=1)

class LeatherArmor(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1, armor_bonus=2)
    
class ChainMail(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=2, armor_bonus=3)