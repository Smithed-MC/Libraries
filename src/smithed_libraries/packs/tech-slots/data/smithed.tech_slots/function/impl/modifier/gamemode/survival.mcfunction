# toggle gamemode
gamemode spectator
gamemode survival

# restore command feedback
execute if score $send_command_feedback smithed.data matches 1 run gamerule send_command_feedback true
