#!/usr/bin/env python3
import copy
import traceback
import tcod

import color
from engine import Engine
import entity_factories
import exceptions
import input_handlers
from procgen import generate_dungeon
from procgen_attributes import set_procgen_attributes

def main() -> None:
  screen_width = 80
  screen_height = 50
  
  map_width, map_height, room_max_size, room_min_size, max_rooms, big_room_quotient, small_room_quotient, max_monsters_per_room, max_items_per_room = set_procgen_attributes()
  
  tileset = tcod.tileset.load_tilesheet(
    "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
  )
  
  player = copy.deepcopy(entity_factories.player)
  
  engine = Engine(player=player)
  
  engine.game_map = generate_dungeon(
    max_rooms=max_rooms,
    room_min_size=room_min_size,
    room_max_size=room_max_size,
    big_room_quotient=big_room_quotient,
    small_room_quotient=small_room_quotient,
    map_width=map_width,
    map_height=map_height,
    max_monsters_per_room=max_monsters_per_room,
    max_items_per_room=max_items_per_room,
    engine=engine
  )
  
  engine.update_fov()
  
  engine.message_log.add_message(
    "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
  )
  
  handler: input_handlers.BaseEventHandler = input_handlers.MainGameEventHandler(engine)
  
  with tcod.context.new_terminal(
    screen_width,
    screen_height,
    tileset=tileset,
    title="Yet Another Roguelike Tutorial",
    vsync=True
  ) as context:
    root_console = tcod.console.Console(screen_width, screen_height, order="F")
    try:
      while True:
        root_console.clear()
        handler.on_render(console=root_console)
        context.present(root_console)
        
        try:
          for event in tcod.event.wait():
            context.convert_event(event)
            handler = handler.handle_events(event)
        except Exception:
          traceback.print_exc()
          if isinstance(handler, input_handlers.EventHandler):
            handler.engine.message_log.add_message(
              traceback.format_exc(), color.error
            )
    except exceptions.QuitWithoutSaving:
      raise
    except SystemExit:
      raise
    except BaseException:
      raise

if __name__ == "__main__":
  main()