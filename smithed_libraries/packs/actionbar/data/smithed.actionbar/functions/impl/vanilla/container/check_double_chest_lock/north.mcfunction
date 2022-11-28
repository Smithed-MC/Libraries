# check if the double chest is locked
# @s = player who clicked on a double chest
# located at the center of the clicked block
# run from vanilla/container/check_double_chest_lock

# check if the other chest is locked
execute if block ~ ~ ~ #smithed.actionbar:impl/chests[type=right] store success score $locked smithed.actionbar.temp if data block ~-1 ~ ~ Lock
execute if block ~ ~ ~ #smithed.actionbar:impl/chests[type=left] store success score $locked smithed.actionbar.temp if data block ~1 ~ ~ Lock
