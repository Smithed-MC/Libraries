advancement revoke @s only smithed:actionbar/__version__/vanilla/used_bed requirement

scoreboard players set @s smithed.actionbar.priority 1
scoreboard players set @s smithed.actionbar.freeze 20
scoreboard players set @s[advancements={smithed:actionbar/__version__/vanilla/slept_in_bed={requirement=true}}] smithed.actionbar.sleeping 1

execute if score @s smithed.actionbar.sleeping matches 1.. run schedule function smithed:actionbar/__version__/vanilla/tick 1t replace 

advancement revoke @s only smithed:actionbar/__version__/vanilla/slept_in_bed requirement
