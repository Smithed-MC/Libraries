# @public

# get the message input
# @s = player that needs a new title shown
# location undefined; based on how the user calls the function
# run from #smithed.title:message

# force-give player a priority score
scoreboard players add @s smithed.title.priority 0

# if there is a message, but they forgot the priority, it should be the default
execute if data storage smithed.title:input message run scoreboard players set $priority smithed.title.temp 99

# convert string priority into number
#  if we introduce new priorities in future versions
#  we can renumber our ints w/o issues
execute if data storage smithed.title:input message{priority:'override'} run scoreboard players set $priority smithed.title.temp 1
execute if data storage smithed.title:input message{priority:'notification'} run scoreboard players set $priority smithed.title.temp 2
execute if data storage smithed.title:input message{priority:'conditional'} run scoreboard players set $priority smithed.title.temp 3
execute if data storage smithed.title:input message{priority:'persistent'} run scoreboard players set $priority smithed.title.temp 4
execute unless data storage smithed.title:input message.priority run scoreboard players set $priority smithed.title.temp 99

# grab freeze
#  load default freeze if not defined
execute store result score $freeze smithed.title.temp run data get storage smithed.title:input message.freeze
execute
    unless data storage smithed.title:input message.freeze
    run scoreboard players operation $freeze smithed.title.temp = $default.freeze smithed.title.const

# to determine if we display
#  if priority is the same or lower AND current priority is not "override"
#  OR if player has no shown title
#    then display the message
execute
    unless score @s smithed.title.priority matches 1    # override notifications should not be "overriden"
    if score $priority smithed.title.temp <= @s smithed.title.priority
    run function smithed.title:impl/display

execute if score @s smithed.title.priority matches 0 run function smithed.title:impl/display

