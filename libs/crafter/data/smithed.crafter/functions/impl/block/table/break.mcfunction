data modify storage smithed:crafter temp.output_item set from entity @s ArmorItems[3].tag.smithed.stored_output
data remove storage smithed:crafter temp.output_item.Slot
execute if data entity @s ArmorItems[3].tag.smithed.stored_output.id as @e[type=item,sort=nearest,distance=..2,tag=!global.ignore,tag=!global.ignore.kill] run function smithed.crafter:impl/__version__/block/table/break/delete_output

execute if entity @e[type=item,nbt={Item:{id:"minecraft:barrel",Count:1b}},limit=1,sort=nearest,distance=..3] run function smithed.crafter:impl/__version__/block/table/break/drop_item
kill @s