execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if score count smithed.data matches 2 if data storage smithed.crafter:main root.temp{shapeless_crafting_input:[{id:"minecraft:red_dye"},{id:"minecraft:yellow_dye"}]} run item replace block ~ ~ ~ container.16 with minecraft:orange_dye 2
execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if score count smithed.data matches 2 if data storage smithed.crafter:main root.temp{shapeless_crafting_input:[{id:"minecraft:orange_dye"},{id:"minecraft:white_wool"}]} run item replace block ~ ~ ~ container.16 with minecraft:orange_wool 1