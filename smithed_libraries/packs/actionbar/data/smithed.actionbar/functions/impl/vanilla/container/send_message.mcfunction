# send message for locked container
# @s = player who clicked a lockable block
# located at the center of the clicked block
# run from vanilla/container/check_lock

data modify storage smithed.actionbar:input message set value {priority:'notification',freeze:20}
function #smithed.actionbar:event/clicked_locked_container
execute if score $locked smithed.actionbar.temp matches 1 run function #smithed.actionbar:message
