execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if data storage smithed.crafter:main root.temp{crafting_input:{0:[{item_tag:["#smithed:red_sandstone"],Slot:0b},{item_tag:["#smithed:red_sandstone"],Slot:1b},{item_tag:["#smithed:red_sandstone"],Slot:2b}]}} if data storage smithed.crafter:main root.temp{crafting_input:{1:[],2:[]}} run item replace block ~ ~ ~ container.16 with minecraft:red_sandstone_slab 6
execute store result score @s smithed.data if entity @s[scores={smithed.data=0}] if data storage smithed.crafter:main root.temp{crafting_input:{0:[{item_tag:["#smithed:red_sandstone_and_cut"],Slot:0b},{id:"minecraft:air",Slot:1b},{id:"minecraft:air",Slot:2b}],1:[{item_tag:["#smithed:red_sandstone_and_cut"],Slot:0b},{item_tag:["#smithed:red_sandstone_and_cut"],Slot:1b},{id:"minecraft:air",Slot:2b}],2:[{item_tag:["#smithed:red_sandstone_and_cut"],Slot:0b},{item_tag:["#smithed:red_sandstone_and_cut"],Slot:1b},{item_tag:["#smithed:red_sandstone_and_cut"],Slot:2b}]}} run item replace block ~ ~ ~ container.16 with minecraft:red_sandstone_stairs 4
