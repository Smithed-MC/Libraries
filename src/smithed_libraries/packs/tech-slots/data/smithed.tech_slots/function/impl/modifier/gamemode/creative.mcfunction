# check if player needs to be set back to flying
execute if predicate {condition:"minecraft:entity_properties",entity:"this",predicate:{flags:{is_flying:0b}}} run tag @s add smithed.tech_slots.no_fly

# toggle gamemode
gamemode spectator
gamemode adventure @s[tag=smithed.tech_slots.no_fly]
gamemode creative
tag @s[tag=smithed.tech_slots.no_fly] remove smithed.tech_slots.no_fly

# restore command feedback
execute if score $send_command_feedback smithed.data matches 1 run gamerule send_command_feedback true
