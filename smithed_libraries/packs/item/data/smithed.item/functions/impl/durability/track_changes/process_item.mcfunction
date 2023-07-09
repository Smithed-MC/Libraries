# checks the item a change in durability
# @s = player who has a custom durability item that changed durability
# located at world spawn
# run from durability/track_changes/process/<SLOT>
# run from durability/damage/force/sub

# compare new and old item damage
execute store result score $new_damage smithed.item run data get storage smithed.item:main item.tag.Damage
execute unless score $force smithed.item matches 1 store result score $old_damage smithed.item run data get storage smithed.item:main item.tag.smithed.durability.damage
execute if score $new_damage smithed.item = $old_damage smithed.item run scoreboard players set $out smithed.item -2
execute unless score $new_damage smithed.item = $old_damage smithed.item run function smithed.item:impl/durability/update/start

# clean up
scoreboard players reset $new_damage smithed.item
scoreboard players reset $old_damage smithed.item
