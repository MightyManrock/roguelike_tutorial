from random import randint

def crit_roll():
  critical_hit = False
  critical_miss = False
  rand_roll = randint(1, 20)
  if rand_roll == 1:
    critical_miss = True
  elif rand_roll == 20:
    critical_hit = True
  return critical_hit, critical_miss

def damage_roll(power_bonus: int, min_dam: int, max_dam: int, critical_hit: bool = False) -> int:
  if critical_hit:
    damage_total = max_dam + randint(min_dam, max_dam) + (power_bonus * 2)
  else:
    damage_total = randint(min_dam, max_dam) + power_bonus
  return damage_total