# @public

# force damage to the item in the player's head slot
# @s = player who needs to have durability changed in head slot
# located at world spawn
# run from api call

# set head durability
data modify storage smithed.item:main item set from entity @s Inventory[{Slot:103b}]
function smithed.item:impl/durability/damage/force/calc_unbreaking

# update head
execute if score $out smithed.item matches 1 run item modify entity @s armor.head smithed.item:impl/update_nbt
execute if score $out smithed.item matches 0 run item replace entity @s armor.head with air
execute if score $out smithed.item matches -1 run function #smithed.item:event/item_changed/head

scoreboard players reset $out smithed.item
