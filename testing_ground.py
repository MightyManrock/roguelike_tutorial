import numpy as np

power_bonus = 0
dam_loc = 3.0
dam_scale = 1.5
critical_hit = True

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
  
random_rolls = []

for i in range (0, 15):
  random_rolls.append(damage_roll(power_bonus, dam_loc, dam_scale, critical_hit))

print(random_rolls)