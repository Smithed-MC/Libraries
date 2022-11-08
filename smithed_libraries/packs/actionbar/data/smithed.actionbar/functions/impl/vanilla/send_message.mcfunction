# halts other messages so vanilla actionbar messages can show
# @s = player who has triggered a vanilla actionbar
# located at @s or at container block (location is irrelevant tho)
# run from vanilla/bed/send_sleep_message
#          vanilla/container/check_lock

data modify storage smithed.actionbar:input message set value {priority:'notification',freeze:20}
function #smithed.actionbar:message
