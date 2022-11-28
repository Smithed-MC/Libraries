scoreboard players operation $xp.temp smithed.data = @s smithed.xp
scoreboard players operation $xp.temp smithed.data -= @s smithed.prev_xp
scoreboard players operation $xp.temp smithed.data *= 2 smithed.const

execute if score $xp.temp smithed.data matches 1.. run function smithed.item:impl/durability/calc_mending/clamp
