scoreboard objectives add smithed.data dummy
scoreboard objectives add smithed.enchanter.seed dummy

execute store result score #lcg_x smithed.data run seed
scoreboard players set #lcg_a smithed.data 1630111353
scoreboard players set #lcg_c smithed.data 1623164762
scoreboard players set #lcg_m smithed.data 2147483647


schedule function ./tick 1t replace