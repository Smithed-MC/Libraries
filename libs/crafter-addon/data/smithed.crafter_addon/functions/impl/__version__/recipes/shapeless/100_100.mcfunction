execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if score count smithed.data matches 2 if data storage smithed.crafter:main root.temp{shapeless_crafting_input:[{id:"minecraft:cobblestone"},{id:"minecraft:moss_block"}]} run item replace block ~ ~ ~ container.16 with minecraft:mossy_cobblestone 1
