execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if score count smithed.data matches 2 if data storage smithed.crafter:main root.temp{shapeless_crafting_input:[{id:"minecraft:blue_dye"},{id:"minecraft:white_wool"}]} run item replace block ~ ~ ~ container.16 with minecraft:blue_wool 1
execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if score count smithed.data matches 1 if data storage smithed.crafter:main root.temp{shapeless_crafting_input:[{id:"minecraft:bone"}]} run item replace block ~ ~ ~ container.16 with minecraft:bone_meal 3
