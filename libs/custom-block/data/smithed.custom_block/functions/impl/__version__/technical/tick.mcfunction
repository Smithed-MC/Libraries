execute as @a at @s run function smithed.custom_block:impl/__version__/player/tick

execute as @e[type=#smithed.custom_block:ticking] at @s run function smithed.custom_block:impl/__version__/technical/entity_tick

schedule function smithed.custom_block:impl/__version__/technical/tick 1t replace
