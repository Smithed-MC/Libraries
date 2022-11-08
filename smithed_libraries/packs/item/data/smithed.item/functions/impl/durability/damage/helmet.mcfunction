# @public

data modify storage smithed.item:main item set from entity @s Inventory[{Slot:103b}]

function smithed.item:impl/durability/damage/force

execute unless data storage smithed.item:main {item:"null"} unless score $out smithed.data matches -1 run item modify entity @s armor.head smithed.item:update_nbt
execute if data storage smithed.item:main {item:"null"} run item replace entity @s armor.head with air