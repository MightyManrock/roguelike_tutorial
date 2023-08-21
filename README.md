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
- Misses and Critical Hits:
   - There is a low chance that any attack can either miss entirely or deal extra damage.
- Damage is determined randomly in a predefined ranged for each monster's attack and for different weapons.
- The player and monsters have a "power" stat that adds bonus damage.
- Armor equipment and monsters have an "armor" stat that is used to mitigate damage.
- Damage Types and Affinities:
   - Monster attacks and weapons have damage types.
   - Monsters have damage affinities, e.g., a monster may be weak to or immune to a certain kind of damage, resist or absorb certain other kinds of damage, etc.
   - Armor can also provide damage affinities to the player.

# Features In Progress

## Changes to Combat

Soon damage types will be changed so that a weapon, monster, or spell can have multiple damage types, such as a sword that has both "slashing" damage and "holy" damage, and the logic will be reworked such that, for instance, a monster resistant to "slashing" damage will not have this benefit against a "holy" damage attack from such a sword if the monster is vulnerable to "holy" damage.

## Predetermined Rooms

The starting room will be a predetermined shape and location in the dungeon, and code that will handle drawing and displaying such non-generated rooms will be implemented.

# TO-DO

1. Give the game a title other than the default tutorial name.
2. Change menu screen art.
3. Incorporate release package publishing into workflow.
4. Revamp monster, weapon, and spell damage types to be a list of damage types.
5. Implement new monster types.
6. Implement new room procgen functions (round rooms, etc.)?
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