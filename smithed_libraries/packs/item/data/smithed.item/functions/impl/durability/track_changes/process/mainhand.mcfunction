# checks the mainhand for a change in durability
# @s = player who has a custom durability item in their mainhand
# located at world spawn
# run from durability/track_changes/get_new

# check mainhand for changes
data modify storage smithed.item:main item set from storage smithed.item:main player.SelectedItem
function smithed.item:impl/durability/track_changes/process_item

# update mainhand
execute if score $out smithed.item matches 1 run item modify entity @s weapon.mainhand smithed.item:impl/update_nbt
execute if score $out smithed.item matches 0 run item replace entity @s weapon.mainhand with air
execute if score $out smithed.item matches -1 run function #smithed.item:event/item_changed/mainhand

scoreboard players reset $out smithed.item
