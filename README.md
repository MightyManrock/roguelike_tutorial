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