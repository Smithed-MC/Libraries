# check if the block is locked
scoreboard players set $locked smithed.actionbar.temp 0
execute if block ~ ~ ~ #smithed.actionbar:__version__/chests unless block ~ ~ ~ #smithed.actionbar:__version__/chests[type=single] run function smithed.actionbar:impl/__version__/vanilla/container/check_double_chest_lock
execute if score $locked smithed.actionbar.temp matches 0 store success score $locked smithed.actionbar.temp if data block ~ ~ ~ Lock

# if the block is locked, show the message
execute if score $locked smithed.actionbar.temp matches 1.. run function smithed.actionbar:impl/__version__/vanilla/container/locked_message
