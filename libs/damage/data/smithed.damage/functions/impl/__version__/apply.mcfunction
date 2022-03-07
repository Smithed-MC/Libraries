# @public

execute if entity @s[type=player] run function smithed.damage:impl/__version__/entity/damage/health/calculate_modifier
execute if entity @s[type=!player] run function smithed.damage:impl/__version__/entity/damage/health/get_entity_health

execute if score @s smithed.damage >= $maximumHealth smithed.damage run function smithed.damage:impl/__version__/entity/damage/on_death
execute if score @s smithed.damage < $maximumHealth smithed.damage run function smithed.damage:impl/__version__/entity/damage/health/update
scoreboard players reset @s smithed.damage
