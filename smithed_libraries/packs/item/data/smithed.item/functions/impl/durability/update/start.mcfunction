# runs the custom damage handling
# @s = player who has a custom durability item that changed durability
# located at world spawn
# run from durability/track_changes/process_item

# store durability related values into scoreboard
execute store result score $custom_max smithed.item run data get storage smithed.item:main item.tag.smithed.durability.max
execute unless data storage smithed.item:main item.tag.smithed.durability.dur run function smithed.item:impl/durability/update/initial_data
execute store result score $custom_durability smithed.item run data get storage smithed.item:main item.tag.smithed.durability.dur
execute unless score $item_max smithed.item matches 0.. store result score $item_max smithed.item run data get storage smithed.item:main item.tag.smithed.durability.item_max

# calculate the new durability
execute if score $item_max smithed.item matches 1.. run function smithed.item:impl/durability/update/calc_durability
scoreboard players reset $item_max smithed.item

# if the item broke, play the break sound
execute if score $out smithed.item matches -1..0 run playsound minecraft:entity.item.break player @a[distance=..16]
