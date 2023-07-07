data modify storage smithed.custom_block:main blockApi set from block ~ ~ ~ Items[0].tag.smithed.block

data modify storage smithed.custom_block:main blockApi.__data set from block ~ ~ ~
function #smithed.custom_block:event/on_place

execute if block ~ ~ ~ #smithed.custom_block:placeable run function smithed.custom_block:impl/place/block_unchanged
