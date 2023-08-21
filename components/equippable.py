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
    self.min_dam = min_dam
    self.max_dam = max_dam
    self.damage_type = damage_type
    self.dam_resist = dam_resist
    self.dam_immune = dam_immune
    self.dam_absorb = dam_absorb
    self.dam_vulnerable = dam_vulnerable

class Club(Equippable):
  def __init__(self, power_bonus: int = 0, damage_type: str = "bludgeoning") -> None:
    super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=power_bonus, min_dam=1, max_dam=4, damage_type=damage_type)

class Dagger(Equippable):
  def __init__(self, power_bonus: int = 0, damage_type: str = "piercing") -> None:
    super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=power_bonus, min_dam=1, max_dam=5, damage_type=damage_type)

class Sword(Equippable):
  def __init__(self, power_bonus: int = 0, damage_type: str = "slashing") -> None:
    super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=power_bonus, min_dam=2, max_dam=7, damage_type=damage_type)

class PaddedArmor(Equippable):
  def __init__(self, armor_bonus: int = 1, dam_resist: List[str] = [""], dam_immune: List[str] = [""], dam_absorb: List[str] = [""], dam_vulnerable: List[str] = [""]) -> None:
    super().__init__(equipment_type=EquipmentType.ARMOR, armor_bonus=armor_bonus, dam_resist=dam_resist, dam_immune=dam_immune, dam_absorb=dam_absorb, dam_vulnerable=dam_vulnerable)

class LeatherArmor(Equippable):
  def __init__(self, armor_bonus: int = 2, dam_resist: List[str] = [""], dam_immune: List[str] = [""], dam_absorb: List[str] = [""], dam_vulnerable: List[str] = [""]) -> None:
    super().__init__(equipment_type=EquipmentType.ARMOR, armor_bonus=armor_bonus, dam_resist=dam_resist, dam_immune=dam_immune, dam_absorb=dam_absorb, dam_vulnerable=dam_vulnerable)
    
class ChainMail(Equippable):
  def __init__(self, armor_bonus: int = 3, dam_resist: List[str] = [""], dam_immune: List[str] = [""], dam_absorb: List[str] = [""], dam_vulnerable: List[str] = [""]) -> None:
    super().__init__(equipment_type=EquipmentType.ARMOR, armor_bonus=armor_bonus, dam_resist=dam_resist, dam_immune=dam_immune, dam_absorb=dam_absorb, dam_vulnerable=dam_vulnerable)