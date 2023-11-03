# @public

# force damage to the item in the player's offhand
# @s = player who needs to have durability changed in offhand
# located at world spawn
# run from api call

# set offhand durability
data modify storage smithed.item:main item set from entity @s Inventory[{Slot:-106b}]
function smithed.item:impl/durability/damage/force/calc_unbreaking

# update offhand
execute if score $out smithed.item matches 1 run item modify entity @s weapon.offhand smithed.item:impl/update_nbt
execute if score $out smithed.item matches 0 run item replace entity @s weapon.offhand with air
execute if score $out smithed.item matches -1 run function #smithed.item:event/item_changed/offhand

scoreboard players reset $out smithed.item