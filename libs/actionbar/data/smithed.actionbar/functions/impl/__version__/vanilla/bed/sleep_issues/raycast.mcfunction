execute if block ~ ~ ~ #minecraft:beds align xyz positioned ~0.5 ~ ~0.5 run function smithed.actionbar:impl/__version__/vanilla/bed/sleep_issues/check_location

# loop until bed is found
scoreboard players remove $ray smithed.actionbar.temp 1
execute unless block ~ ~ ~ #minecraft:beds if score $ray smithed.actionbar.temp matches 1.. positioned ^ ^ ^0.1 run function smithed.actionbar:impl/__version__/vanilla/bed/sleep_issues/raycast
