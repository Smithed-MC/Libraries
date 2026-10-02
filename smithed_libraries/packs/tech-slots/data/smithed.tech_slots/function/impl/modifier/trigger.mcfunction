# @public

# disable command feedback
execute if function smithed.tech_slots:impl/technical/get_send_command_feedback run gamerule send_command_feedback false

# toggle gamemode (and re-enable command feedback)
execute if entity @s[gamemode=survival] run return run function smithed.tech_slots:impl/modifier/gamemode/survival
execute if entity @s[gamemode=adventure] run return run function smithed.tech_slots:impl/modifier/gamemode/adventure
execute if entity @s[gamemode=creative] run return run function smithed.tech_slots:impl/modifier/gamemode/creative
execute if entity @s[gamemode=spectator] run function smithed.tech_slots:impl/modifier/gamemode/spectator
