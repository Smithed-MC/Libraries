####################
# Commands to run when the output is changed
####################

tag @s remove smithed.no_shift_click
execute if data entity @s ArmorItems[3].components."minecraft:custom_data".smithed.stored_output.id run function smithed.crafter:impl/block/table/crafting/manage_invalids/export_output
execute if entity @s[tag=smithed.crafter.assembled_output] run function smithed.crafter:impl/block/table/crafting/output/clear_input
