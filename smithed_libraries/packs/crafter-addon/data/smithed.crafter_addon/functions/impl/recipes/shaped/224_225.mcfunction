execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if data storage smithed.crafter:main root.temp{crafting_input:{0:[{id:"minecraft:wheat",Slot:0b},{id:"minecraft:wheat",Slot:1b},{id:"minecraft:wheat",Slot:2b}],1:[{id:"minecraft:wheat",Slot:0b},{id:"minecraft:wheat",Slot:1b},{id:"minecraft:wheat",Slot:2b}],2:[{id:"minecraft:wheat",Slot:0b},{id:"minecraft:wheat",Slot:1b},{id:"minecraft:wheat",Slot:2b}]}} run item replace block ~ ~ ~ container.16 with minecraft:hay_block 1
execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if data storage smithed.crafter:main root.temp{crafting_input:{0:[{id:"minecraft:iron_ingot",Slot:0b},{id:"minecraft:iron_ingot",Slot:1b},{id:"minecraft:air",Slot:2b}]}} if data storage smithed.crafter:main root.temp{crafting_input:{1:[],2:[]}} run item replace block ~ ~ ~ container.16 with minecraft:heavy_weighted_pressure_plate 1