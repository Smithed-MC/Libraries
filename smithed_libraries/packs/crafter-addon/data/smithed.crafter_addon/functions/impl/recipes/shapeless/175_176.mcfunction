execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if score count smithed.data matches 1 if data storage smithed.crafter:main root.temp{shapeless_crafting_input:[{id:"minecraft:lily_of_the_valley"}]} run item replace block ~ ~ ~ container.16 with minecraft:white_dye 1
execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if score count smithed.data matches 3 if data storage smithed.crafter:main root.temp{shapeless_crafting_input:[{id:"minecraft:book"},{id:"minecraft:ink_sac"},{id:"minecraft:feather"}]} run item replace block ~ ~ ~ container.16 with minecraft:writable_book 1