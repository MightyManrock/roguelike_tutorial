from random import randint

def crit_roll(crit_chance: int = 97, miss_chance: int = 5):
  critical_hit = False
  critical_miss = False
  rand_roll = randint(1, 100)
  if rand_roll <= miss_chance:
    critical_miss = True
  elif rand_roll > crit_chance:
    critical_hit = True
  #print(f"Roll: {rand_roll}")
  return critical_hit, critical_miss

def damage_roll(power_bonus: int, min_dam: int, max_dam: int, critical_hit: bool = False) -> int:
  if critical_hit:
    damage_total = max_dam + randint(min_dam, max_dam) + (power_bonus * 2)
  else:
    damage_total = randint(min_dam, max_dam) + power_bonus
  #print(f"Damage: {damage_total}")
  return damage_total