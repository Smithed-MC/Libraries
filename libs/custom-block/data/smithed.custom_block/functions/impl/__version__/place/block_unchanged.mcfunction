execute store success score $temp smithed.data run data modify storage smithed.custom_block: blockApi.__data set from block ~ ~ ~

execute if score $temp smithed.data matches 0 run function smithed.custom_block:impl/__version__/place/throw_warning
