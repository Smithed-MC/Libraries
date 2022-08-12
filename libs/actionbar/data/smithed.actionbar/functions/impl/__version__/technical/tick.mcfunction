# reset scores when at 1
execute as @a[scores={smithed.actionbar.freeze=1}] run function smithed.actionbar:impl/__version__/reset

# decrement everyone's score
scoreboard players remove @a[scores={smithed.actionbar.freeze=1..}] smithed.actionbar.freeze 1

# reset sneak_time score
scoreboard players reset @a smithed.actionbar.sneaking

# loop every tick
schedule function smithed.actionbar:impl/__version__/technical/tick 1t replace
