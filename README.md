# roguelike_tutorial
Python/TCOD roguelike tutorial

# About
This is a personal Python project following a tutorial to build a simple roguelike game using the TCOD library.

The tutorial is [here](https://rogueliketutorials.com/tutorials/tcod/v2/).

# Features So Far

- All features up through part 12 of the tutorial.
- Changes to reflect updates to TCOD library since the tutorial was first written.
- Implementation of imageio library to replace soon-to-be-deprecated `tcod.image.load()` function.
- Additional logic to tweak procgen randomness.
- Generated floor storage (previously visited floors remain in memory and can be revisited).
- Can ascend to new floors as well as descend.
- Character level displayed in UI panel.
- Probably some stuff I forgot.

# TO-DO

1. Complete [part 13](https://rogueliketutorials.com/tutorials/tcod/v2/part-13).
2. Give the game a title other than the default tutorial name.
3. Change menu screen art.
4. Incorporate release package publishing into workflow.
5. Implement new monster types.
6. Implement new room procgen functions (round rooms, etc.)?
7. Implement combat changes:
   - Random roll for to-hit.
   - Split `actor.fighter.defense` into an agility stat to avoid being hit (inherent to character, can be leveled up) and a defense stat (from armor, etc.) to absorb damage.
8. Implement non-scroll-based ranged combat (i.e., bows, etc.)?
9. Add new equipment?
10. Implement character classes?
11. Implement inherent spellcasting for certain classes?
    - Implement MP? 
12. Add new scrolls/consumables?
13. Add new monster types?
14. Implement special actions for classes?
15. Implement monster inventory?
16. Implement monsters that have ranged attacks or spellcasting?
17. Implement game sequence (overall goal, altered tables based on game state, preset starting room with dungeon exit)?
18. Implement boss monsters?
19. Implement warp portals and "demiplane" location maps?
