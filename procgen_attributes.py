import random

def set_procgen_attributes():
  map_width = 80
  map_height = 43
  
  room_max_size = 16
  room_min_size = 4
  max_rooms = 30
  big_room_quotient = 6
  small_room_quotient = 8
  
  max_monsters_per_room = 2
  max_items_per_room = 2
  
  return map_width, map_height, room_max_size, room_min_size, max_rooms, big_room_quotient, small_room_quotient, max_monsters_per_room, max_items_per_room
  
#def randomize_procgen_attributes(current_floor):
#  map_width = random.randint(40, 80)
#  map_height = random.randint(26, 43)
#  
#  room_max_size = random.randint(8, 16)
#  room_min_size = random.randint(3, 6)
#  
#  if room_min_size >= room_max_size:
#    room_max_size = room_min_size
#    room_max_size += 2
#    room_min_size -= 1
#  
#  max_rooms = random.randint(5, 30)
#  big_room_quotient = random.randint(3, 9)
#  small_room_quotient = random.randint(2, 10)
#  
#  if big_room_quotient == small_room_quotient:
#    big_room_quotient -= 1
#    small_room_quotient += 1
#  
#  max_monsters_per_room = random.randint(1, int(2 + (abs(current_floor - 20) // 4)))
#  max_items_per_room = random.randint(1, int(1 + (abs(current_floor - 20) // 6)))
#  
#  return map_width, map_height, room_max_size, room_min_size, max_rooms, big_room_quotient, small_room_quotient, max_monsters_per_room, max_items_per_room