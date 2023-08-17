import numpy as np

def to_hit_roll():
  critical_hit = False
  critical_miss = False
  rand_roll = int(np.random.normal(loc=11.5, scale=4.5))
  if rand_roll < 0:
    rand_roll = rand_roll * -1
  elif rand_roll == 0 or rand_roll == 1:
    rand_roll = 1
    critical_miss = True
  elif rand_roll > 20:
    rand_roll = 20
    critical_hit = True
  return rand_roll, critical_hit, critical_miss

def damage_roll(power_bonus: int, dam_loc: float, dam_scale: float, critical_hit: bool = False) -> int:
  damage_total = 1
  if critical_hit:
    damage_total = 0
    rand_rolls = []
    rand_rolls.append(int(dam_loc + dam_scale))
    rand_rolls.append(int(np.random.normal(loc=dam_loc, scale=dam_scale)))
    for i in range(len(rand_rolls)):
      if rand_rolls[i] < 0:
        rand_rolls[i] = rand_rolls[i] * -1
      elif rand_rolls[i] == 0:
        rand_rolls[i] = 1
      damage_total += rand_rolls[i]
    damage_total += power_bonus * 2
  else:
    rand_roll = int(np.random.normal(loc=dam_loc, scale=dam_scale))
    if rand_roll < 0:
      rand_roll = rand_roll * -1
    elif rand_roll == 0:
      rand_roll = 1
    damage_total = rand_roll + power_bonus
  return damage_total