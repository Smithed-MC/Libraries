execute unless data storage smithed.crafter:input {flags:["consume_buckets"]} if predicate smithed.crafter:block/table/special_clear/buckets run function smithed.crafter:impl/block/table/crafting/output/clear_input/advanced/buckets
# if the item is a tool, not unbreakable and does not have not_tool:1b
execute 
    unless data storage smithed.crafter:input {flags:["consume_tools"]} 
    if items entity @s weapon.mainhand *[minecraft:max_damage,!minecraft:unbreakable,!minecraft:custom_data~{smithed:{not_tool:1b}}] 
    run function smithed.crafter:impl/block/table/crafting/output/clear_input/handle_tools
function #smithed.crafter:event/advanced_remove
