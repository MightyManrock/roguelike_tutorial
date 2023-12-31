from __future__ import annotations

import imageio.v3 as iio
import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod
from tcod import libtcodpy

import color
from engine import Engine
import entity_factories
import input_handlers
from game_map import GameWorld
from procgen_attributes import set_procgen_attributes

background_image = iio.imread("images/menu_background.png")

def new_game() -> Engine:
  
  map_width, map_height, room_max_size, room_min_size, max_rooms, big_room_quotient, small_room_quotient = set_procgen_attributes()
  
  player = copy.deepcopy(entity_factories.player)
  
  engine = Engine(player=player)
  
  engine.game_world = GameWorld(
    engine=engine,
    max_rooms=max_rooms,
    room_min_size=room_min_size,
    room_max_size=room_max_size,
    big_room_quotient=big_room_quotient,
    small_room_quotient=small_room_quotient,
    map_width=map_width,
    map_height=map_height
  )
  
  engine.game_world.generate_floor()
  engine.update_fov()
  
  engine.message_log.add_message(
    "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
  )
  
  club = copy.deepcopy(entity_factories.club)
  padded_armor = copy.deepcopy(entity_factories.padded_armor)
  
  club.parent = player.inventory
  padded_armor.parent = player.inventory
  
  player.inventory.items.append(club)
  player.equipment.toggle_equip(club, add_message=False)
  
  player.inventory.items.append(padded_armor)
  player.equipment.toggle_equip(padded_armor, add_message=False)
  
  print(player.fighter.damage_type)
  print(player.fighter.dam_absorb)
  
  return engine

def load_game(filename: str) -> Engine:
  with open(filename, "rb") as f:
    engine = pickle.loads(lzma.decompress(f.read()))
  assert isinstance(engine, Engine)
  return engine

class MainMenu(input_handlers.BaseEventHandler):
  def on_render(self, console: tcod.console.Console) -> None:
    console.draw_semigraphics(background_image, 0, 0)
    
    console.print(
      console.width // 2,
      console.height // 2 - 4,
      "TOMBS OF THE ANCIENT KINGS",
      fg=color.menu_title,
      alignment=libtcodpy.CENTER
    )
    console.print(
      console.width // 2,
      console.height - 2,
      "By MightyManrock",
      fg=color.menu_title,
      alignment=libtcodpy.CENTER
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
        alignment=libtcodpy.CENTER,
        bg_blend=libtcodpy.BKGND_ALPHA(64)
      )
  
  def ev_keydown(
    self, event: tcod.event.KeyDown
  ) -> Optional[input_handlers.BaseEventHandler]:
    if event.sym in (tcod.event.KeySym.q, tcod.event.KeySym.ESCAPE):
      raise SystemExit()
    elif event.sym == tcod.event.KeySym.c:
      try:
        return input_handlers.MainGameEventHandler(load_game("saves/savegame.sav"))
      except FileNotFoundError:
        return input_handlers.PopupMessage(self, "No saved game to load.")
      except Exception as exc:
        traceback.print_exc()
        return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
    elif event.sym == tcod.event.KeySym.n:
      return input_handlers.MainGameEventHandler(new_game())
    
    return None