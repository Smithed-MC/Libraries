execute if entity @s[type=player] run function smithed.damage:impl/entity/health/update_player
execute if entity @s[type=!player] run function smithed.damage:impl/entity/health/update_entity
