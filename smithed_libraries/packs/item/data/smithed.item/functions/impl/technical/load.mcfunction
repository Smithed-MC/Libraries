forceload add -30000000 1600
setblock -30000000 0 1603 oak_sign
scoreboard objectives add smithed.item dummy
scoreboard players set $delta smithed.item -1

scoreboard objectives add smithed.const dummy
scoreboard players set 16 smithed.const 16
scoreboard players set 2 smithed.const 2
scoreboard players set 0 smithed.const 0

scoreboard objectives add smithed.xp xp
scoreboard objectives add smithed.item.prev_xp dummy

#declare storage smithed.item:main
