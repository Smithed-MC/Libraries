# place an item in the body slot
function smithed.tech_slots:impl/player/set_body_item

# get player storage entry
execute store result score $modifier_count smithed.data run function smithed.tech_slots:impl/storage/load_player with entity @s
execute if score $modifier_count smithed.data matches 0 run return run data remove storage smithed.tech_slots:data temp

# restore modifiers
function smithed.tech_slots:impl/player/restore_modifier with storage smithed.tech_slots:data temp.current_modifiers[-1]

# allow other packs to run custom functionality
function #smithed.tech_slots:player/restore_modifiers
data remove storage smithed.tech_slots:data temp
