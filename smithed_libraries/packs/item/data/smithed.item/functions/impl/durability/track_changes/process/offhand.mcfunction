# checks the offhand for a change in durability
# @s = player who has a custom durability item in their offhand
# located at world spawn
# run from durability/track_changes/get_new

# check offhand for changes
data modify storage smithed.item:main item set from storage smithed.item:main player.Inventory[{Slot:-106b}]
function smithed.item:impl/durability/track_changes/process_item

# update offhand
execute if score $out smithed.item matches 1 run item modify entity @s weapon.offhand smithed.item:impl/update_nbt
execute if score $out smithed.item matches 0 run item replace entity @s weapon.offhand with air
execute if score $out smithed.item matches -1 run function #smithed.item:event/item_changed/offhand

scoreboard players reset $out smithed.item
