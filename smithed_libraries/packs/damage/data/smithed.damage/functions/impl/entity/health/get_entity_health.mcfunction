execute store result score $maximumHealth smithed.damage run data get entity @s Health
execute store result score $absorptionHealth smithed.damage run data get entity @s AbsorptionAmount
scoreboard players operation $maximumHealth smithed.damage += $absorptionHealth smithed.damage
