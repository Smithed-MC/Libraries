# @public

# force damage to the item in the player's chest slot
# @s = player who needs to have durability changed in chest slot
# located at world spawn
# run from api call

# set chest durability
data modify storage smithed.item:main item set from entity @s Inventory[{Slot:102b}]
function smithed.item:impl/durability/damage/force/calc_unbreaking

# update chest
execute if score $out smithed.item matches 1 run item modify entity @s armor.chest smithed.item:impl/update_nbt
execute if score $out smithed.item matches 0 run item replace entity @s armor.chest with air
execute if score $out smithed.item matches -1 run function #smithed.item:event/item_changed/chest

scoreboard players reset $out smithed.item
