execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if data storage smithed.crafter:main root.temp{crafting_input:{0:[{id:"minecraft:air",Slot:0b},{id:"minecraft:gold_ingot",Slot:1b},{id:"minecraft:air",Slot:2b}],1:[{id:"minecraft:gold_ingot",Slot:0b},{id:"minecraft:redstone",Slot:1b},{id:"minecraft:gold_ingot",Slot:2b}],2:[{id:"minecraft:air",Slot:0b},{id:"minecraft:gold_ingot",Slot:1b},{id:"minecraft:air",Slot:2b}]}} run item replace block ~ ~ ~ container.16 with minecraft:clock 1
execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if data storage smithed.crafter:main root.temp{crafting_input:{0:[{id:"minecraft:coal",Slot:0b},{id:"minecraft:coal",Slot:1b},{id:"minecraft:coal",Slot:2b}],1:[{id:"minecraft:coal",Slot:0b},{id:"minecraft:coal",Slot:1b},{id:"minecraft:coal",Slot:2b}],2:[{id:"minecraft:coal",Slot:0b},{id:"minecraft:coal",Slot:1b},{id:"minecraft:coal",Slot:2b}]}} run item replace block ~ ~ ~ container.16 with minecraft:coal_block 1
