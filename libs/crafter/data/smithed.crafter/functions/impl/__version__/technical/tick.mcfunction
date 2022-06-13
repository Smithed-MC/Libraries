execute as @e[type=armor_stand,tag=smithed.crafter] at @s run function smithed.crafter:impl/__version__/block/table/tick

schedule function smithed.crafter:impl/__version__/technical/tick 1t replace
