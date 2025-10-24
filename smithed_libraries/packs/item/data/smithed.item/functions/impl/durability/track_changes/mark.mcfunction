# prepare the player for damage calculations
# @s = player who has a custom durability item that changed durability
# located at world spawn
# run from advancement inventory_changed

# mark player for durability checks
tag @s add smithed.item.check
schedule function smithed.item:impl/durability/track_changes/wait 1
