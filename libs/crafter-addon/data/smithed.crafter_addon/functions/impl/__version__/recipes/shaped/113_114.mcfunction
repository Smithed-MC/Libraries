execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if data storage smithed.crafter:main root.temp{crafting_input:{0:[{id:"minecraft:stick",Slot:0b},{id:"minecraft:iron_ingot",Slot:1b},{id:"minecraft:stick",Slot:2b}],1:[{id:"minecraft:string",Slot:0b},{id:"minecraft:tripwire_hook",Slot:1b},{id:"minecraft:string",Slot:2b}],2:[{id:"minecraft:air",Slot:0b},{id:"minecraft:stick",Slot:1b},{id:"minecraft:air",Slot:2b}]}} run item replace block ~ ~ ~ container.16 with minecraft:crossbow 1
execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if data storage smithed.crafter:main root.temp{crafting_input:{0:[{id:"minecraft:copper_block",Slot:0b},{id:"minecraft:copper_block",Slot:1b},{id:"minecraft:air",Slot:2b}],1:[{id:"minecraft:copper_block",Slot:0b},{id:"minecraft:copper_block",Slot:1b},{id:"minecraft:air",Slot:2b}]}} if data storage smithed.crafter:main root.temp{crafting_input:{2:[]}} run item replace block ~ ~ ~ container.16 with minecraft:cut_copper 4
