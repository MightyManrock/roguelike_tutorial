from __future__ import annotations

import copy
from typing import Optional

import tcod

import color
from engine import Engine
import entity_factories
import input_handlers
from procgen import generate_dungeon
from procgen_attributes import set_procgen_attributes

background_image = tcod.image.load("menu_background.png")[:, :, :3]

def new_game() -> Engine:
  
  map_width, map_height, room_max_size, room_min_size, max_rooms, big_room_quotient, small_room_quotient, max_monsters_per_room, max_items_per_room = set_procgen_attributes()
  
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
  return engine

class MainMenu(input_handlers.BaseEventHandler):
  def on_render(self, console: tcod.console.Console) -> None:
    console.draw_semigraphics(background_image, 0, 0)
    
    console.print(
      console.width // 2,
      console.height // 2 - 4,
      "TOMBS OF THE ANCIENT KINGS",
      fg=color.menu_title,
      alignment=tcod.CENTER
    )
    console.print(
      console.width // 2,
      console.height - 2,
      "By MightyManrock",
      fg=color.menu_title,
      alignment=tcod.CENTER
    )
    
    menu_width = 24
    for i, text in enumerate(
      ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
    ):
      console.print(
        console.width // 2,
        console.height // 2 - 2 + i,
        text.ljust(menu_width),
        fg=color.menu_text,
        bg=color.black,
        alignment=tcod.CENTER,
        bg_blend=tcod.BKGND_ALPHA(64)
      )
  
  def ev_keydown(
    self, event: tcod.event.KeyDown
  ) -> Optional[input_handlers.BaseEventHandler]:
    if event.sym in (tcod.event.KeySym.q, tcod.event.KeySym.ESCAPE):
      raise SystemExit()
    elif event.sym == tcod.event.KeySym.c:
      pass
    elif event.sym == tcod.event.KeySym.n:
      return input_handlers.MainGameEventHandler(new_game())
    
    return None