
# get container name
execute if score $locked smithed.actionbar.temp matches 1 run data modify storage smithed.actionbar:input container_name set from block ~ ~ ~ CustomName
execute unless data storage smithed.actionbar:input container_name run function smithed.actionbar:impl/__version__/vanilla/container/get_default_name

# display message
data modify storage smithed.actionbar:input message set value {json:'{"translate":"container.isLocked","with":[{"nbt":"container_name","storage":"smithed.actionbar:input","interpret":true}],"color":"yellow"}',priority:'notification',freeze:10}
function #smithed.actionbar:message

# clean up
data remove storage smithed.actionbar:input container_name
