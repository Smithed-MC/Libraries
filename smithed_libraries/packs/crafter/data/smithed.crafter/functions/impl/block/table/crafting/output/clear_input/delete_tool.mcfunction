

scoreboard players set $max_damage smithed.data 0
execute if data entity @s HandItems[0].components."minecraft:max_damage" store result score $max_damage smithed.data run data get entity @s HandItems[0].components."minecraft:max_damage"
execute if data entity @s HandItems[0].components."minecraft:max_damage" if score $temp1 smithed.data >= $max_damage smithed.data run function smithed.crafter:impl/block/table/crafting/output/clear_input/delete_tool/sub
execute unless data entity @s HandItems[0].components."minecraft:max_damage" run function smithed.crafter:impl/block/table/crafting/output/clear_input/delete_tool/vanilla


