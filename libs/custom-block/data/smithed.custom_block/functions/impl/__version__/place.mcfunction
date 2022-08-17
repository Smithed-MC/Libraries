# @doc item/custom_block
# To create a custom block, the item the player places down needs some special nbt.  
# Custom blocks can be any of the following items by default:
# * furnace
# * blast_furnace
# * smoker
# * barrel
# * dispenser
# * dropper
# * campfire
# * soul_campfire
# 
# The container block used as the custom block item must have a `BlockEntityTag` which
# sets the first (and only) slot of the `Items` to an item with the nbt `smithed:{block:{id:\"INDICATOR\""}}`.
# Note that the block itself does not need to be the same block, but the item must be one of these container blocks.
# 
# ## Example Loot Table:
# ```json
# {
#   "pools": [
#     {
#       "rolls": 1,
#       "entries": [
#         {
#           "type": "minecraft:item",
#           "name": "minecraft:furnace",
#           "functions": [
#             {
#               "function": "minecraft:set_nbt",
#               "tag": "{display:{Name:'"Custom Block"'},BlockEntityTag:{Items:[{Slot:0b,id:\"minecraft:stick\",Count:1b,tag:{smithed:{block:{id:\"my_custom_block\"}}}}]}}"
#             }
#           ]
#         }
#       ]
#     }
#   ]
# }
# ```
# 
# ## Additional Items
# If you want to use a container for the item, but it's not supported by default, you can create a loot table under 
# `smithed.custom_block:blocks/placeable` with `"replace": false` to add the item.
# Note that the block must be a container block.
# ### Example:
# loot table `smithed.custom_block:blocks/placeable`
# ```json
# {
#   "replace": false,
#   "values": [
#     "minecraft:chest",
#     "minecraft:shulker_box"
#   ]
# }


# find the custom block placed by the player
# @s = player who just placed down a custom block item
# located at @s
# run from advancement technical/place_custom_block

advancement revoke @s only smithed.custom_block:impl/__version__/technical/place_custom_block

execute align xyz positioned ~0.5 ~-6.5 ~0.5 run function smithed.custom_block:impl/__version__/place/layer
execute align xyz positioned ~0.5 ~-5.5 ~0.5 run function smithed.custom_block:impl/__version__/place/layer
execute align xyz positioned ~0.5 ~-4.5 ~0.5 run function smithed.custom_block:impl/__version__/place/layer
execute align xyz positioned ~0.5 ~-3.5 ~0.5 run function smithed.custom_block:impl/__version__/place/layer
execute align xyz positioned ~0.5 ~-2.5 ~0.5 run function smithed.custom_block:impl/__version__/place/layer
execute align xyz positioned ~0.5 ~-1.5 ~0.5 run function smithed.custom_block:impl/__version__/place/layer
execute align xyz positioned ~0.5 ~-0.5 ~0.5 run function smithed.custom_block:impl/__version__/place/layer
execute align xyz positioned ~0.5 ~0.5 ~0.5 run function smithed.custom_block:impl/__version__/place/layer
execute align xyz positioned ~0.5 ~1.5 ~0.5 run function smithed.custom_block:impl/__version__/place/layer
execute align xyz positioned ~0.5 ~2.5 ~0.5 run function smithed.custom_block:impl/__version__/place/layer
execute align xyz positioned ~0.5 ~3.5 ~0.5 run function smithed.custom_block:impl/__version__/place/layer
execute align xyz positioned ~0.5 ~4.5 ~0.5 run function smithed.custom_block:impl/__version__/place/layer
execute align xyz positioned ~0.5 ~5.5 ~0.5 run function smithed.custom_block:impl/__version__/place/layer
execute align xyz positioned ~0.5 ~6.5 ~0.5 run function smithed.custom_block:impl/__version__/place/layer
