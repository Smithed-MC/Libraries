execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if data storage smithed.crafter:main root.temp{crafting_input:{0:[{id:"minecraft:red_nether_bricks",Slot:0b},{id:"minecraft:red_nether_bricks",Slot:1b},{id:"minecraft:red_nether_bricks",Slot:2b}],1:[{id:"minecraft:red_nether_bricks",Slot:0b},{id:"minecraft:red_nether_bricks",Slot:1b},{id:"minecraft:red_nether_bricks",Slot:2b}]}} if data storage smithed.crafter:main root.temp{crafting_input:{2:[]}} run item replace block ~ ~ ~ container.16 with minecraft:red_nether_brick_wall 6
execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if data storage smithed.crafter:main root.temp{crafting_input:{0:[{id:"minecraft:red_sand",Slot:0b},{id:"minecraft:red_sand",Slot:1b},{id:"minecraft:air",Slot:2b}],1:[{id:"minecraft:red_sand",Slot:0b},{id:"minecraft:red_sand",Slot:1b},{id:"minecraft:air",Slot:2b}]}} if data storage smithed.crafter:main root.temp{crafting_input:{2:[]}} run item replace block ~ ~ ~ container.16 with minecraft:red_sandstone 1
