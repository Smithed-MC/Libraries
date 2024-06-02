####################
# Creates the extra output items that are needed
####################

# Then, remove the required number of output slots
execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot:2b}].count
scoreboard players operation @s smithed.data -= $temp2 smithed.data
item modify block ~ ~ ~ container.2 smithed.crafter:impl/set_count_from_score

execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot:3b}].count
scoreboard players operation @s smithed.data -= $temp2 smithed.data
item modify block ~ ~ ~ container.3 smithed.crafter:impl/set_count_from_score

execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot:4b}].count
scoreboard players operation @s smithed.data -= $temp2 smithed.data
item modify block ~ ~ ~ container.4 smithed.crafter:impl/set_count_from_score

execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot:11b}].count
scoreboard players operation @s smithed.data -= $temp2 smithed.data
item modify block ~ ~ ~ container.11 smithed.crafter:impl/set_count_from_score

execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot:12b}].count
scoreboard players operation @s smithed.data -= $temp2 smithed.data
item modify block ~ ~ ~ container.12 smithed.crafter:impl/set_count_from_score

execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot:13b}].count
scoreboard players operation @s smithed.data -= $temp2 smithed.data
item modify block ~ ~ ~ container.13 smithed.crafter:impl/set_count_from_score

execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot:20b}].count
scoreboard players operation @s smithed.data -= $temp2 smithed.data
item modify block ~ ~ ~ container.20 smithed.crafter:impl/set_count_from_score

execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot:21b}].count
scoreboard players operation @s smithed.data -= $temp2 smithed.data
item modify block ~ ~ ~ container.21 smithed.crafter:impl/set_count_from_score

execute store result score @s smithed.data run data get block ~ ~ ~ Items[{Slot:22b}].count
scoreboard players operation @s smithed.data -= $temp2 smithed.data
item modify block ~ ~ ~ container.22 smithed.crafter:impl/set_count_from_score

# $temp2 now stores the number of extra items that need to be spawned, and in turn, the count that needs to be removed from each slot
# Recreate the output nbt so it can be used to create the extras
function smithed.crafter:impl/block/table/crafting/input/read_barrel
data modify storage smithed.crafter:main root.temp.item set from block ~ ~ ~ Items[{Slot:16b}]
data remove block ~ ~ ~ Items[{Slot:16b}]

execute as @p[distance=..12,tag=smithed.inside_crafter,tag=smithed.shift_clicked] at @s run function smithed.crafter:impl/block/table/crafting/output/shift_click/spawn_extra_items
function smithed.crafter:impl/block/table/crafting/input/read_barrel
tag @s remove smithed.crafter.assembled_output
data modify entity @s ArmorItems[3].components."minecraft:custom_data".smithed.stored_output set value {Slot:16b}
data modify entity @s ArmorItems[3].components."minecraft:custom_data".smithed.stored_barrel_data set from block ~ ~ ~ Items
