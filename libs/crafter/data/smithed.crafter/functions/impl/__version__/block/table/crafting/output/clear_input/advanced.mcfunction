execute unless data storage smithed.crafter:main {flags:["consume_buckets"]} if predicate smithed.crafter:block/table/special_clear/buckets store success score $temp smithed.data run function smithed.crafter:impl/__version__/block/table/crafting/output/clear_input/advanced/buckets
execute unless data storage smithed.crafter:main {flags:["consume_tools"]} if predicate smithed.crafter:block/table/special_clear/tools unless data entity @s {HandItems:[{tag:{Unbreakable:1b}}]} run function smithed.crafter:impl/__version__/block/table/crafting/output/clear_input/handle_tools

function #smithed.crafter:events/advanced_remove
