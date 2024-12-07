# set damage change and run the damage handler
# @s = player who needs to have durability changed
# located at world spawn
# run from durability/damage/force/calc_unbreaking

# get durability change
execute store result score $old_damage smithed.item run data get storage smithed.item:main item.tag.Damage
scoreboard players operation $old_damage smithed.item += $delta smithed.item
scoreboard players set $delta smithed.item -1

# update durability
scoreboard players set $force smithed.item 1
execute if score $unbreakable smithed.item matches 0 run function smithed.item:impl/durability/track_changes/process_item
scoreboard players reset $force smithed.item
