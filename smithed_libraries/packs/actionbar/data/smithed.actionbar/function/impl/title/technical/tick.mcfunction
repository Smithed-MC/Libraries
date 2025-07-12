# loop every tick
schedule function smithed.actionbar:impl/title/technical/tick 1t replace

# reset scores when at 1
execute as @a[scores={smithed.title.freeze=1}] run function smithed.actionbar:impl/title/reset

# decrement everyone's score
scoreboard players remove @a[scores={smithed.title.freeze=1..}] smithed.title.freeze 1

# reset sneak_time score
scoreboard players reset @a smithed.title.sneaking
