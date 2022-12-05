# scoreboard players operation $temp smithed.damage = @s smithed.damage
# data merge storage smithed:log {message:'[{"score":{"name":"$temp","objective":"smithed.damage"}}]',level:1,type:'INFO'}
# function #smithed.damage:technical/tools/log
#!dbg score "$temp", "smithed.damage"

scoreboard players operation @s smithed.damage *= 100 smithed.const

# handle absorption
execute store result score $absorption smithed.damage run data get entity @s AbsorptionAmount 100
scoreboard players operation $absorption smithed.damage -= @s smithed.damage

execute if score $absorption smithed.damage matches ..0 run data remove entity @s AbsorptionAmount
execute if score $absorption smithed.damage matches 1..
    store result entity @s AbsorptionAmount float 0.01
    run scoreboard players get $absorption smithed.damage

scoreboard players operation @s smithed.damage += $absorption smithed.damage

execute if score $absorption smithed.damage matches ..0 function ./health:
    execute store result score $health smithed.damage run data get entity @s Health 100

    scoreboard players operation @s smithed.damage *= 100 smithed.const
    scoreboard players operation $health smithed.damage -= @s smithed.damage

    execute store result entity @s Health float 0.01 run scoreboard players get $health smithed.damage

    effect give @s[type=#smithed.damage:undead] instant_health 1 127 true
    effect give @s[type=!#smithed.damage:undead] instant_damage 1 127 true
