# check if the double chest is locked
# @s = player who clicked on a double chest
# located at the center of the clicked block
# run from vanilla/container/check_lock

# check attached block
scoreboard players set $facing_resolved smithed.actionbar.temp 0
execute if score $facing_resolved smithed.actionbar.temp matches 0 if block ~ ~ ~ #smithed.actionbar:impl/chests[facing=north] run function smithed.actionbar:impl/vanilla/container/check_double_chest_lock/north
execute if score $facing_resolved smithed.actionbar.temp matches 0 if block ~ ~ ~ #smithed.actionbar:impl/chests[facing=east] run function smithed.actionbar:impl/vanilla/container/check_double_chest_lock/east
execute if score $facing_resolved smithed.actionbar.temp matches 0 if block ~ ~ ~ #smithed.actionbar:impl/chests[facing=south] run function smithed.actionbar:impl/vanilla/container/check_double_chest_lock/south
execute if score $facing_resolved smithed.actionbar.temp matches 0 if block ~ ~ ~ #smithed.actionbar:impl/chests[facing=west] run function smithed.actionbar:impl/vanilla/container/check_double_chest_lock/west
