data modify storage smithed.damage: item set from entity @s Inventory[{Slot:101b}]
function smithed.damage:impl/__version__/durability/process/handle

execute unless data storage smithed.damage: {item:"null"} unless score $out smithed.data matches -1 run item modify entity @s armor.legs smithed.damage:update_nbt
execute if data storage smithed.damage: {item:"null"} run item replace entity @s armor.legs with air