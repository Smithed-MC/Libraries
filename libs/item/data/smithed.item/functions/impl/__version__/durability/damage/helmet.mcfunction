# @public

data modify storage smithed.damage: item set from entity @s Inventory[{Slot:103b}]

function smithed.damage:impl/__version__/durability/damage/force

execute unless data storage smithed.damage: {item:"null"} unless score $out smithed.data matches -1 run item modify entity @s armor.head smithed.damage:update_nbt
execute if data storage smithed.damage: {item:"null"} run item replace entity @s armor.head with air