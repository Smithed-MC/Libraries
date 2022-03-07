####################
# Mirrors the recipes
####################

data modify storage smithed.crafter:main root.temp.crafting_input_temp set value [[{id:"minecraft:air"},{id:"minecraft:air"},{id:"minecraft:air"}],[{id:"minecraft:air"},{id:"minecraft:air"},{id:"minecraft:air"}],[{id:"minecraft:air"},{id:"minecraft:air"},{id:"minecraft:air"}]]

execute unless data storage smithed.crafter:main root.temp.crafting_input{0:[{id:"minecraft:air",Slot:0b}]} if data storage smithed.crafter:main root.temp.crafting_input{0:[{Slot:0b}]} run data modify storage smithed.crafter:main root.temp.crafting_input_temp[0][2] set from storage smithed.crafter:main root.temp.crafting_input.0[{Slot:0b}]
execute unless data storage smithed.crafter:main root.temp.crafting_input{0:[{id:"minecraft:air",Slot:1b}]} if data storage smithed.crafter:main root.temp.crafting_input{0:[{Slot:1b}]} run data modify storage smithed.crafter:main root.temp.crafting_input_temp[0][1] set from storage smithed.crafter:main root.temp.crafting_input.0[{Slot:1b}]
execute unless data storage smithed.crafter:main root.temp.crafting_input{0:[{id:"minecraft:air",Slot:2b}]} if data storage smithed.crafter:main root.temp.crafting_input{0:[{Slot:2b}]} run data modify storage smithed.crafter:main root.temp.crafting_input_temp[0][0] set from storage smithed.crafter:main root.temp.crafting_input.0[{Slot:2b}]
execute unless data storage smithed.crafter:main root.temp.crafting_input{1:[{id:"minecraft:air",Slot:0b}]} if data storage smithed.crafter:main root.temp.crafting_input{1:[{Slot:0b}]} run data modify storage smithed.crafter:main root.temp.crafting_input_temp[1][2] set from storage smithed.crafter:main root.temp.crafting_input.1[{Slot:0b}]
execute unless data storage smithed.crafter:main root.temp.crafting_input{1:[{id:"minecraft:air",Slot:1b}]} if data storage smithed.crafter:main root.temp.crafting_input{1:[{Slot:1b}]} run data modify storage smithed.crafter:main root.temp.crafting_input_temp[1][1] set from storage smithed.crafter:main root.temp.crafting_input.1[{Slot:1b}]
execute unless data storage smithed.crafter:main root.temp.crafting_input{1:[{id:"minecraft:air",Slot:2b}]} if data storage smithed.crafter:main root.temp.crafting_input{1:[{Slot:2b}]} run data modify storage smithed.crafter:main root.temp.crafting_input_temp[1][0] set from storage smithed.crafter:main root.temp.crafting_input.1[{Slot:2b}]
execute unless data storage smithed.crafter:main root.temp.crafting_input{2:[{id:"minecraft:air",Slot:0b}]} if data storage smithed.crafter:main root.temp.crafting_input{2:[{Slot:0b}]} run data modify storage smithed.crafter:main root.temp.crafting_input_temp[2][2] set from storage smithed.crafter:main root.temp.crafting_input.2[{Slot:0b}]
execute unless data storage smithed.crafter:main root.temp.crafting_input{2:[{id:"minecraft:air",Slot:1b}]} if data storage smithed.crafter:main root.temp.crafting_input{2:[{Slot:1b}]} run data modify storage smithed.crafter:main root.temp.crafting_input_temp[2][1] set from storage smithed.crafter:main root.temp.crafting_input.2[{Slot:1b}]
execute unless data storage smithed.crafter:main root.temp.crafting_input{2:[{id:"minecraft:air",Slot:2b}]} if data storage smithed.crafter:main root.temp.crafting_input{2:[{Slot:2b}]} run data modify storage smithed.crafter:main root.temp.crafting_input_temp[2][0] set from storage smithed.crafter:main root.temp.crafting_input.2[{Slot:2b}]

function smithed.crafter:impl/__version__/block/table/crafting/input/process
function smithed.crafter:impl/__version__/block/table/crafting/recipes
