# runs visuals to prevent unwanted blocks from being placed
#  ideally, this function should only ever run during development of a data pack
# @s = player who just placed a custom block
# located at the center of a custom block that failed to place
# run from place/block_unchanged

particle cloud ~ ~ ~ 0 0 0 0 10 force @a
setblock ~ ~ ~ air
function #smithed.custom_block:event/placement_failure
