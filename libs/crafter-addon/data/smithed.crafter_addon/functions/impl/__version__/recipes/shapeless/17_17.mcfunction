execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if score count smithed.data matches 1 if data storage smithed.crafter:main root.temp{shapeless_crafting_input:[{id:"minecraft:cornflower"}]} run item replace block ~ ~ ~ container.16 with minecraft:blue_dye 1
