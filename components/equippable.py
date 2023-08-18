from __future__ import annotations

from typing import List, TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
  from entity import Item
  
class Equippable(BaseComponent):
  parent: Item
  
  def __init__(
    self,
    equipment_type: EquipmentType,
    armor_bonus: int = 0,
    power_bonus: int = 0,
    defense_bonus: int = 0,
    min_dam: int = 0,
    max_dam: int = 0,
    damage_type: str = "",
    dam_resist: List[str] = [""],
    dam_immune: List[str] = [""],
    dam_absorb: List[str] = [""],
    dam_vulnerable: List[str] = [""]
  ):
    self.equipment_type = equipment_type
    self.armor_bonus = armor_bonus
    self.power_bonus = power_bonus
    self.defense_bonus = defense_bonus
    self.min_dam = min_dam
    self.max_dam = max_dam
    self.damage_type = damage_type
    self.dam_resist = dam_resist
    self.dam_immune = dam_immune
    self.dam_absorb = dam_absorb
    self.dam_vulnerable = dam_vulnerable

class Club(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.WEAPON, min_dam=1, max_dam=4, damage_type="bludgeoning")

class Dagger(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.WEAPON, min_dam=1, max_dam=5, damage_type="piercing")

class Sword(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.WEAPON, min_dam=2, max_dam=7, damage_type="slashing")

class PaddedArmor(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.ARMOR, armor_bonus=1, dam_resist=["bludgeoning"])

class LeatherArmor(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.ARMOR, armor_bonus=2)
    
class ChainMail(Equippable):
  def __init__(self) -> None:
    super().__init__(equipment_type=EquipmentType.ARMOR, armor_bonus=3, dam_resist=["slashing"])