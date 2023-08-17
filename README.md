# roguelike_tutorial
Python/TCOD roguelike tutorial

# About
This is a personal Python project following a tutorial to build a simple roguelike game using the TCOD library.

The tutorial is [here](https://rogueliketutorials.com/tutorials/tcod/v2/).

# Features So Far

- All features from the tutorial.
- Changes to reflect updates to TCOD library since the tutorial was first written.
- Implementation of imageio library to replace soon-to-be-deprecated `tcod.image.load()` function.
- Additional logic to tweak procgen randomness.
- Generated floor storage (previously visited floors remain in memory and can be revisited).
- Can ascend to new floors as well as descend.
- Character level displayed in UI panel.
- Probably some stuff I forgot.

# Features In Progress

## Changes to Combat

Currently, the game follows the tutorial's combat engine:
   
   - entities deal HP damage based on their power stat (with an inherent `base_power` augmented by a `power_bonus` from equipment);
   - entities soak damage based on their defense stat (with an inherent `base_defense` augmented by a `defense_bonus` from equipment).

The combat redesign will achieve the following:
   
   - combat will involve a random roll to hit, and on a successful hit, damage will be randomized within a small range;
   - entities will have an inherent `base_to_hit` stat, which the player can level up and which increases the likelihood of success on the random roll to hit;
   - entities will have an inherent `base_power` stat (which the player *cannot* level up) that will influence the randomly rolled damage;
   - entities will have an inherent `base_defense` stat, which the player can level up and which decreases the likelihood of an attack roll succeeding on them;
   - entities will have an inherent `base_armor` stat (which the player *cannot* level up) that will reduce the damage taken from damage rolls.

Equipment will function as follows:
   
   - armor will provide an `armor_bonus` to soak damage;
   - weapons will each have a `damage_calculation` function for determining random damage;
   - monsters will either have equipment themselves or have an inherent `damage_calculation` function for their attacks;
   - either type of equipment may provide additional benefits, such as a `to_hit_bonus` or `defense_bonus`.

# TO-DO

1. Give the game a title other than the default tutorial name.
2. Change menu screen art.
3. Incorporate release package publishing into workflow.
4. Implement new monster types.
5. Implement new room procgen functions (round rooms, etc.)?
6. Implement combat changes:
   - Random roll for to-hit.
   - Randomized damage? Critical hits?
   - Split `actor.fighter.defense` into an agility stat to avoid being hit (inherent to character, can be leveled up) and a defense stat (from armor, etc.) to absorb damage.
7. Implement non-scroll-based ranged combat (i.e., bows, etc.)?
   - Ammunition system?
8. Add new equipment?
   - Add equipment slots?
9. Implement character classes?
10. Implement inherent spellcasting for certain classes?
    - Implement MP?
11. Implement level maximum?
12. Add new scrolls/consumables?
13. Add new special monster types for highest/lowest floors?
14. Add class-synergizing equipment (staves, etc.)?
15. Implement special actions for classes?
16. Implement monster inventory?
17. Implement monsters that have ranged attacks or spellcasting?
18. Implement game sequence (overall goal, altered tables based on game state, preset starting room with dungeon exit)?
    - Score/grade on dungeon exit or death?
19. Implement boss monsters?
20. Implement warp portals and "demiplane" location maps?
    - Implement special color palettes for highest/lowest dungeon floors and "demiplane" locations?
21. Implement more advanced speed/timing system?