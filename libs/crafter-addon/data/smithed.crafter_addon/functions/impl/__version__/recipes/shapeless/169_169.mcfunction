execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if score count smithed.data matches 2 if data storage smithed.crafter:main root.temp{shapeless_crafting_input:[{id:"minecraft:weathered_cut_copper_slab"},{id:"minecraft:honeycomb"}]} run item replace block ~ ~ ~ container.16 with minecraft:waxed_weathered_cut_copper_slab 1
