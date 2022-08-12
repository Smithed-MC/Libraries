# check if the player entered the bed
tag @s[advancements={smithed.actionbar:impl/__version__/vanilla/bed/clicked_bed={occupied=true}}] add smithed.actionbar.occupied
tag @s[advancements={smithed.actionbar:impl/__version__/vanilla/bed/slept_in_bed={requirement=true}}] add smithed.actionbar.sleeping

advancement revoke @s only smithed.actionbar:impl/__version__/vanilla/bed/clicked_bed
advancement revoke @s only smithed.actionbar:impl/__version__/vanilla/bed/slept_in_bed

# if the player isn't in the bed, check why
execute if entity @s[tag=!smithed.actionbar.sleeping] run function smithed.actionbar:impl/__version__/vanilla/bed/sleep_issues/check

# else send sleeping message
# execute if entity @s[tag=smithed.actionbar.sleeping] run schedule function smithed.actionbar:__version__/vanilla/tick 1t replace 

# clean up
tag @s remove smithed.actionbar.occupied
tag @s remove smithed.actionbar.sleeping
