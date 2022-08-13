# check clicked block
execute if data block ~ ~ ~ Lock run scoreboard players set $locked smithed.actionbar.temp 1

# check attached block
scoreboard players set $facing_resolved smithed.actionbar.temp 0
execute if score $facing_resolved smithed.actionbar.temp matches 0 if block ~ ~ ~ #smithed.actionbar:__version__/chests[facing=north] run function smithed.actionbar:impl/__version__/vanilla/container/check_double_chest_lock/north
execute if score $facing_resolved smithed.actionbar.temp matches 0 if block ~ ~ ~ #smithed.actionbar:__version__/chests[facing=east] run function smithed.actionbar:impl/__version__/vanilla/container/check_double_chest_lock/east
execute if score $facing_resolved smithed.actionbar.temp matches 0 if block ~ ~ ~ #smithed.actionbar:__version__/chests[facing=south] run function smithed.actionbar:impl/__version__/vanilla/container/check_double_chest_lock/south
execute if score $facing_resolved smithed.actionbar.temp matches 0 if block ~ ~ ~ #smithed.actionbar:__version__/chests[facing=west] run function smithed.actionbar:impl/__version__/vanilla/container/check_double_chest_lock/west

# prevent double name set
execute if score $locked smithed.actionbar.temp matches 1.. run scoreboard players set $locked smithed.actionbar.temp 2
