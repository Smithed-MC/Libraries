execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if data storage smithed.crafter:main root.temp{crafting_input:{0:[{id:"minecraft:stripped_dark_oak_log",Slot:0b},{id:"minecraft:stripped_dark_oak_log",Slot:1b},{id:"minecraft:air",Slot:2b}],1:[{id:"minecraft:stripped_dark_oak_log",Slot:0b},{id:"minecraft:stripped_dark_oak_log",Slot:1b},{id:"minecraft:air",Slot:2b}]}} if data storage smithed.crafter:main root.temp{crafting_input:{2:[]}} run item replace block ~ ~ ~ container.16 with minecraft:stripped_dark_oak_wood 3
execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if data storage smithed.crafter:main root.temp{crafting_input:{0:[{id:"minecraft:stripped_jungle_log",Slot:0b},{id:"minecraft:stripped_jungle_log",Slot:1b},{id:"minecraft:air",Slot:2b}],1:[{id:"minecraft:stripped_jungle_log",Slot:0b},{id:"minecraft:stripped_jungle_log",Slot:1b},{id:"minecraft:air",Slot:2b}]}} if data storage smithed.crafter:main root.temp{crafting_input:{2:[]}} run item replace block ~ ~ ~ container.16 with minecraft:stripped_jungle_wood 3
