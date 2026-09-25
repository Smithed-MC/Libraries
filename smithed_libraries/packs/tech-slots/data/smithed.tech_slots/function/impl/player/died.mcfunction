advancement revoke @s only smithed.tech_slots:impl/death
scoreboard players reset @s smithed.tech_slots.death
execute unless function smithed.tech_slots:impl/technical/get_keep_inventory run advancement revoke @s only smithed.tech_slots:impl/respawn
