execute as @a at @s run function smithed.custom_block:impl/player/tick

#/ execute as @e[type=#smithed.custom_block:ticking] at @s run function smithed.custom_block:impl/technical/entity_tick

schedule function smithed.custom_block:impl/technical/tick 1t replace

