# @public

# force damage to the item in the player's legs slot
# @s = player who needs to have durability changed in legs slot
# located at world spawn
# run from api call

# set legs durability
data modify storage smithed.item:main item set from entity @s Inventory[{Slot:101b}]
function smithed.item:impl/durability/damage/force/calc_unbreaking

# update legs
execute if score $out smithed.item matches 1 run item modify entity @s armor.legs smithed.item:impl/update_nbt
execute if score $out smithed.item matches 0 run item replace entity @s armor.legs with air
execute if score $out smithed.item matches -1 run function #smithed.item:event/item_changed/legs

scoreboard players reset $out smithed.item
