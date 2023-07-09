# waits until the item can be modified safely
# @s = none
# located at world spawn
# run from durability/track_changes/mark

execute as @a[tag=smithed.item.check] run function smithed.item:impl/durability/track_changes/check_durability
