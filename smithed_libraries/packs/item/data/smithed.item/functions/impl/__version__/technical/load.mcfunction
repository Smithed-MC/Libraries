forceload add -30000000 1600
setblock -30000000 0 1603 oak_sign
scoreboard objectives add smithed.data dummy

schedule function smithed.item:impl/__version__/technical/tick 1t replace