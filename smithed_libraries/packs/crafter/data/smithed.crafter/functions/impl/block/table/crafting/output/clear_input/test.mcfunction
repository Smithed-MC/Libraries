

data remove entity @s HandItems[0]
scoreboard players set $temp smithed.data 0
data modify entity @s HandItems[0] set from block ~ ~ ~ Items[{Slot:2b}]
function smithed.crafter:impl/block/table/crafting/output/clear_input/advanced
execute if score $temp smithed.data matches 0 run item modify block ~ ~ ~ container.2 smithed.crafter:impl/remove_one
execute if score $temp smithed.data matches 1 run item replace block ~ ~ ~ container.2 from entity @s weapon.mainhand

data remove entity @s HandItems[0]
scoreboard players set $temp smithed.data 0
data modify entity @s HandItems[0] set from block ~ ~ ~ Items[{Slot:3b}]
function smithed.crafter:impl/block/table/crafting/output/clear_input/advanced
execute if score $temp smithed.data matches 0 run item modify block ~ ~ ~ container.3 smithed.crafter:impl/remove_one
execute if score $temp smithed.data matches 1 run item replace block ~ ~ ~ container.3 from entity @s weapon.mainhand

data remove entity @s HandItems[0]
scoreboard players set $temp smithed.data 0
data modify entity @s HandItems[0] set from block ~ ~ ~ Items[{Slot:4b}]
function smithed.crafter:impl/block/table/crafting/output/clear_input/advanced
execute if score $temp smithed.data matches 0 run item modify block ~ ~ ~ container.4 smithed.crafter:impl/remove_one
execute if score $temp smithed.data matches 1 run item replace block ~ ~ ~ container.4 from entity @s weapon.mainhand

data remove entity @s HandItems[0]
scoreboard players set $temp smithed.data 0
data modify entity @s HandItems[0] set from block ~ ~ ~ Items[{Slot:11b}]
function smithed.crafter:impl/block/table/crafting/output/clear_input/advanced
execute if score $temp smithed.data matches 0 run item modify block ~ ~ ~ container.11 smithed.crafter:impl/remove_one
execute if score $temp smithed.data matches 1 run item replace block ~ ~ ~ container.11 from entity @s weapon.mainhand

data remove entity @s HandItems[0]
scoreboard players set $temp smithed.data 0
data modify entity @s HandItems[0] set from block ~ ~ ~ Items[{Slot:12b}]
function smithed.crafter:impl/block/table/crafting/output/clear_input/advanced
execute if score $temp smithed.data matches 0 run item modify block ~ ~ ~ container.12 smithed.crafter:impl/remove_one
execute if score $temp smithed.data matches 1 run item replace block ~ ~ ~ container.12 from entity @s weapon.mainhand

data remove entity @s HandItems[0]
scoreboard players set $temp smithed.data 0
data modify entity @s HandItems[0] set from block ~ ~ ~ Items[{Slot:13b}]
function smithed.crafter:impl/block/table/crafting/output/clear_input/advanced
execute if score $temp smithed.data matches 0 run item modify block ~ ~ ~ container.13 smithed.crafter:impl/remove_one
execute if score $temp smithed.data matches 1 run item replace block ~ ~ ~ container.13 from entity @s weapon.mainhand

data remove entity @s HandItems[0]
scoreboard players set $temp smithed.data 0
data modify entity @s HandItems[0] set from block ~ ~ ~ Items[{Slot:20b}]
function smithed.crafter:impl/block/table/crafting/output/clear_input/advanced
execute if score $temp smithed.data matches 0 run item modify block ~ ~ ~ container.20 smithed.crafter:impl/remove_one
execute if score $temp smithed.data matches 1 run item replace block ~ ~ ~ container.20 from entity @s weapon.mainhand

data remove entity @s HandItems[0]
scoreboard players set $temp smithed.data 0
data modify entity @s HandItems[0] set from block ~ ~ ~ Items[{Slot:21b}]
function smithed.crafter:impl/block/table/crafting/output/clear_input/advanced
execute if score $temp smithed.data matches 0 run item modify block ~ ~ ~ container.21 smithed.crafter:impl/remove_one
execute if score $temp smithed.data matches 1 run item replace block ~ ~ ~ container.21 from entity @s weapon.mainhand

data remove entity @s HandItems[0]
scoreboard players set $temp smithed.data 0
data modify entity @s HandItems[0] set from block ~ ~ ~ Items[{Slot:22b}]
function smithed.crafter:impl/block/table/crafting/output/clear_input/advanced
execute if score $temp smithed.data matches 0 run item modify block ~ ~ ~ container.22 smithed.crafter:impl/remove_one
execute if score $temp smithed.data matches 1 run data modify block ~ ~ ~ Items[{Slot:22b}] set from entity @s HandItems[0]

data remove entity @s HandItems[0]
scoreboard players set $temp smithed.data 0