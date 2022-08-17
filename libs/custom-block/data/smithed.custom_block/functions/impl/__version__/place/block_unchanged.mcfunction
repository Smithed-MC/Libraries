# check if the custom block placement failed
# @s = player who just placed a custom block item
# located at the center of the custom block that needs updating
# run from place/found

execute store success score $changed smithed.custom_block run data modify storage smithed.custom_block:main blockApi.__data set from block ~ ~ ~
execute if score $changed smithed.custom_block matches 0 run function smithed.custom_block/impl/__version__/place/failed
