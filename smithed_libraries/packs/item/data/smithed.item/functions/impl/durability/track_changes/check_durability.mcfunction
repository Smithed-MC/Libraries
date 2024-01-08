# checks player for items custom durability
# @s = player who had a custom durability item change durability
# located at world spawn
# run from durability/track_changes/wait

# for each custom item, check what changed
data modify storage smithed.item:main player set from entity @s {}
execute if predicate smithed.item:impl/has_custom_durability/mainhand run function smithed.item:impl/durability/track_changes/process/mainhand
execute if predicate smithed.item:impl/has_custom_durability/offhand run function smithed.item:impl/durability/track_changes/process/offhand
execute if predicate smithed.item:impl/has_custom_durability/head run function smithed.item:impl/durability/track_changes/process/head
execute if predicate smithed.item:impl/has_custom_durability/chest run function smithed.item:impl/durability/track_changes/process/chest
execute if predicate smithed.item:impl/has_custom_durability/legs run function smithed.item:impl/durability/track_changes/process/legs
execute if predicate smithed.item:impl/has_custom_durability/feet run function smithed.item:impl/durability/track_changes/process/feet

# mark as done with durability changes
tag @s remove smithed.item.check
advancement revoke @s only smithed.item:impl/inventory_changed
