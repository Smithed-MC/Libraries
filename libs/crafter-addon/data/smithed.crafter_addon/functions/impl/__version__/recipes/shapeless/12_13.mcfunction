execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if score count smithed.data matches 1 if data storage smithed.crafter:main root.temp{shapeless_crafting_input:[{id:"minecraft:blaze_rod"}]} run item replace block ~ ~ ~ container.16 with minecraft:blaze_powder 2
execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if score count smithed.data matches 2 if data storage smithed.crafter:main root.temp{shapeless_crafting_input:[{id:"minecraft:white_bed"},{id:"minecraft:blue_dye"}]} run item replace block ~ ~ ~ container.16 with minecraft:blue_bed 1
