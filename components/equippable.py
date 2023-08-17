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
    dam_loc: float = 2.0,
    dam_scale: float = 1.0
  ):
    self.equipment_type = equipment_type
    self.to_hit_bonus = to_hit_bonus
    self.armor_bonus = armor_bonus
    self.power_bonus = power_bonus
    self.defense_bonus = defense_bonus
    self.dam_loc = dam_loc
    self.dam_scale = dam_scale

class Club(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.WEAPON, dam_loc=3.0, dam_scale=1.0)

class Dagger(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.WEAPON, dam_loc=4.5, dam_scale=2.0)

class Sword(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.WEAPON, dam_loc=5.5, dam_scale=3.0)

class PaddedArmor(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.ARMOR, armor_bonus=1)

class LeatherArmor(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.ARMOR, armor_bonus=2)
    
class ChainMail(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.ARMOR, armor_bonus=3)