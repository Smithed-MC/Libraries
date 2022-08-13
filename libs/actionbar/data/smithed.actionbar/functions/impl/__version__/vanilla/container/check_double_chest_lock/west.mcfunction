# store whether the clicked chest is locked
scoreboard players set $facing_resolved smithed.actionbar.temp 1
scoreboard players operation $this_locked smithed.actionbar.temp = $locked smithed.actionbar.temp

# check if the other chest is locked
execute store result score $right_chest smithed.actionbar.temp if block ~ ~ ~ #smithed.actionbar:__version__/chests[type=right]
execute if score $right_chest smithed.actionbar.temp matches 1 if data block ~ ~ ~1 Lock run scoreboard players add $locked smithed.actionbar.temp 1
execute if score $right_chest smithed.actionbar.temp matches 0 if data block ~ ~ ~-1 Lock run scoreboard players add $locked smithed.actionbar.temp 1

# if both chests are locked, use the name of the left-most chest
execute if score $locked smithed.actionbar.temp matches 2 if score $right_chest smithed.actionbar.temp matches 1 run data modify storage smithed.actionbar:input container_name set from block ~ ~ ~ CustomName
execute if score $locked smithed.actionbar.temp matches 2 if score $right_chest smithed.actionbar.temp matches 0 run data modify storage smithed.actionbar:input container_name set from block ~ ~ ~-1 CustomName

# if only one chest is locked, use the name of the locked chest
execute if score $locked smithed.actionbar.temp matches 1 if score $this_locked smithed.actionbar.temp matches 1 run data modify storage smithed.actionbar:input container_name set from block ~ ~ ~ CustomName
execute if score $locked smithed.actionbar.temp matches 1 if score $this_locked smithed.actionbar.temp matches 0 if score $right_chest smithed.actionbar.temp matches 1 run data modify storage smithed.actionbar:input container_name set from block ~ ~ ~1 CustomName
execute if score $locked smithed.actionbar.temp matches 1 if score $this_locked smithed.actionbar.temp matches 0 if score $right_chest smithed.actionbar.temp matches 0 run data modify storage smithed.actionbar:input container_name set from block ~ ~ ~-1 CustomName
