scoreboard players set $temp1 smithed.data 0

execute unless data entity @s {HandItems:[{components:{"minecraft:damage":0}}]} store result score $temp1 smithed.data run data get entity @s HandItems[0].components."minecraft:damage"
execute unless data entity @s {HandItems:[{components:{"minecraft:damage":0}}]} store success score $temp smithed.data store result entity @s HandItems[0].components."minecraft:damage" int 1 run scoreboard players add $temp1 smithed.data 1
execute if data entity @s {HandItems:[{components:{"minecraft:damage":0}}]} store success score $temp smithed.data run data modify entity @s HandItems[0].components."minecraft:damage" set value 1




function smithed.crafter:impl/block/table/crafting/output/clear_input/delete_tool

