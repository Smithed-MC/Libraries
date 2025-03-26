# checks the chest for a change in durability
# @s = player who has a custom durability item in their chest
# located at world spawn
# run from durability/track_changes/get_new

# check chest for changes
data modify storage smithed.item:main item set from storage smithed.item:main player.Inventory[{Slot:102b}]
function smithed.item:impl/durability/track_changes/process_item

# update chest
execute if score $out smithed.item matches 1 run item modify entity @s armor.chest smithed.item:impl/update_nbt
execute if score $out smithed.item matches 0 run item replace entity @s armor.chest with air
execute if score $out smithed.item matches -1 run function #smithed.item:event/item_changed/chest

scoreboard players reset $out smithed.item
