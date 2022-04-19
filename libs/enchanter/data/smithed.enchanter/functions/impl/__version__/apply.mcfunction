# @public

execute if entity @s[type=player] run function smithed.damage:impl/__version__/entity/health/calculate_modifier
execute if entity @s[type=!player] run function smithed.damage:impl/__version__/entity/health/get_entity_health

execute if score @s smithed.damage >= $maximumHealth smithed.damage run function smithed.damage:impl/__version__/entity/on_death
execute if score @s smithed.damage < $maximumHealth smithed.damage run function smithed.damage:impl/__version__/entity/health/update
scoreboard players reset @s smithed.damage
