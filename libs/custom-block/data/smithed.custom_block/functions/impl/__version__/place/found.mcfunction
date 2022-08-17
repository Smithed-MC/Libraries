# @doc event/on_place
# When a player places down a custom block, the function tag `#smithed.custom_block:event/on_place` is run.
# To complete the placement of a custom block, a function must be added to this tag to verify the block id
# and run a function to complete the placement.
# 
# # Example Implementation
# function tag `#smithed.custom_block:event/on_place`
# ```json
# {
#   "values": [
#     "example:check_block"
#   ]
# }
# ```
# 
# function `example:check_block`
# ```mcfunction
# execute if data storage smithed.custom_block:main {blockApi:{id:"my_custom_block"}} run function example:place_block_1
# # multiple blocks can be checked in this same function if your data pack adds more than 1
# execute if data storage smithed.custom_block:main {blockApi:{id:"my_custom_block"}} run function example:place_block_2
# ```
# 
# function `example:place_block_1`
# ```mcfunction
# # the block MUST be replaced with another block, or have it's items cleared
# setblock ~ ~ ~ dropper{CustomName:'"Custom Block 1"'}
# summon armor_stand ~ ~ ~ {CustomName:'"my_custom_block_1"',Tags:["my_custom_block_1","smithed.entity","smithed.strict","smithed.block"],ArmorItems:[{},{},{},{id:"minecraft:gold_block",Count:1b,tag:{CustomModelData:1234567}}]}
# ```
# function `example:place_block_2`
# ```mcfunction
# # the block MUST be replaced with another block, or have it's items cleared
# data merge block ~ ~ ~ {CustomName:'"Custom Block 2"',Items:[]}
# summon armor_stand ~ ~ ~ {CustomName:'"my_custom_block_2"',Tags:["my_custom_block_2","smithed.entity","smithed.strict","smithed.block"],ArmorItems:[{},{},{},{id:"minecraft:gold_block",Count:1b,tag:{CustomModelData:1234567}}]}
# ```


# update the custom block
# @s = player who just placed a custom block item
# located at the center of the custom block that needs updating
# run from place/layer

data modify storage smithed.custom_block:main blockApi.id set from block ~ ~ ~ Items[0].tag.smithed.block.id 

data modify storage smithed.custom_block:main blockApi.__data set from block ~ ~ ~
function #smithed.custom_block:event/on_place

execute if block ~ ~ ~ #smithed.custom_block:placeable run function smithed.custom_block:impl/__version__/place/block_unchanged
