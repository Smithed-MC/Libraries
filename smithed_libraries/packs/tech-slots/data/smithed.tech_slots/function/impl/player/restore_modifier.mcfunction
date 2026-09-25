

$item modify entity @s armor.body $(modifier)
data remove storage smithed.tech_slots:data temp.current_modifiers[-1]
scoreboard players remove $modifier_count smithed.data 1
execute if score $modifier_count smithed.data matches 1.. run function smithed.tech_slots:impl/player/restore_modifier with storage smithed.tech_slots:data temp.current_modifiers[-1]
