# @public

data modify storage smithed.damage:main item set from entity @s Inventory[{Slot:101b}]

function smithed.damage:impl/__version__/durability/damage/force

execute unless data storage smithed.damage:main {item:"null"} unless score $out smithed.data matches -1 run item modify entity @s armor.legs smithed.damage:update_nbt
execute if data storage smithed.damage:main {item:"null"} run item replace entity @s armor.legs with air