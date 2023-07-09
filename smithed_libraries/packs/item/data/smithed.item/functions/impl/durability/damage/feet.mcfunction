# @public

# force damage to the item in the player's feet slot
# @s = player who needs to have durability changed in feet slot
# located at world spawn
# run from api call

# set feet durability
data modify storage smithed.item:main item set from entity @s Inventory[{Slot:100b}]
function smithed.item:impl/durability/damage/force/calc_unbreaking

# update feet
execute if score $out smithed.item matches 1 run item modify entity @s armor.feet smithed.item:impl/update_nbt
execute if score $out smithed.item matches 0 run item replace entity @s armor.feet with air
execute if score $out smithed.item matches -1 run function #smithed.item:event/item_changed/feet

scoreboard players reset $out smithed.item
