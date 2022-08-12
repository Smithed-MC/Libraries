scoreboard players set $resolved_sleep smithed.actionbar.temp 0

# check occupied
execute if score $resolved_sleep smithed.actionbar.temp matches 0 store result score $resolved_sleep smithed.actionbar.temp if entity @s[tag=smithed.actionbar.occupied] if block ~ ~ ~ #minecraft:beds[occupied=true] run data modify storage smithed.actionbar:input message set value {json:'{"translate":"block.minecraft.bed.occupied","color":"yellow"}',priority:'notification',freeze:10}

# check distance
execute if score $resolved_sleep smithed.actionbar.temp matches 0 run function smithed.actionbar:impl/__version__/vanilla/bed/sleep_issues/distance_check

# check obstructed
execute if score $resolved_sleep smithed.actionbar.temp matches 0 run function smithed.actionbar:impl/__version__/vanilla/bed/sleep_issues/obstruction_check

# check time
execute if score $resolved_sleep smithed.actionbar.temp matches 0 store result score $resolved_sleep smithed.actionbar.temp if predicate smithed.actionbar:__version__/vanilla/is_night run data modify storage smithed.actionbar:input message set value {json:'{"translate":"block.minecraft.bed.no_sleep","color":"yellow"}',priority:'notification',freeze:10}

# check monsters
execute if score $resolved_sleep smithed.actionbar.temp matches 0 store result score $resolved_sleep smithed.actionbar.temp if entity @s[gamemode=!creative] positioned ~-8 ~-5 ~-8 if entity @e[predicate=smithed.actionbar:__version__/vanilla/prevents_sleep,dx=16,dy=10,dz=16,limit=1] run data modify storage smithed.actionbar:input message set value {json:'{"translate":"block.minecraft.bed.not_safe","color":"yellow"}',priority:'notification',freeze:10}

# display message
function #smithed.actionbar:message
