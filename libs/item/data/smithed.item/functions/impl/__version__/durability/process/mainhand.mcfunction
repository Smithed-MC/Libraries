data modify storage smithed.damage:main item set from entity @s SelectedItem
function smithed.damage:impl/__version__/durability/process/handle

execute unless data storage smithed.damage:main {item:"null"} unless score $out smithed.data matches -1 run item modify entity @s weapon.mainhand smithed.damage:update_nbt
execute if data storage smithed.damage:main {item:"null"} run item replace entity @s weapon.mainhand with air