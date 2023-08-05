# force damage to the item
# @s = player who needs to have durability changed
# located at world spawn
# run from durability/damage/<SLOT>

# get unbreaking level
execute store result score $unbreaking_lvl smithed.item run data get storage smithed.item:main item.tag.Enchantments[{id:"minecraft:unbreaking"}].lvl

# check if the item is unbreakable
scoreboard players set $unbreakable smithed.item 0
execute store result score $unbreakable smithed.item run data get storage smithed.item:main item.tag.Unbreakable 1
execute unless score $unbreakable smithed.item matches 0 run scoreboard players set $unbreaking_lvl smithed.item -1

# if delta is positive (i.e. adding durability), ignore unbreaking
execute if score $delta smithed.item matches 1.. run scoreboard players set $unbreaking_lvl smithed.item 0

# damage the item, based on its unbreaking level
execute if score $unbreaking_lvl smithed.item matches 0 run function smithed.item:impl/durability/damage/force/sub
execute if score $unbreaking_lvl smithed.item matches 1 if predicate smithed.item:impl/chance/50 run function smithed.item:impl/durability/damage/force/sub
execute if score $unbreaking_lvl smithed.item matches 2 if predicate smithed.item:impl/chance/33 run function smithed.item:impl/durability/damage/force/sub
execute if score $unbreaking_lvl smithed.item matches 3 if predicate smithed.item:impl/chance/25 run function smithed.item:impl/durability/damage/force/sub
execute if score $unbreaking_lvl smithed.item matches 4 if predicate smithed.item:impl/chance/20 run function smithed.item:impl/durability/damage/force/sub
execute if score $unbreaking_lvl smithed.item matches 5 if predicate smithed.item:impl/chance/16 run function smithed.item:impl/durability/damage/force/sub
execute if score $unbreaking_lvl smithed.item matches 6 if predicate smithed.item:impl/chance/14 run function smithed.item:impl/durability/damage/force/sub
execute if score $unbreaking_lvl smithed.item matches 7 if predicate smithed.item:impl/chance/12 run function smithed.item:impl/durability/damage/force/sub
execute if score $unbreaking_lvl smithed.item matches 8 if predicate smithed.item:impl/chance/11 run function smithed.item:impl/durability/damage/force/sub
execute if score $unbreaking_lvl smithed.item matches 9 if predicate smithed.item:impl/chance/10 run function smithed.item:impl/durability/damage/force/sub
execute if score $unbreaking_lvl smithed.item matches 10.. if predicate smithed.item:impl/chance/9 run function smithed.item:impl/durability/damage/force/sub
